import pandas as pd
import numpy as np
from datetime import timedelta

# Prepare data
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df = df.sort_values(['code', 'datetime'])

# Get all unique sectors
sectors = sorted(df['sector'].unique())
sector_index = {sector: i for i, sector in enumerate(sectors)}
n_sectors = len(sectors)

# Initialize count matrix
count_matrix = np.zeros((n_sectors, n_sectors))

# Get all unique person-date combinations
person_dates = df[['code', 'date']].drop_duplicates().sort_values(['code', 'date'])

# Create 3-day sequences for each person
for person in df['code'].unique():
    person_dates_subset = person_dates[person_dates['code'] == person]
    dates = sorted(person_dates_subset['date'].unique())
    
    # Create sliding window of 3 consecutive days
    for i in range(len(dates) - 2):
        day1, day2, day3 = dates[i], dates[i+1], dates[i+2]
        
        # Check if days are consecutive (optional)
        # if (day2 - day1 == timedelta(days=1)) and (day3 - day2 == timedelta(days=1)):
        
        # Get transactions for this 3-day window
        window_trans = df[(df['code'] == person) & 
                         (df['date'].isin([day1, day2, day3]))]
        
        # Sort by datetime and process transitions
        sectors_sequence = window_trans.sort_values('datetime')['sector'].values
        
        # Count all transitions in the 3-day window
        for j in range(len(sectors_sequence) - 1):
            from_sector = sectors_sequence[j]
            to_sector = sectors_sequence[j+1]
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

print("3-Day Sequence Transition Matrix:")
print(transition_df.round(3))
