from flask import Flask, render_template, request
from datetime import datetime
from stocks import StockAnalyzer

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        ticker = request.form.get('ticker')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Validate inputs
        if not all([ticker, start_date, end_date]):
            return render_template('index.html',
                                   error_msg="Please fill in all fields")

        try:
            # Create StockAnalyzer instance
            analyzer = StockAnalyzer(ticker, start_date, end_date)

            # Fetch stock data
            stock_data, error = analyzer.fetch_stock_data()
            if error:
                return render_template('index.html', error_msg=error)

            # Make predictions
            predictions, pred_error = analyzer.make_predictions()
            if pred_error:
                return render_template('index.html',
                                       stock_data=stock_data,
                                       error_msg=pred_error)

            return render_template('index.html',
                                   stock_data=stock_data,
                                   predictions=predictions)

        except Exception as e:
            return render_template('index.html',
                                   error_msg=f"An error occurred: {str(e)}")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)