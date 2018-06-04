import os
import traceback
import types

import pandas as pd
import sys
import wget
from cassandra.cqlengine.query import BatchQuery

from meetup import database
from meetup.models import Product

database.init()


def int_or_none(s):
    try:
        x = int(s)
        return x
    except ValueError:
        return None


def list_of_text(s):
    if len(s) == 0:
        return []
    else:
        return [e.strip() for e in s.split(",")]


def create_dtype_and_converters():
    dtype, converters = {}, {}
    cql_to_types_or_converters = {
        'text': str,
        'timestamp': int,
        'double': float,
        'int': int_or_none,
        'list<text>': list_of_text
    }
    for column_name, column in Product._columns.items():
        cql_column_name = column.db_field_name
        cql_type = column.db_type
        type_or_converter = cql_to_types_or_converters[cql_type]

        if isinstance(type_or_converter, types.FunctionType):
            converters[cql_column_name] = type_or_converter
        else:
            dtype[cql_column_name] = type_or_converter

    return dtype, converters


dtype, converters = create_dtype_and_converters()


def import_csv(csv_path, batch=False, chucksize=500):
    for df in pd.read_csv(csv_path, delimiter='\t', encoding='utf-8', dtype=dtype, converters=converters,
                          chunksize=chucksize):
        print("transform")
        df = df.where((pd.notnull(df)), None)
        print("importing rows {} to {}".format(df.index.min(), df.index.max()))

        if batch:
            b = BatchQuery()

        for i, row in df.iterrows():
            try:
                print(i, row['code'], ";", row['url'], ";", row['product_name'])

                if row['code'] is None or len(row['code'].strip()) == 0:
                    print("error with line {0} : code = '{1}'".format(i, row['code']))
                    continue

                row_converted = {
                    Product._get_column_by_db_name(cql_name).column_name: value
                    for cql_name, value in row.items()
                    if
                    not cql_name.endswith('_datetime') and value is not None and (type(value) != str or len(value) > 0)
                }

                product = Product.create(**row_converted)

                if not batch:
                    product.save()

            except Exception as err:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=10, file=sys.stderr)

        if batch:
            print("executing batch for rows {} to {}".format(df.index.min(), df.index.max()))
            b.execute()


if __name__ == '__main__':
    csv_path_or_url = os.environ.get('CSV_PATH_OR_URL', 'fr.openfoodfacts.org.products.csv')

    if csv_path_or_url.startswith("http://") or csv_path_or_url.startswith("https://"):
        print("downloading csv")
        csv_path_or_url = wget.download(csv_path_or_url, out="/tmp")

    import_csv(csv_path_or_url)
