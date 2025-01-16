import pandas as pd
import numpy as np
from tqdm import tqdm

# Initialize a list to store the new rows
rows = []

# Group by 'FCLICODE'
grouped = df.groupby('FCLICODE')

for client_code, temp_df in tqdm(grouped):
    temp_df = temp_df.sort_values(by='ReportDate')
    
    for key in ['Bonds', 'Demand Deposits', 'Time Deposit']:
        row_dict = {
            'FCLICODE': client_code,
            'Start Balance': 0,
            'New Clients': 0,
            'Closed Clients': 0,
            'From other': 0,
            'Spch': 0,
            'End Balance': 0,
            'Category': key,
        }

        if temp_df.shape[0] == 1:
            temp_date = temp_df['ReportDate'].iloc[0].replace('-', '')
            if temp_date == startDate:
                row_dict['Closed Clients'] = temp_df[key].iloc[0]
                row_dict['Start Balance'] = temp_df[key].iloc[0]
            elif temp_date == endDate:
                row_dict['New Clients'] = temp_df[key].iloc[0]
                row_dict['End Balance'] = temp_df[key].iloc[0]
        else:
            row_dict['Start Balance'] = temp_df[key].iloc[0]
            row_dict['End Balance'] = temp_df[key].iloc[1]

            sum1 = temp_df.iloc[1][2:].sum() - temp_df.iloc[1][key]
            sum2 = temp_df.iloc[0][2:].sum() - temp_df.iloc[0][key]

            balance_diff = row_dict['End Balance'] - row_dict['Start Balance']
            sum_diff = sum2 - sum1

            if (balance_diff > 0 and sum_diff < 0) or (balance_diff < 0 and sum_diff > 0):
                row_dict['From other'] = (
                    min(abs(balance_diff), abs(sum_diff)) * (1 if balance_diff > 0 else -1)
                )
            row_dict['Spch'] = balance_diff - row_dict['From other']

        rows.append(row_dict)

# Convert the list of rows into a DataFrame
new_df = pd.DataFrame(rows)
