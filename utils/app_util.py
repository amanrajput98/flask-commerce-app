import pandas as pd


def load_and_clean_data(csv_file_path):
    """Loads input csv to dataframe and transform & clean data before 
    loading into DB"""
    df = pd.read_csv(csv_file_path)
    
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['price'].fillna(df['price'].median(), inplace=True)
    df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
    df['rating'] = df.groupby('category')['rating'].apply(lambda x: x.fillna(x.mean()))
    
    return df