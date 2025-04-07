import pandas as pd
import numpy as np
from collections import defaultdict

# Convert to datetime if not already
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date

# Sort by person, date, and time to get proper sequences
df = df.sort_values(['code', 'date', 'datetime'])

# Get all unique sectors
sectors = sorted(df['sector'].unique())
sector_index = {sector: i for i, sector in enumerate(sectors)}
n_sectors = len(sectors)

# Initialize count matrix
count_matrix = np.zeros((n_sectors, n_sectors))

# Group by person and date to get daily sequences per person
for (person, date), daily_trans in df.groupby(['code', 'date']):
    sectors_sequence = daily_trans['sector'].values
    
    # Count transitions for this person on this day
    for i in range(len(sectors_sequence) - 1):
        from_sector = sectors_sequence[i]
        to_sector = sectors_sequence[i+1]
        count_matrix[sector_index[from_sector], sector_index[to_sector]] += 1

# Convert counts to probabilities
transition_matrix = np.zeros_like(count_matrix)
for i in range(n_sectors):
    row_sum = count_matrix[i].sum()
    if row_sum > 0:
        transition_matrix[i] = count_matrix[i] / row_sum
    else:
        transition_matrix[i] = 0

# Create final transition matrix
transition_df = pd.DataFrame(transition_matrix,
                           index=sectors,
                           columns=sectors)

print("Person- and Day-Aware Transition Matrix:")
print(transition_df.round(3))
