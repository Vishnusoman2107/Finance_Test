import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Function to get S&P 500 stock symbols
def get_sp500_symbols():
    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    table = data[0]
    return table['Symbol'].tolist()

# Main Streamlit app code
def main():
    st.title('Stock Dashboard')

    # Dropdown to select the stock ticker symbol
    sp500_symbols = get_sp500_symbols()
    ticker = st.sidebar.selectbox('Select Ticker', sp500_symbols)

    # Input for start date and end date
    start_date = st.sidebar.text_input('Start Date (dd/mm/yyyy)')
    end_date = st.sidebar.text_input('End Date (dd/mm/yyyy)')

    # Convert date format to yyyy-mm-dd for yfinance
    try:
        start_date = pd.to_datetime(start_date, format='%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date, format='%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        st.sidebar.error('Invalid date format. Use dd/mm/yyyy.')

    if start_date and end_date:
        # Fetch historical stock price data using yfinance
        df = yf.download(ticker, start=start_date, end=end_date)

        # Plotting the stock price data using plotly
        if not df.empty:
            st.write(f"## Historical Stock Prices for {ticker}")
            fig = px.line(df, x=df.index, y='Close', title=f'{ticker} Close Price')
            fig.update_xaxes(title='Date')
            fig.update_yaxes(title='Close Price')
            st.plotly_chart(fig)
        else:
            st.sidebar.warning('No data available for the selected date range.')

if __name__ == '__main__':
    main()
