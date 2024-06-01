import logging
from decimal import Decimal
from datetime import datetime
from django.db import connection

def aggregate_bars(tickers, start_timestamp, end_timestamp, interval):
    interval_mapping = {
        's': 'strftime("%Y-%m-%d %H:%M:%S", mdb.timestamp / 1000000000, "unixepoch")',
        'm': 'strftime("%Y-%m-%d %H:%M", mdb.timestamp / 1000000000, "unixepoch")',
        'h': 'strftime("%Y-%m-%d %H", mdb.timestamp / 1000000000, "unixepoch")',
        'd': 'date(mdb.timestamp / 1000000000, "unixepoch")'
    }

    if interval not in interval_mapping:
        raise ValueError("Invalid interval. Choose from 's', 'm', 'h', 'd'.")

    interval_expression = interval_mapping[interval]
    tickers_placeholder = ','.join(['%s'] * len(tickers))

    query = f"""
    WITH InitialValues AS (
        SELECT
            mdb.symbol_id,
            s.ticker,
            {interval_expression} AS interval_time,
            mdb.open,
            mdb.high,
            mdb.low,
            mdb.close,
            mdb.volume,
            ROW_NUMBER() OVER (PARTITION BY mdb.symbol_id, {interval_expression} ORDER BY mdb.timestamp) AS row_num_open,
            ROW_NUMBER() OVER (PARTITION BY mdb.symbol_id, {interval_expression} ORDER BY mdb.timestamp DESC) AS row_num_close
        FROM
            market_data_bardata mdb
        JOIN
            symbols_symbol s ON mdb.symbol_id = s.id
        WHERE
            s.ticker IN ({tickers_placeholder})
            AND mdb.timestamp BETWEEN %s AND %s
    ),
    DailyData AS (
        SELECT
            symbol_id,
            ticker,
            interval_time,
            (SELECT open FROM InitialValues iv WHERE iv.symbol_id = InitialValues.symbol_id AND iv.interval_time = InitialValues.interval_time AND iv.row_num_open = 1) AS open,
            MAX(high) AS high,
            MIN(low) AS low,
            (SELECT close FROM InitialValues iv WHERE iv.symbol_id = InitialValues.symbol_id AND iv.interval_time = InitialValues.interval_time AND iv.row_num_close = 1) AS close,
            SUM(volume) AS volume
        FROM
            InitialValues
        GROUP BY
            symbol_id,
            ticker,
            interval_time
    )
    SELECT
        symbol_id,
        ticker,
        interval_time,
        open,
        high,
        low,
        close,
        volume
    FROM
        DailyData
    ORDER BY
        interval_time;
    """

    params = tickers + [start_timestamp, end_timestamp]

    with connection.cursor() as cursor:
        cursor.execute(query,  params)
        results = cursor.fetchall()

        # Convert results to list of dictionaries with correct types
        columns = [col[0] for col in cursor.description]
        results = [
            {
                'symbol_id': row[0],
                'ticker': row[1],
                'timestamp': int(datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').timestamp() * 1000000000) if interval != 'd' else int(datetime.strptime(row[2], '%Y-%m-%d').timestamp() * 1000000000),
                'open': Decimal(row[3]),
                'high': Decimal(row[4]),
                'low': Decimal(row[5]),
                'close': Decimal(row[6]),
                'volume': int(row[7])
            }
            for row in results
        ]

        return results


# ADD INTO BarDataViewSet
@action(detail=False, methods=['get'], url_path='aggregate-bars')
def aggregate_bars(self, request, *args, **kwargs):
    tickers = request.query_params.get('tickers')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    interval = request.query_params.get('interval', 'd').lower()

    # Validate tickers
    if not tickers:
        raise ValidationError("Tickers parameter is required.")
    ticker_list = tickers.split(',')

    # Validate start_date and end_date
    try:
        start_date = int(start_date)
        end_date = int(end_date)
    except (TypeError, ValueError):
        raise ValidationError("Start date and end date must be valid Unix timestamps.")

    # Validate interval
    if interval not in ['s', 'm', 'h', 'd']:
        raise ValidationError("Interval must be one of 's', 'm', 'h', or 'd'.")

    # Call the aggregate_bars function
    try:
        results = aggregate_bars(ticker_list, start_date, end_date, interval)
    except Exception as e:
        logger.error(f"Error in aggregate_bars: {e}")
        raise ValidationError("An error occurred while aggregating bars.")

    return Response(results)