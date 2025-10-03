import matplotlib.pyplot as plt

# Example probability dictionary for 100 prisoners
# Most probabilities are tiny, only the last one (100) is significant
prob_dict = {k: 0.001 for k in range(1, 100)}  # tiny probabilities for 1-99
prob_dict[100] = 0.31  # probability all 100 succeed

# x and y values
x = list(prob_dict.keys())
y = list(prob_dict.values())

# Plot
plt.figure(figsize=(12, 6))
plt.bar(x, y, color="skyblue", edgecolor="blue")
plt.yscale("log")  # logarithmic scale
plt.xlabel("Number of prisoners succeeded")
plt.ylabel("Probability (log scale)")
plt.title("Cycle-Following Strategy Probability Distribution (100 Prisoners)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("cycle_strategy_probability_log.png")
plt.show()
