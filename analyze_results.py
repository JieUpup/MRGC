import pandas as pd


files = {
    "results_edge10.csv": 20,
    "results_edge25.csv": 25,
    "results_edge50.csv": 50
}

all_data = []

for filename, agent_count in files.items():
    df = pd.read_csv(filename)
    df["agents"] = agent_count
    all_data.append(df)


df_all = pd.concat(all_data, ignore_index=True)


summary = df_all.groupby(["agents", "strategy"]).agg({
    "conflicts": "mean",
    "delay": "mean",
    "utilization": "mean",
    "success_rate": "mean",
    "throughput": "mean"
}).round(2).reset_index()


summary.to_csv("summary_results_edge.csv", index=False)


print("summary_results_edge.csv，as below：\n")
print(summary)

