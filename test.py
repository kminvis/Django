from fbprophet import Prophet
import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download("AAPL", start = '2022-01-01')

data = data.rename(columns={'Close':'y'})
data['ds'] = data.index 
data = data[['ds', 'y']]

m = Prophet(daily_seasonality = True)
m.fit(data)

future = m.make_future_dataframe(periods=10)
prediction = m.predict(future)

fig = plt.figure(figsize=(10, 6))
plt.plot(data['ds'], data['y'], label='price', color="black")
plt.plot(prediction['ds'], prediction['yhat'], label='prediction', color="red")
plt.plot(prediction['ds'], prediction['yhat_lower'], color="red")
plt.plot(prediction['ds'], prediction['yhat_upper'], color="red")

fig