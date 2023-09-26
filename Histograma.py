import numpy as np
import matplotlib.pyplot as plt

# Number of simulations
num_simulations = 3000

# Time steps
n = 10000

# Initialize an array to store the final values of X_n for each simulation
final_values = np.zeros(num_simulations)

# Loop through each simulation
for i in range(num_simulations):
    # Initial number of white balls
    Y_n = 1
    # Initial total number of balls
    total_balls = 1
    
    # Simulate the process
    for t in range(1, n + 1):
        # Add a white ball with 50% probability, otherwise add a black ball
        new_ball = np.random.choice(['white', 'black'])
        if new_ball == 'white':
            Y_n += 1
        total_balls += 1
        
        # Update X_n (martingale)
        X_n = Y_n / (total_balls + 1)
    
    # Store the final value of X_n for this simulation
    final_values[i] = X_n

# Create the histogram
plt.figure(figsize=(10, 6))
plt.hist(final_values, bins=30, density=True, color='skyblue', edgecolor='black')
plt.xlabel('$X_{10,000}$')
plt.ylabel('Frequency')
plt.title('Histogram of $X_{10,000}$ for 3000 Simulations')
plt.grid(True)
plt.show()
