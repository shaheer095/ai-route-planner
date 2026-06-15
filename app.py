"""
AI Route Planner — Flask Backend
Dijkstra's & A* on real OpenStreetMap data via OSMnx + NetworkX
"""

import heapq, math, time, logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import osmnx as ox

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# ── In-memory graph cache ──────────────────────────────────────
_CACHE = {}

def get_graph(city: str):
    if city not in _CACHE:
        log.info(f"Downloading OSM graph for: {city}")
        G = ox.graph_from_place(city, network_type="drive")
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        _CACHE[city] = G
        log.info(f"Cached: {len(G.nodes)} nodes, {len(G.edges)} edges")
    return _CACHE[city]

# ── Edge weight helper ─────────────────────────────────────────
def _w(G, u, v, attr="length"):
    data = G.get_edge_data(u, v)
    if not data:
        return math.inf
    vals = [e.get(attr, math.inf) for e in data.values()
            if isinstance(e, dict) and e.get(attr) is not None]
    return min(vals) if vals else math.inf

# ── Dijkstra ───────────────────────────────────────────────────
def dijkstra(G, src, dst, attr="length"):
    t0 = time.perf_counter()
    dist = {n: math.inf for n in G.nodes}
    dist[src] = 0
    prev = {}
    vis  = set()
    pq   = [(0.0, src)]
    exp  = 0

    while pq:
        d, u = heapq.heappop(pq)
        if u in vis: continue
        vis.add(u); exp += 1
        if u == dst: break
        for v in G.neighbors(u):
            nd = d + _w(G, u, v, attr)
            if nd < dist[v]:
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd, v))

    ms = (time.perf_counter() - t0) * 1000
    return _path(prev, src, dst), dist.get(dst, math.inf), exp, ms

# ── A* ─────────────────────────────────────────────────────────
def _hav(G, a, b):
    R = 6_371_000
    la1,lo1 = math.radians(G.nodes[a]["y"]), math.radians(G.nodes[a]["x"])
    la2,lo2 = math.radians(G.nodes[b]["y"]), math.radians(G.nodes[b]["x"])
    x = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return R * 2 * math.asin(math.sqrt(x))

def astar(G, src, dst, attr="length"):
    t0 = time.perf_counter()
    g  = {n: math.inf for n in G.nodes}
    g[src] = 0
    prev = {}
    closed = set()
    pq = [(_hav(G,src,dst), 0.0, src)]
    exp = 0

    while pq:
        _, cost, u = heapq.heappop(pq)
        if u in closed: continue
        closed.add(u); exp += 1
        if u == dst: break
        for v in G.neighbors(u):
            if v in closed: continue
            ng = g[u] + _w(G, u, v, attr)
            if ng < g[v]:
                g[v] = ng; prev[v] = u
                heapq.heappush(pq, (ng + _hav(G,v,dst), ng, v))

    ms = (time.perf_counter() - t0) * 1000
    return _path(prev, src, dst), g.get(dst, math.inf), exp, ms

def _path(prev, src, dst):
    p, n = [], dst
    while n != src:
        p.append(n)
        n = prev.get(n)
        if n is None: return []
    p.append(src); p.reverse()
    return p

def travel_time_min(G, path):
    total = 0
    for u, v in zip(path[:-1], path[1:]):
        data = G.get_edge_data(u, v)
        if data:
            ts = [e.get("travel_time",0) for e in data.values() if isinstance(e,dict)]
            if ts: total += min(ts)
    return round(total/60, 1)

# ── Routes ─────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/health")
def health():
    return jsonify({"ok": True})

@app.route("/api/route", methods=["POST"])
def api_route():
    body  = request.get_json()
    city  = body.get("city", "Islamabad, Pakistan")
    orig  = body.get("origin")
    dest  = body.get("destination")
    mode  = body.get("weight", "length")   # "length" or "travel_time"

    if not orig or not dest:
        return jsonify({"error": "origin and destination required"}), 400

    try:
        G = get_graph(city)
        sn = ox.distance.nearest_nodes(G, orig["lng"], orig["lat"])
        dn = ox.distance.nearest_nodes(G, dest["lng"], dest["lat"])

        if sn == dn:
            return jsonify({"error": "Points are too close — try locations further apart."}), 400

        d_path, d_dist, d_exp, d_ms = dijkstra(G, sn, dn, mode)
        a_path, a_dist, a_exp, a_ms = astar(G, sn, dn, mode)

        def fmt(path, dist, exp, ms, name):
            if not path:
                return {"found": False, "name": name}
            coords = [[G.nodes[n]["y"], G.nodes[n]["x"]] for n in path]
            return {
                "found": True, "name": name,
                "coords": coords,
                "distance_m": round(dist),
                "distance_km": round(dist/1000, 2),
                "travel_min": travel_time_min(G, path),
                "nodes_explored": exp,
                "time_ms": round(ms, 2),
            }

        return jsonify({
            "dijkstra": fmt(d_path, d_dist, d_exp, d_ms, "Dijkstra"),
            "astar":    fmt(a_path, a_dist, a_exp, a_ms, "A*"),
            "snap": {
                "origin":      [G.nodes[sn]["y"], G.nodes[sn]["x"]],
                "destination": [G.nodes[dn]["y"], G.nodes[dn]["x"]],
            }
        })

    except Exception as e:
        log.error(e, exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/api/geocode")
def api_geocode():
    place = request.args.get("q","")
    if not place:
        return jsonify({"error":"q param required"}), 400
    try:
        lat, lng = ox.geocoder.geocode(place)
        return jsonify({"lat": lat, "lng": lng})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
