# 🗺️ AI Route Planner & Pathfinding Visualizer

A web-based visualization tool that demonstrates how modern navigation systems calculate the most efficient paths between two points. This project visualizes complex pathfinding algorithms in real-time, allowing users to understand the logic behind route-planning systems like Google Maps.

## ✨ Core Features
* **Interactive Grid:** Users can place start/end nodes and draw impenetrable walls (obstacles) to challenge the algorithms.
* **Real-Time Visualization:** Step-by-step animation of how algorithms explore the grid, highlighting visited nodes and the final shortest path.
* **Algorithm Comparison:**
  * **Dijkstra's Algorithm:** Guarantees the shortest path by exploring all possible routes equally.
  * **A* (A-Star) Search:** Uses heuristics (distance estimations) to guarantee the shortest path much faster than Dijkstra's by prioritizing directions closer to the target.

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Algorithms Implemented:** Dijkstra's Algorithm, A* (A-Star) Search

## 🚀 How to Run Locally
1. Clone this repository: `git clone https://github.com/shaheer095/ai-route-planner.git`
2. Navigate into the directory: `cd ai-route-planner`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the application: `python app.py`

> *Note: This project demonstrates my understanding of advanced data structures, algorithmic problem-solving, and efficient pathfinding optimization in Python.*
