




prodeco.am;cas2k16.ameriabank.am;confluence.ameriabank.am;*.ameriabank.am;*.ameria-bank.am;*.ameriabank.local;*.ameriagroup.am;*.ameriaonline.am;*.myameria.am;services.nasdaqomx.am;fxlimits.amx.net;10.115.30.*;172.16.75.*;172.16.76.*;172.16.83.13;192.168.99.*;192.168.199.*;172.16.178.*;172.16.179.*;172.16.188.*;192.168.197.60;192.168.197.160;172.16.194.15;192.168.23*;192.168.225*;10.100.65.100;100.39.143.111;100.39.143.110;SRV-SQL16-CRM1;SRV-SQL16-CRM2;ccagent.ameriabank.am;myameria.am

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
