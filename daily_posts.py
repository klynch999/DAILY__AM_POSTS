import asyncio
import datetime
import io
import mysql.connector
import nest_asyncio
nest_asyncio.apply()
import numpy as np
import os
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import requests
import telegram
from sqlalchemy import create_engine
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telegram import InputMediaPhoto
from time import sleep

async def get_24h_stats(bot, chat_id):
    response = requests.get("https://api.coingecko.com/api/v3/global").json()
    dominance = round(float(response['data']['market_cap_percentage']['btc']), 2)

    response = requests.get('https://api.binance.com/api/v3/ticker/24hr').json()
    symbols = [t for t in response if
               any(t['symbol'] == s for s in ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT'])]
    message = "<b>24 Hour Stats:</b> \n \n"
    message += f"<b>BTC Dominance:</b> {dominance} \n (Coingecko.com) \n"
    for ticker in symbols:
        symbol = ticker['symbol']
        volatility = get_volatility(symbol.lower())
        pc = ticker['priceChangePercent']
        volume = ticker['volume']
        message += f"<b>{symbol} </b> \n"
        message += f"Price Change: {pc}% \n"
        message += f"Volume: {round(float(volume), 2)} \n"
        message += f"Volatility: {volatility}% \n \n"
    await bot.sendMessage(chat_id=chat_id, text=message, parse_mode="HTML")

    # Filter out non-BTC pairs and sort by price change percentage
    tickers_usdt = [t for t in response if t['symbol'].endswith('USDT')]
    tickers_usdt_sorted = sorted(tickers_usdt, key=lambda t: float(t['priceChangePercent']), reverse=True)

    # Print top 5 movers
    message = "<b>Top ten gainers 24h:</b> \n \n"
    for ticker in tickers_usdt_sorted[:10]:
        symbol = ticker['symbol']
        price_change_percent = ticker['priceChangePercent']
        message += f"<b>{symbol}:</b> {price_change_percent}% \n"

    await bot.sendMessage(chat_id=chat_id, text=message, parse_mode="HTML")

    tickers_usdt_sorted = sorted(tickers_usdt, key=lambda t: float(t['priceChangePercent']), reverse=False)
    message = "<b>Top ten losers 24h:</b> \n \n"
    for ticker in tickers_usdt_sorted[:10]:
        symbol = ticker['symbol']
        price_change_percent = ticker['priceChangePercent']
        message += f"<b>{symbol}:</b> {price_change_percent}% \n"

    await bot.sendMessage(chat_id=chat_id, text=message, parse_mode="HTML")

async def get_fg_screenshots_cnn(bot, chat_id):
    media_group = []

    PATH = PATH_TO_DRIVER
    url = "https://edition.cnn.com/markets/fear-and-greed?utm_source=business_ribbon"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    chrome_options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(service=Service(PATH), options=chrome_options)

    driver.get(url)
    sleep(5)

    element = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    element.click()
    sleep(5)

    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[1]/div[2]/div[1]/div")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    sleep(3)
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[3]/div[3]/div[1]")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    sleep(3)
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[4]/div[3]/div[1]")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    sleep(3)
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[5]/div[3]/div[1]")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    sleep(3)
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[6]/div[3]/div[1]")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    sleep(3)
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[7]/div[3]/div[1]")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    sleep(3)
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[8]/div[3]/div[1]")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    sleep(3)
    element = driver.find_element(By.XPATH,
                                  "/html/body/div[1]/section[3]/section[1]/section[1]/div/section/div[9]/div[3]/div[1]")
    screenshot = element.screenshot_as_png
    image_stream = BytesIO(screenshot)
    im = Image.open(image_stream)
    w, h = im.size
    new_width = int(w * 2)
    new_height = int(h * 2)
    resized_image = im.resize((new_width, new_height))
    image_stream2 = BytesIO()
    resized_image.save(image_stream2, format='PNG')
    image_bytes = image_stream2.getvalue()
    media = InputMediaPhoto(image_bytes)
    media_group.append(media)

    # Close the browser
    driver.quit()
    sleep(3)
    # Send the media group to the chat
    await bot.send_media_group(chat_id=chat_id,
                               media=media_group,
                               caption="Here is the daily Fear and Greed Index for stocks from CNN Money:")

def get_volatility(symbol):

    # Set up connection to database
    connection = mysql.connector.connect(
        user=?
        password=?
        host=?
        database=?
    )

    # Create cursor object and execute query
    cursor = connection.cursor()
    query = f"SELECT * FROM {symbol} ORDER BY timestamp DESC LIMIT {30 * 1440}"
    cursor.execute(query)

    # Fetch data and store in pandas dataframe
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[col[0] for col in cursor.description])
    
     # Convert time column to datetime
    df['timestamp'] = pd.to_datetime(df['close_time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['close_time'], unit='ms')
    df = df.set_index('timestamp')

    start_time = df.index.min()
    end_time = df.index.max()
    all_times = pd.date_range(start=start_time, end=end_time, freq='1min')
    all_data = pd.DataFrame(index=all_times)

    merged_data = pd.merge(all_data, df, how='outer', left_index=True, right_index=True)
    df = merged_data.fillna(method='ffill')

    daily_data = df.resample('1D').agg({
        'open_price': 'first',
        'high_price': 'max',
        'low_price': 'min',
        'close_price': 'last',
        'Close Time': 'last',
        'volume': 'sum'
    })

    daily_data['return'] = daily_data['close_price'].pct_change()

    # Compute and round volatility
    volatility = np.std(daily_data['return']) * 100
    volatility = round(volatility, 2)

    # Clean up resources
    cursor.close()
    connection.close()

    return volatility

async def fear_and_greed_crypto(bot, chat_id):
    caption = "Here is the updated Fear and Greed Index. Data sourced from: https://alternative.me/crypto/fear-and-greed-index/"

    y = []
    x = []
    z = []

    url = r"https://api.alternative.me/fng/?limit=28"
    response = requests.get(url)
    data = response.json()
    for entry in data['data']:
        _class = entry['value_classification']
        z.append(_class)
        val = entry['value']
        y.append(float(val))
        ts = entry['timestamp']
        date = dt_object = datetime.datetime.fromtimestamp(int(ts))
        x.append(date)

    trace = go.Scatter(

        x=x,
        y=y,
        mode='lines'

    )

    most_recent_value = int(y[0])
    if z[0] == "Extreme Greed":
        color = "dark red"
    elif z[0] == "Greed":
        color = "red"
    elif z[0] == "Neutral":
        color = "black"
    elif z[0] == "Fear":
        color = "green"
    elif z[0] == "Extreme Fear":
        color = "dark green"

    annotation = go.layout.Annotation(
        x=x[0], y=y[0],
        text=f"<b>{most_recent_value} {z[0]}</b>",
        showarrow=True, arrowhead=7, ax=-50, ay=-50,
        font=dict(
            family='Arial',
            size=22,
            color='red',
        )
    )

    layout = go.Layout(
        height=600,
        width=900,
        yaxis=dict(range=[0, 100], showgrid=True),
        xaxis=dict(showgrid=False),

        title={
            'text': '<b>Fear and Greed Index</b>',
            'x': 0.5,
            'y': .93,
            'font': {'size': 24, 'family': 'Arial', 'color': 'black'}
        },
        annotations=[annotation]
    )

    fig = go.Figure(layout=layout)
    fig.add_trace(trace)
    png_bytes = io.BytesIO()
    fig.write_image(png_bytes, format="png")
    png_bytes.seek(0)
    await bot.send_photo(chat_id=chat_id, photo=png_bytes, caption=caption)

bot = telegram.Bot(token=?)
chat_id = ?

async def main():
    await asyncio.gather(get_24h_stats(bot, chat_id),
                         get_fg_screenshots_cnn(bot, chat_id),
                        fear_and_greed_crypto(bot, chat_id))

# Run the main async function
if __name__ == '__main__':
    asyncio.run(main())
