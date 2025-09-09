# MRGC
Simulating a Resource Scheduler with MSTs and Graph Coloring
We present a graph-theoretic scheduling algorithm that builds a minimum spanning tree to minimize connection cost and applies graph coloring to allocate resources without conflicts, enabling efficient, simulatable schedules under dependency and concurrency constraints.

# MRGC vs Random vs Fully vs RoundRobin Simulation

This project simulates 4 different scheduling and resource allocation strategies on agent–graph environments.  
It compares **MRGC (Minimum Spanning Tree + Greedy Coloring)**, **Random**, **Round Robin**, and **Fully Connected Graph** strategies in terms of conflicts, delay, utilization, success rate, and throughput.

##  Features
- **Graph generation**
  - Random agent graphs (with max edges per node)
  - Fully connected graphs
- **Coloring strategies**
  - MRGC (using MST + greedy coloring)
  - Random slot assignment
  - Round-robin slot assignment
  - Greedy coloring on fully connected graphs
- **Metrics**
  - Conflicts
  - Delay
  - Utilization
  - Success rate
  - Throughput
- **CSV result Export**
  - Results saved in structured format for later analysis


## Step

### 
1. Install dependencies
pip install networkx
python 3.11

3. Run the simulation
python simulation.py --agents 20 --slots 5 --episodes 10 --max_edges 3 --seed 42 --output output/results.csv
Note: we change to agent number with 20,50,100, Can try diffrent parameters.
5. Arguments examples
Argument	Type	Default	Description
--agents	int	20	Number of agents (nodes in graph)
--slots	int	5	Number of resource slots
--episodes	int	10	Number of simulation episodes
--max_edges	int	3	Maximum number of edges per agent in random graph
--seed	int	42	Random seed for reproducibility
--output	str	output/results.csv	Output CSV file path

Output Format
The results are saved as a CSV file with the following columns:

Example Workflow
Generate random and fully connected graphs.

Apply multiple slot assignment strategies.

Simulate execution to measure conflicts, delay, utilization, success rate, and throughput.

Save results into CSV for later visualization and analysis (e.g., matplotlib, pandas, Excel).

📂 Project Structure

simulation.py        # Main script
output/results.csv   # Example output file
README.md            # Documentation

