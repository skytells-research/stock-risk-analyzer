import numpy as np
import pandas_ta as ta

def add_features(df):
    """
    Add technical indicators as features for the model.
    """
    # Basic features
    df['Daily Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Daily Return'].rolling(window=21).std() * np.sqrt(252)
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    
    # Additional technical indicators using pandas_ta
    df['RSI'] = df.ta.rsi(length=14)
    df['MACD'] = df.ta.macd(fast=12, slow=26, signal=9)['MACD_12_26_9']
    
    # Correct way to calculate Bollinger Bands
    bb_bands = df.ta.bbands(close=df['Close'], length=20)
    df['BB_upper'] = bb_bands['BBU_20_2.0']
    df['BB_middle'] = bb_bands['BBM_20_2.0']
    df['BB_lower'] = bb_bands['BBL_20_2.0']
    
    # Drop any NaN values that might have been created
    df = df.dropna()
    
    return df