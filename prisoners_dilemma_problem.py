"""
Problem statement (classic version)

There are 100 prisoners and 100 boxes in a room.
Each prisoner is assigned a unique number from 1 to 100.
The 100 slips, one per prisoner number, are placed one per box in a random permutation (each box contains exactly one distinct prisoner number).
One by one, each prisoner may enter the room (they cannot communicate or leave hints for later prisoners).
Inside, each prisoner may open up to 50 boxes (i.e., half of the boxes). They may look at the slips in those boxes but must leave the slips where they found them and must close the boxes again.
If every prisoner finds the slip with their own number among the boxes they opened, then all prisoners are released.
If any prisoner fails to find their own number, all prisoners are executed (or lose) — so success requires every prisoner to succeed.

What is the question?

Can the prisoners use a strategy that gives them a good chance to all survive, and if so, what is it and how likely is success?
Naive approach (and why it's terrible)
If each prisoner just randomly opens 50 boxes (independently), the probability that a given prisoner finds their number is 1/2.
The probability that all 100 succeed is (1/2)^100 which is astronomically small (~7.9 x 10 ^ -31).
So a naive independent strategy is essentially hopeless.

The powerful (and optimal) strategy — follow the permutation cycles
Number the boxes 1-100 (boxes have fixed labels).
Each prisoner i when entering the room:
First opens the box labeled i.
If that box contains slip i, done.
If it contains slip j (some other number), the prisoner next opens the box labeled j.
Continue following this chain (open box whose label equals the number just seen) until either the prisoner finds his own number or has opened 50 boxes.
Every prisoner uses the same rule (starting at their own box and following the permutation cycle).
Why this helps: the boxes and their contents form a permutation of 1..100, which decomposes uniquely into disjoint cycles.
Following the boxes is exactly following the cycle that contains that prisoner's number.
A prisoner will find his number within 50 opens if his cycle length ≤ 50.
Success condition with this strategy

All prisoners succeed = the permutation has no cycle of length > 50.
So the problem reduces to: what is the probability that a uniformly random permutation of 100 elements has all cycle lengths ≤ 50?

Success probability (numeric)
The probability that a random permutation of 100 has no cycle longer than 50 is about 0.311827…, i.e. roughly 31.18%.
That means using the cycle-following strategy gives ~31% chance that all 100 prisoners survive — astronomically better than(~7.9 x 10 ^ -31).
"""

"""
In the below program we will test with 
1. choosing a random box (We will limit the max iterations to 10000, as we cannot run till they succeed)
2. using the optimal solution.
"""


import random
from pprint import pprint
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.stats import binom
import numpy as np
import logging
import json

