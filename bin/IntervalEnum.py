MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24

map = {
        '1m'  : MINUTE,
        '3m'  : MINUTE * 3,
        '5m'  : MINUTE * 5,
        '15m' : MINUTE * 15,
        '30m' : MINUTE * 30,
        '1h'  : HOUR,
        '2h'  : HOUR * 2,
        '4h'  : HOUR * 4,
        '6h'  : HOUR * 6,
        '8h'  : HOUR * 8,
        '12h' : HOUR * 12,
        '1d'  : DAY,
        '3d'  : DAY * 3,
        '1w'  : DAY * 7,
        '1M'  : DAY * 30
    }


def interval_to_sec(interval):
    return map[interval]
