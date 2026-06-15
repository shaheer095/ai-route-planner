# 🗺️ AI Route Planner & Pathfinding Visualizer

A web-based visualization tool that demonstrates how modern navigation systems calculate the most efficient paths between two points. This project visualizes complex pathfinding algorithms in real-time, allowing users to understand the logic behind route-planning systems like Google Maps.

## ✨ Core Features
* **Interactive Grid:** Users can place start/end nodes and draw impenetrable walls (obstacles) to challenge the algorithms.
* **Real-Time Visualization:** Step-by-step animation of how algorithms explore the grid, highlighting visited nodes and the final shortest path.
* **Algorithm Comparison:**
  * **Dijkstra's Algorithm:** Guarantees the shortest path by exploring all possible routes equally.
  * **A* (A-Star) Search:** Uses heuristics (distance estimations) to guarantee the shortest path much faster than Dijkstra's by prioritizing directions closer to the target.

## 🛠️ Technical Stack
* **Frontend:** React.js, HTML5, CSS3 
* **State Management:** React Hooks
* **Algorithms Implemented:** Dijkstra, A* Search, Breadth-First Search (BFS)

## 🚀 How to Run Locally
1. Clone this repository: `git clone [Insert Your Repo URL Here]`
2. Navigate into the directory: `cd route-planner`
3. Install the required dependencies: `npm install`
4. Start the development server: `npm start`
5. The application will be running at `http://localhost:3000`

> *Note: This project is part of my software engineering portfolio, demonstrating algorithmic problem solving and front-end state management.*