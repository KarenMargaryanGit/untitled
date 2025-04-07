import pandas as pd
import numpy as np
from collections import defaultdict

# Assuming your data has:
# - 'code': transaction identifier
# - 'datetime': full timestamp (date + time)
# - 'sector': the sector category

# Convert to datetime if not already
df['datetime'] = pd.to_datetime(df['datetime'])

# Sort by datetime to get proper transaction sequence
df = df.sort_values('datetime')

# Get all unique sectors
sectors = sorted(df['sector'].unique())
sector_index = {sector: i for i, sector in enumerate(sectors)}
n_sectors = len(sectors)

# Initialize count matrix
count_matrix = np.zeros((n_sectors, n_sectors))

# Create date column for daily grouping
df['date'] = df['datetime'].dt.date

# Group by date and process each day's transactions
for date, group in df.groupby('date'):
    # Get sectors in order of their transaction times
    sectors_sequence = group.sort_values('datetime')['sector'].values
    
    # Count transitions within this day
    for i in range(len(sectors_sequence) - 1):
        from_sector = sectors_sequence[i]
        to_sector = sectors_sequence[i+1]
        count_matrix[sector_index[from_sector], sector_index[to_sector]] += 1

    # OPTIONAL: Handle cross-day transitions (comment out if not needed)
    if len(sectors_sequence) > 0:
        last_sector_of_day = sectors_sequence[-1]
        next_day_first_sector = df[df['date'] == date + pd.Timedelta(days=1)].sort_values('datetime')['sector'].values
        if len(next_day_first_sector) > 0:
            count_matrix[sector_index[last_sector_of_day], sector_index[next_day_first_sector[0]]] += 1

# Convert counts to probabilities
transition_matrix = np.zeros_like(count_matrix)
for i in range(n_sectors):
    row_sum = count_matrix[i].sum()
    if row_sum > 0:
        transition_matrix[i] = count_matrix[i] / row_sum
    else:
        transition_matrix[i] = 0

# Create a readable DataFrame
transition_df = pd.DataFrame(transition_matrix,
                           index=sectors,
                           columns=sectors)

print("Markov Transition Matrix with Datetime Handling:")
print(transition_df.round(3))  # Round to 3 decimal places for readability
