import os
import traceback
import types
import datetime as dt

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
        'timestamp': int_or_none,
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


def import_csv(csv_path, batch=False, chunksize=500, skiprows=None):
    start_time = dt.datetime.today().timestamp()

    for df in pd.read_csv(csv_path, delimiter='\t', encoding='utf-8', dtype=dtype, converters=converters,
                          chunksize=chunksize, skiprows=skiprows, error_bad_lines=False, warn_bad_lines=True):

        print("transform")
        df = df.where((pd.notnull(df)), None)
        print("importing rows {} to {}".format(df.index.min(), df.index.max()))

        if batch:
            b = BatchQuery()

        for i, row in df.iterrows():
            try:
                print(u"DOING {} ; {}".format(i, row['code'].encode('utf-8')))

                if row['code'] is None or len(row['code'].strip()) == 0:
                    print("error with line {0} : code = '{1}'".format(i, row['code'].encode('utf-8')))
                    continue

                row_converted = {
                    Product._get_column_by_db_name(cql_name).column_name: value
                    for cql_name, value in row.items()
                    if not cql_name.endswith('_datetime')
                       and value is not None
                       and (type(value) != str or len(value) > 0)
                }

                product = Product.create(**row_converted)

                if not batch:
                    product.save()

                print(u"DONE {} ; {}".format(i, row['code'].encode('utf-8')))
            except Exception:
                print(u"EXCEPTION {} ; {}".format(i, row['code'].encode('utf-8')))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=10, file=sys.stderr)

        if batch:
            print("executing batch for rows {} to {}".format(df.index.min(), df.index.max()))
            b.execute()

        time_diff = dt.datetime.today().timestamp() - start_time
        print("TIMING {} rows/s".format(chunksize / time_diff))
        start_time = dt.datetime.today().timestamp()


if __name__ == '__main__':

    csv_path_or_url = os.environ.get('CSV_PATH_OR_URL', '../fr.openfoodfacts.org.products.csv')
    if csv_path_or_url.startswith("http://") or csv_path_or_url.startswith("https://"):
        print("downloading csv")
        csv_path_or_url = wget.download(csv_path_or_url, out="/tmp")

    start_from = os.environ.get('IMPORT_START_FROM', None)
    skiprows = range(1, int(start_from)) if start_from else None

    batch = os.environ.get("IMPORT_BATCH", "yes").lower() in ("yes", "true", "y", "t", "oui", "1")
    chunksize = int(os.environ.get("IMPORT_CHUNKSIZE", "500"))

    import_csv(csv_path_or_url, batch=batch, chunksize=chunksize, skiprows=skiprows)
