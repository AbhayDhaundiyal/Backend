import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Connection Engine
engine = create_engine('sqlite:///task.db')

# Fetching Data From The Database
unfiltered_df = pd.read_sql_query("Select * from 'HINDALCO_1D.xlsx' where instrument like 'HINDALCO'", con=engine)

# Creating A Filtered Dataframe
df = pd.DataFrame({'date' : unfiltered_df['datetime'], 'close' : unfiltered_df['close']})

#####  Applying SMA(short-term/long-term fluctuations) ####
df['20_SMA'] = ((unfiltered_df['close'] + unfiltered_df['open'] + unfiltered_df['high'] + unfiltered_df['low'])/4).rolling(window=20, min_periods=1).mean()
df['50_SMA'] = ((unfiltered_df['close'] + unfiltered_df['open'] + unfiltered_df['high'] + unfiltered_df['low'])/4).rolling(window=50, min_periods=1).mean()
#########################

########## Plotting The Data ###########
df.plot(x = 'date')
df['close'].plot(color = 'dimgrey') 
df['20_SMA'].plot(color = 'crimson') 
df['50_SMA'].plot(color = 'gold')
df['signal'] = 0.0
df['signal'] = np.where(df['20_SMA'] > df['50_SMA'], 1.0, 0.0)
df['Position'] = df['signal'].diff()


# Buy Marker
plt.plot(df[df['Position'] == 1].index, 
         df['20_SMA'][df['Position'] == 1], 
         '^', markersize = 8, color = 'g', label = 'buy')

#Sell Marker
plt.plot(df[df['Position'] == -1].index, 
         df['20_SMA'][df['Position'] == -1], 
         'v', markersize = 8, color = 'r', label = 'sell')

plt.ylabel('Price in Rupees', fontsize = 15 )
plt.xlabel('Date', fontsize = 15)
plt.title('HINDALCO', fontsize = 20)
plt.legend()
plt.grid()
plt.show()
#################################################### END #############################################