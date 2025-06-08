import matplotlib.pyplot as plt

def create_plot(df, stock):
    plt.figure(figsize=(10, 5))
    plt.plot(df["ds"], df["yhat"], marker='o', linestyle='-', color='blue')
    plt.title(f"Forecast for {stock}")
    plt.xlabel("Date")
    plt.ylabel("Predicted Price")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/forecast.png")
    plt.close()
