import random

def should_pick_extra(n1):
    avg_iterations, remainder = divmod(n1, 5)
    # Calculate the weighted probabilities
    p_extra = remainder / 5
    p_no_extra = 1 - p_extra

    # Decide based on weighted random choice
    choice = random.choices([0, 1], weights=[p_no_extra, p_extra], k=1)[0]
    
    return choice == 1

# This can be called by each distributed process
n1 = 7
for _ in range(5):  # representing the 5 processes
    extra = should_pick_extra(n1)
    print("Extra iteration?" if extra else "Base iterations only")
