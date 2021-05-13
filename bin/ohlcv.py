from decimal import Decimal


class Ohlvc():
    def __init__(self, data):
        self.start_time = Decimal(data[0])
        self.open = Decimal(data[1])
        self.high = Decimal(data[2])
        self.low = Decimal(data[3])
        self.close = Decimal(data[4])
        self.volume = Decimal(data[5])
        self.end_time = Decimal(data[6])

    
    def __repr__(self):
        return(f"""

-------OHLVC--------
Start Time: {self.start_time}
End Time: {self.end_time}
Open: {self.open}
High: {self.high}
Low: {self.low}
Close: {self.close}
Volume: {self.volume}""")
