import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib widget

df = pd.read_csv("./src/assets/dataset.csv")

df['winner_was_first_mover'] = (df['winner'] == df['first_move']).astype(int)

# Count wins for each player from first move and second move
wins_first_move = df[df['winner_was_first_mover'] == 1]['winner'].value_counts()
wins_second_move = df[df['winner_was_first_mover'] == 0]['winner'].value_counts()

# Create a new DataFrame with the counts
df_wins = pd.DataFrame({'First Move': wins_first_move, 'Second Move': wins_second_move})

# Plot the DataFrame as a bar plot
df_wins.plot(kind='bar', figsize=(10,6))

plt.title('Wins for each player from first and second move')
plt.xlabel('Player')
plt.ylabel('Wins')
plt.legend(loc='upper left')

print(int(np.ceil(df_wins.max().max())))

plt.ylim(0, int(np.ceil(df_wins.max().max())))
plt.yticks(range(0, int(np.ceil(df_wins.max().max()) + 1), 1))

plt.show()