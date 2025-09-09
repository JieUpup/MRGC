import argparse
from dataclasses import dataclass, asdict
import networkx as nx
import random
from collections import defaultdict
import csv
import os


@dataclass
class Metrics:
    episode: int
    strategy: str
    conflicts: int
    delay: int
    utilization: float
    success_rate: float
    throughput: int


def build_random_agent_graph(num_agents, max_edges, seed=None):
    if seed is not None:
        random.seed(seed)
    G = nx.Graph()
    G.add_nodes_from(range(num_agents))
    for node in G.nodes():
        neighbors = random.sample([n for n in G.nodes() if n != node], k=random.randint(1, max_edges))
        for n in neighbors:
            if not G.has_edge(node, n):
                weight = random.randint(1, 10)
                G.add_edge(node, n, weight=weight)
    return G

def build_fully_connected_graph(num_agents, seed=None):
    if seed is not None:
        random.seed(seed)
    G = nx.complete_graph(num_agents)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)
    return G

def generate_graph_pool(strategy, pool_size, num_agents, max_edges, base_seed):
    pool = []
    for i in range(pool_size):
        seed = base_seed + i
        if strategy == "random":
            pool.append(build_random_agent_graph(num_agents, max_edges, seed))
        elif strategy == "fully":
            pool.append(build_fully_connected_graph(num_agents, seed))
    return pool


def greedy_coloring(G):
    return nx.coloring.greedy_color(G, strategy='largest_first')

def random_coloring(num_agents, num_slots):
    return {i: random.randint(0, num_slots - 1) for i in range(num_agents)}

def round_robin_coloring(num_agents, num_slots):
    return {i: i % num_slots for i in range(num_agents)}

# ------------------Simulation Rounds ------------------ #
def simulate_execution(coloring, num_slots):
    slots = defaultdict(list)
    for agent, slot in coloring.items():
        slots[slot].append(agent)

    conflicts = sum(len(v) > 1 for v in slots.values())
    delay = sum(random.randint(1, 5) for _ in slots)
    utilization = len(slots) / num_slots
    success_rate = 1 - conflicts / len(coloring) if coloring else 0
    throughput = len(coloring) - conflicts

    return conflicts, delay, utilization, success_rate, throughput


def run_experiment(args):
    results = []
    random_graphs = generate_graph_pool("random", args.episodes, args.agents, args.max_edges, args.seed)
    fully_graphs = generate_graph_pool("fully", args.episodes, args.agents, args.max_edges, args.seed)

    for ep in range(args.episodes):
        # MRGC
        mst = nx.minimum_spanning_tree(random_graphs[ep])
        mrgc_coloring = greedy_coloring(mst)
        c, d, u, s, t = simulate_execution(mrgc_coloring, args.slots)
        results.append(Metrics(ep, "MRGC", c, d, u, s, t))

        # Random
        rand_coloring = random_coloring(args.agents, args.slots)
        c, d, u, s, t = simulate_execution(rand_coloring, args.slots)
        results.append(Metrics(ep, "Random", c, d, u, s, t))

        # RoundRobin
        rr_coloring = round_robin_coloring(args.agents, args.slots)
        c, d, u, s, t = simulate_execution(rr_coloring, args.slots)
        results.append(Metrics(ep, "RoundRobin", c, d, u, s, t))

        # Fully Graph
        full_coloring = greedy_coloring(fully_graphs[ep])
        c, d, u, s, t = simulate_execution(full_coloring, args.slots)
        results.append(Metrics(ep, "FullyGraph", c, d, u, s, t))

    return results

def save_to_csv(results, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=asdict(results[0]).keys())
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))


def parse_args():
    parser = argparse.ArgumentParser(description="MRGC vs Random vs Fully vs RoundRobin Simulation")
    parser.add_argument("--agents", type=int, default=20, help="Number of agents")
    parser.add_argument("--slots", type=int, default=5, help="Number of resource slots")
    parser.add_argument("--episodes", type=int, default=10, help="Number of episodes")
    parser.add_argument("--max_edges", type=int, default=3, help="Max edges per agent in random graph")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default="output/results.csv", help="CSV output file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    results = run_experiment(args)
    save_to_csv(results, args.output)
    print(f"Simulation finished. Results saved to {args.output}")

