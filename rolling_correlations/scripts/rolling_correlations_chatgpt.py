# Rolling correlation: chatgpt example 

import numpy as np
import pandas as pd

# Create a sample DataFrame with two columns
data = {'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1]}
df = pd.DataFrame(data)

data2 = {'A': [1, 1, 1, 1, 1],
        'B': [1, 2, 3, 4, 5]}
df2 = pd.DataFrame(data2)



# Create a sample DataFrame with two variables
np.random.seed(42)
data3 = {'A': np.random.rand(100),
        'B': 2 * np.random.rand(100)}  # B is a constant multiple of A

df3 = pd.DataFrame(data3)


# Choose a window size for the rolling correlation
window_size = 10

# Calculate rolling correlation
rolling_corr = df3['A'].rolling(window=window_size).corr(df3['B'])

# Print the result
print(type(rolling_corr))
print(rolling_corr.tail(40))


import matplotlib.pyplot as plt

# Plot the rolling correlation
plt.plot(rolling_corr, label='Rolling Correlation')
plt.title('Rolling Correlation between A and B')
plt.xlabel('Time')
plt.ylabel('Correlation')
plt.legend()
plt.show()