logging.basicConfig(
    filename="prisoners_dilemma_problem.log",
    format="[%(asctime)s] [%(levelname)8s] : %(message)s",
    force=True,
    level="INFO",
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


prisoners_numbers = list(range(1, 101))

# Assiging unique numbers to 100 box
box_numbers = {}
num_lis = list(range(1, 101))
for i in range(1, 101):
    num = random.choice(num_lis)
    box_numbers[f"box_{i}"] = num
    num_lis.remove(num)

logger.info("Box's Unique numbers are")
logger.info(json.dumps(box_numbers, indent=4))
# print("Box's Unique numbers are")
# pprint(box_numbers, sort_dicts=False)


plot_graph = True
max_iteration = 100000

# Random choice
logger.info("Running Random Choice")
win_cnt = 0
win_cnt_list = []
for iter_cnt in tqdm(range(max_iteration)):
    number_found_cnt = 0
    for i in prisoners_numbers:
        number_found = False
        boxes_numbers_keys = list(box_numbers.keys())
        for open_cnt in range(50):
            box_id = random.choice(boxes_numbers_keys)
            boxes_numbers_keys.remove(box_id)
            if box_numbers[box_id] == i:
                number_found = True
                break
        if number_found:
            logger.info(f"Number Found: {i} - {box_id}")
            # print(f"Number Found: {i} - {box_id}")
            number_found_cnt += 1

    win_cnt_list.append(number_found_cnt)
    if number_found_cnt == 100:
        # print("All prisoners found their number")
        win_cnt += 1
    logger.info(f"Iteration {iter_cnt}: {number_found_cnt}/100 found their number")
    # print(f"Iteration {iter_cnt}: {number_found_cnt}/100 found their number")
logger.info(f"Win % = {win_cnt}/{max_iteration} = {round(win_cnt/max_iteration, 6)} %")
print(f"Win % = {win_cnt}/{max_iteration} = {round(win_cnt/max_iteration, 6)} %")

if plot_graph:
    n = 100  # number of trials
    p = 0.5  # success probability
    # X-axis: number of successes (0 to n)
    x = win_cnt_list
    y = binom.pmf(x, n, p)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.bar(x, y, width=1.0, color="skyblue", edgecolor="blue")
    plt.xlim(0, 100)
    plt.ylim(0, max(y) * 1.1)
    plt.xlabel("Number of Successes")
    plt.ylabel("Probability")
    plt.title(f"Binomial Distribution: n={n}, p={p}")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig("random_choice.png")  # can use .pdf, .jpg, etc.
    plt.close()


# Optimal choice (Cyclic)
logger.info("Running Optimal Choice")
win_cnt = 0
win_cnt_list = []
for iter_cnt in tqdm(range(max_iteration)):
    box_numbers = {}
    num_lis = list(range(1, 101))
    # Assiging unique numbers to 100 box - Resetting, otherwise will be checking the same box sequence everytime
    for i in range(1, 101):
        num = random.choice(num_lis)
        box_numbers[f"box_{i}"] = num
        num_lis.remove(num)
    logger.debug("Box's Unique numbers are")
    logger.debug(json.dumps(box_numbers, indent=4))

    number_found_cnt = 0
    for i in prisoners_numbers:
        number_found = False
        box_id = f"box_{i}"
        for open_cnt in range(50):
            if box_numbers[box_id] == i:
                number_found = True
                break
            else:
                box_id = f"box_{box_numbers[box_id]}"

        if number_found:
            logger.debug(f"Number Found: {i} - {box_id} on {open_cnt+1} try")
            # print(f"Number Found: {i} - {box_id} on {open_cnt+1} try")
            number_found_cnt += 1

    win_cnt_list.append(number_found_cnt)
    if number_found_cnt == 100:

        # print("All prisoners found their number")
        win_cnt += 1
    logger.info(f"Iteration {iter_cnt}: {number_found_cnt}/100 found their number")
    # print(f"Iteration {iter_cnt}: {number_found_cnt}/100 found their number")
logger.info(f"Win % = {win_cnt}/{max_iteration} = {round(win_cnt/max_iteration, 6)} %")
print(f"Win % = {win_cnt}/{max_iteration} = {round(win_cnt/max_iteration, 6)} %")

if plot_graph:

    x = win_cnt_list
    x_len = len(x)
    prob_dict = {}
    for i in range(101):
        prob_dict[i] = x.count(i) / x_len

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
    plt.savefig("optimal_choice.png")
    plt.close()


"""
if longest cycle <=50, all will succeed, if >50, all people in that cycle will fail, hence 51-99 is impossible.

Each prisoner can open up to 50 boxes.
Boxes contain numbers forming a random permutation.
Permutation can be broken into disjoint cycles.
Example: cycle (3 → 7 → 2 → 3)
If a cycle is longer than 50, all prisoners in that cycle fail.
If all cycles ≤ 50, everyone succeeds.


Why the number of prisoners succeeding is almost always either small (<50) or all 100

Key rule: if any cycle in the permutation has length > 50, every prisoner in that cycle will fail.
If all cycles ≤ 50, then all 100 prisoners succeed.
There is no way for exactly 51-99 prisoners to succeed:
If some cycle > 50 exists, all prisoners in that cycle fail.
This will reduce the total number of prisoners succeeding to ≤50 (roughly 1-50).
If all cycles ≤50, then everyone succeeds, so total = 100.

Probability distribution shape
# prisoners succeed	Probability
1-50	small (~0.01) — occurs when there is a long cycle >50
51-99	0 — impossible due to how cycles work
100	large (~0.31) — occurs when all cycles ≤50

Reason 51-99 is impossible:
Any cycle >50 means all prisoners in that cycle fail, which removes ≥51 prisoners from success? Not quite — let's refine:



1-50 prisoners succeed → happens when there is a cycle >50
51-99 prisoners succeed → impossible
100 prisoners succeed → happens when all cycles ≤50
"""
# # Plot
# plt.figure(figsize=(12, 6))
# plt.bar(x, y, width=1.0, color="skyblue", edgecolor="blue")
# plt.xlim(0, 100)
# plt.ylim(0, max(y) * 1.1)
# plt.xlabel("Number of Successes")
# plt.ylabel("Probability")
# plt.title(f"Binomial Distribution: n={n}, p={p}")
# plt.grid(axis="y", linestyle="--", alpha=0.7)
# plt.show()

# plt.savefig("optimal_choice.png")  # can use .pdf, .jpg, etc.
# plt.close()
