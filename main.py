def calculate_3day_transitions(df):
    # Convert and sort data
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].dt.date
    df = df.sort_values(['code', 'datetime'])
    
    # Get all unique sectors
    sectors = sorted(df['sector'].unique())
    sector_index = {sector: i for i, sector in enumerate(sectors)}
    n_sectors = len(sectors)
    
    # Initialize count matrix
    count_matrix = np.zeros((n_sectors, n_sectors), dtype=np.int32)
    
    # Pre-calculate date sequences per person
    person_date_sequences = df.groupby('code')['date'].unique()
    
    for person, dates in person_date_sequences.items():
        dates = sorted(dates)
        
        # Vectorized 3-day window processing
        for i in range(len(dates) - 2):
            day1, day2, day3 = dates[i], dates[i+1], dates[i+2]
            
            # Get transactions using boolean indexing (faster than isin)
            mask = (df['code'] == person) & (
                (df['date'] == day1) | 
                (df['date'] == day2) | 
                (df['date'] == day3)
            )
            window_trans = df.loc[mask]
            
            # Process transitions
            sectors_sequence = window_trans['sector'].values
            for j in range(len(sectors_sequence) - 1):
                from_idx = sector_index[sectors_sequence[j]]
                to_idx = sector_index[sectors_sequence[j+1]]
                count_matrix[from_idx, to_idx] += 1
                
    return count_matrix, sectors

def create_transition_matrix(count_matrix, sectors):
    # Convert counts to probabilities
    row_sums = count_matrix.sum(axis=1, keepdims=True)
    transition_matrix = np.divide(count_matrix, row_sums, 
                                out=np.zeros_like(count_matrix, dtype=np.float64),
                                where=row_sums!=0)
    
    return pd.DataFrame(transition_matrix, index=sectors, columns=sectors)

# Main execution
count_matrix, sectors = calculate_3day_transitions(df)
transition_df = create_transition_matrix(count_matrix, sectors)

print("Optimized 3-Day Transition Matrix:")
print(transition_df.round(3))
