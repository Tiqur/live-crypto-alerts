class Ohlvc():
    def __init__(self, data):
        self.start_time = data[0]
        self.open = float(data[1])
        self.high = float(data[2])
        self.low = float(data[3])
        self.close = float(data[4])
        self.volume = float(data[5])
        self.end_time = float(data[6])

    
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
