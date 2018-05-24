
import pandas as pd
from meetup import database
from meetup.models import Product


database.init()

dtype = {
    'code': str,
    'url': str,
    'product_name': str
}

for df in pd.read_csv('fr.openfoodfacts.org.products.csv',
                      delimiter='\t', encoding='utf-8', dtype=dtype, chunksize=500):
    print("transform")
    df = df.where((pd.notnull(df)), None)
    print("importing rows {} to {}".format(df.index.min(), df.index.max()))
    for i, row in df.iterrows():
        try:
            print(i, row['code'], ";", row['url'], ";", row['product_name'])

            if row['code'] is None or len(row['code'].strip()) == 0:
                print("error with line {0} : code = '{1}'".format(i, row['code']))
                continue

            product = Product.create(
                code=row['code'],
                url=row['url'],
                product_name=row['product_name']
            )
        except UnicodeEncodeError as err:
            print("UnicodeEncode error: {}".format(err))

    print("executing batch for rows {} to {}".format(df.index.min(), df.index.max()))
