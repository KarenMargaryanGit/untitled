import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load data
df = pd.read_csv('example.csv')

def show_top_losers():
    top_losers = df.nsmallest(100, 'End Balance')
    st.header('Top 100 Losers')
    st.dataframe(top_losers)
    fig1, ax1 = plt.subplots()
    ax1.bar(top_losers['FCLICODE'], top_losers['End Balance'])
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    tick_positions = ax1.get_xticks()
    tick_labels = top_losers['FCLICODE'].iloc[:len(tick_positions)]
    ax1.set_xticklabels(tick_labels, rotation=90)
    st.pyplot(fig1)

def show_top_gainers():
    top_gainers = df.nlargest(100, 'End Balance')
    st.header('Top 100 Gainers')
    st.dataframe(top_gainers)
    fig2, ax2 = plt.subplots()
    ax2.bar(top_gainers['FCLICODE'], top_gainers['End Balance'])
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    tick_positions = ax2.get_xticks()
    tick_labels = top_gainers['FCLICODE'].iloc[:len(tick_positions)]
    ax2.set_xticklabels(tick_labels, rotation=90)
    st.pyplot(fig2)

def show_client_analysis():
    st.header('Client Analysis')
    
    # Filter for FCLICODE
    fclico_options = df['FCLICODE'].unique()
    fclico_filter = st.multiselect('Filter by FCLICODE', options=fclico_options, default=None)
    
    if fclico_filter:
        filtered_df = df[df['FCLICODE'].isin(fclico_filter)]
        st.dataframe(filtered_df)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        for fclico in fclico_filter:
            client_data = filtered_df[filtered_df['FCLICODE'] == fclico]
            ax.plot(client_data.index, client_data['End Balance'], label=fclico)
        
        ax.set_xlabel('Index')
        ax.set_ylabel('End Balance')
        ax.set_title('End Balance per Client')
        ax.legend(title='FCLICODE')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info('No FCLICODE selected. Displaying total End Balance per Category.')
        total = df.groupby('Category')['End Balance'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(total['Category'], total['End Balance'], marker='o')
        ax.set_xlabel('Category')
        ax.set_ylabel('Total End Balance')
        ax.set_title('Total End Balance by Category')
        plt.xticks(rotation=45)
        st.pyplot(fig)

# Sidebar for navigation
page = st.sidebar.selectbox("Select Page", ["Top Losers", "Top Gainers", "Client Analysis"])

if page == "Top Losers":
    show_top_losers()
elif page == "Top Gainers":
    show_top_gainers()
elif page == "Client Analysis":
    show_client_analysis()