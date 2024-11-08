def preprocess_data(df):
    """
    Preprocess the stock data by handling missing values and resetting the index.
    Args:
        df (pd.DataFrame): Raw stock data.
    Returns:
        pd.DataFrame: Preprocessed stock data.
    """
    try:
        df = df.dropna()  # Remove missing values
        df.reset_index(inplace=True)  # Reset index
        return df
    except Exception as e:
        raise ValueError(f"Error during preprocessing: {e}")
