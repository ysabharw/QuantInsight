from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", title="QuantInsight - Financial Market Analysis")

@app.route("/stocks", methods=["GET", "POST"])
def stocks():
    if request.method == "POST":
        # Get the ticker symbol from the form
        ticker = request.form.get("ticker")
        if ticker:
            try:
                # Debug message to log the ticker being fetched
                print(f"Fetching data for ticker: {ticker}")
                
                # Fetch stock data
                data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
                
                # Debug message to show the first few rows of data
                print(data.head())
                
                # Handle empty data (invalid ticker or no data)
                if data.empty:
                    return render_template(
                        "stocks.html",
                        title="Stock Data",
                        error="Invalid ticker symbol. Please try again.",
                        ticker=None,
                    )
                
                # Extract relevant data (dates and closing prices)
                prices = data['Close'].tolist()
                dates = data.index.strftime('%Y-%m-%d').tolist()
                
                # Render the template with stock data
                return render_template(
                    "stocks.html",
                    title="Stock Data",
                    ticker=ticker,
                    prices=prices,
                    dates=dates,
                )
            except Exception as e:
                # Log any errors that occur
                print(f"Error fetching data for ticker {ticker}: {e}")
                return render_template(
                    "stocks.html",
                    title="Stock Data",
                    error="An error occurred while fetching stock data. Please try again.",
                    ticker=None,
                )
    
    # Default behavior for GET requests (display the form)
    return render_template("stocks.html", title="Stock Data", ticker=None)

if __name__ == "__main__":
    app.run(debug=True)
