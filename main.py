from datetime import timedelta
from tqdm import tqdm

arr = []

# Define time windows
t_delta = (timedelta(days=0, hours=22), timedelta(days=1, hours=2))
t_delta_7 = (timedelta(days=6, hours=22), timedelta(days=7, hours=2))

# Initialize check columns
grouped_['Check_1'] = False
grouped_['Check_7'] = False

def mark_sequences(temp_df, check_col, time_window, day_step):
    checked = temp_df[check_col].values
    datetimes = temp_df['DateTime'].values

    for i in range(len(temp_df)):
        if not checked[i]:
            count = 1
            checked[i] = True
            base_time = datetimes[i]
            for j in range(i + 1, len(temp_df)):
                expected_time = base_time + timedelta(days=day_step * (count))
                time_diff = datetimes[j] - expected_time
                if not checked[j] and time_window[0] < time_diff < time_window[1]:
                    count += 1
                    checked[j] = True
            if count > 1:
                row = {
                    'Code': temp_df.index[0][0],  # Update based on your index
                    'Check_Type': check_col,
                    'Start': base_time,
                    'Count': count,
                    # Add any other needed fields
                }
                arr.append(row)

for index in tqdm(indexes):
    temp_df = grouped_.loc[index].sort_values('DateTime').copy()
    mark_sequences(temp_df, 'Check_1', t_delta, 1)
    mark_sequences(temp_df, 'Check_7', t_delta, 7)
