import pandas as pd

dtype = {
    'code': str,
    'url': str,
    'product_name': str
}

for df in pd.read_csv('fr.openfoodfacts.org.products.csv',
                      delimiter='\t', encoding='utf-8', dtype=dtype, chunksize=5000):

    df = df.where((pd.notnull(df)), None)
    df.to_csv("converted.fr.openfoodfacts.org.products.csv", header=df.index.min() == 0)
