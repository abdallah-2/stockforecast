import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta


class StockAnalyzer:
    def __init__(self, ticker, start_date, end_date):
        """Initialize with stock parameters"""
        self.ticker = ticker.upper()
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def fetch_stock_data(self):
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(self.ticker)
            self.data = stock.history(start=self.start_date, end=self.end_date)

            if self.data.empty:
                return None, "No data found for the specified ticker and date range"

            # Reset index to make Date a column
            self.data = self.data.reset_index()

            # Drop unnecessary columns
            self.data = self.data.drop(['Dividends', 'Stock Splits'], axis=1)

            # Format the date column
            self.data['Date'] = self.data['Date'].dt.strftime('%Y-%m-%d')

            # Add ticker column right after date
            self.data.insert(1, 'Ticker', self.ticker)

            # Round all numeric columns to 2 decimal places
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            self.data[numeric_columns] = self.data[numeric_columns].round(2)

            # Convert to HTML with bootstrap classes and proper spacing
            html_table = self.data.to_html(
                classes=['table', 'table-striped', 'table-hover', 'table-bordered'],
                index=False,
                justify='center'
            )

            # Add custom CSS for table formatting
            html_table = f"""
            <style>
                .table {{
                    width: 100%;
                    margin-bottom: 1rem;
                    text-align: center;
                }}
                .table th {{
                    background-color: #f8f9fa;
                    text-align: center;
                    padding: 12px;
                }}
                .table td {{
                    padding: 12px;
                }}
            </style>
            {html_table}
            """

            return html_table, None

        except Exception as e:
            return None, f"Error fetching stock data: {str(e)}"

    def make_predictions(self, days=5):
        """Generate ARIMA predictions"""
        try:
            if self.data is None:
                return None, "No data available for predictions"

            # Use 'Close' prices for predictions
            close_prices = self.data['Close'].values

            # Fit ARIMA model
            model = ARIMA(close_prices, order=(5, 1, 0))
            model_fit = model.fit()

            # Make predictions
            forecast = model_fit.forecast(steps=days)

            # Create dates for predictions
            last_date = datetime.strptime(self.data['Date'].iloc[-1], '%Y-%m-%d')
            future_dates = [(last_date + timedelta(days=i + 1)).strftime('%Y-%m-%d')
                            for i in range(days)]

            # Create prediction DataFrame
            pred_df = pd.DataFrame({
                'Date': future_dates,
                'Ticker': self.ticker,  # Add ticker to predictions too
                'Predicted Close': forecast.round(2)
            })

            # Convert to HTML with bootstrap classes and proper spacing
            html_table = pred_df.to_html(
                classes=['table', 'table-striped', 'table-hover', 'table-bordered'],
                index=False,
                justify='center'
            )

            # Add custom CSS for table formatting
            html_table = f"""
            <style>
                .table {{
                    width: 100%;
                    margin-bottom: 1rem;
                    text-align: center;
                }}
                .table th {{
                    background-color: #f8f9fa;
                    text-align: center;
                    padding: 12px;
                }}
                .table td {{
                    padding: 12px;
                }}
            </style>
            {html_table}
            """

            return html_table, None

        except Exception as e:
            return None, f"Error making predictions: {str(e)}"