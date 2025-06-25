import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class railway:
    distance = {
        ("Dimapur","Malda Town"): 900,
        ("Dimapur","Patna"): 1200,
        ("Dimapur","Kolkata"): 1300,
        ("Dimapur","Delhi"): 1800,
        ("Kolkata", "Delhi"): 1000,
        ("Kolkata", "Patna"): 600
    }

    classes = {
        "SL":0.6,
        "AC": 1.4,
        "GEN": 0.3,
        "SLEEPER":0.6,
        "GENERAL": 0.3

}



    def __init__(self,train_class,train_no,date,source_station,destination_station):
        self.train_class = train_class
        self.train_no = train_no
        self.date = date
        self.source_station = source_station
        self.destination_station = destination_station
        self.pnr = self.generatepnr()
        self.passenger = []
        # self.fare = []

    def addpassenger(self,name,gender,age):
        coachno = self.coach()
        seatno = self.seat()
        eachfare = self.getfare()
        self.passenger.append((name,gender,age,coachno,seatno,eachfare))
        print(self.passenger)



    def generatepnr(self):
        return f"PNR{random.randint(1000000,9999999)}"

    def coach(self):
        sl = random.randint(1,9)
        return "S"+str(sl)

    def seat(self):
        a = random.randint(0,72)
        if a%2 == 0:
            s = "L"
        elif a%3 == 0:
            s = "M"
        elif a%5 == 0:
            s = "U"
        elif a%7 == 0:
            s = "SL"
        else:
            s = "SU"
        return f"{str(a)} {s}"


    def getfare(self):
        route = (self.source_station, self.destination_station)
        reverse_route = (self.destination_station, self.source_station)
        passesnger_coach = self.train_class.upper()
        distance = 0
        if route in railway.distance:
            distance = railway.distance[route]
        elif reverse_route in railway.distance:
            distance = railway.distance[route]
        else:
            distance = 200 #For any unknown distance

        if passesnger_coach in railway.classes:
            rate = railway.classes[passesnger_coach]

        else:
            rate = railway.classes.get(passesnger_coach,0.6)
        return  distance * rate


    def display(self):
        print(f'''
                PNR: {self.pnr} | Date of Journey: {self.date}
                Train no: {self.train_no} | Class: {self.train_class}
                From: {self.source_station} to {self.destination_station}
              ''')

        for i,p in enumerate(self.passenger, start = 1):
            name,gender,age,coachno,seatno,eachfare = p
            print(f"{i}. {name} ({age} {gender}) | Coach: {coachno} Seat: {seatno} | Fare: ₹{eachfare}")



    def store(self):
        with open("ticket.txt", "a") as f:
            for p in self.passenger:
                name, gender, age, coachno, seatno, eachfare = p
                f.write(f"{self.pnr},{name},{age},{gender},{self.train_class},{coachno},{seatno},{self.train_no},{self.date},{self.source_station},{self.destination_station},{eachfare}\n")


    def save_ticket_txt(self):
        filename = f"{self.pnr}.txt"
        with open(filename, "w") as f:
            f.write(f"PNR: {self.pnr}\n")
            f.write(f"Date of Journey: {self.date}\n")
            f.write(f"Train no: {self.train_no} | Class: {self.train_class}\n")
            f.write(f"From: {self.source_station} to {self.destination_station}\n")
            f.write("Passenger Details:\n")
            for i, p in enumerate(self.passenger, start=1):
                name, gender, age, coachno, seatno, eachfare = p
                f.write(f"{i}. {name} ({age} {gender}) | Coach: {coachno} | Seat: {seatno} | Fare:{eachfare}\n")
        print(f"Ticket saved as {filename}")





    @staticmethod
    def searchbypnr():
        found = False
        pnr2 = str(input("Enter PNR to search: ")).strip().upper()
        with open("ticket.txt", "r") as f:
            i = 1
            for line in f:
                data = line.split(",")
                if data[0].strip().upper() == pnr2:
                    print(f'''

                PNR: {data[0]}
                Passenger Name: Passenger {i}
                Age and Gender(M/F): {data[2]} {data[3]}
                Train no: {data[7]}
                Class: {data[4]}
                Date of Journey: {data[8]}
                From: {data[9]} to {data[10]}
                Coach: {data[5]} {data[6]}
                Fare: {data[11]}

                          ''')
                    found = True
                    i += i
                    continue

        if found == False:
            print("No such Booking....")




    def save_ticket_pdf(self):
        filename = f"{self.pnr}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        y = height - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"PNR: {self.pnr}")
        y -= 30
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Date of Journey: {self.date}")
        y -= 20
        c.drawString(50, y, f"Train no: {self.train_no} | Class: {self.train_class}")
        y -= 20
        c.drawString(50, y, f"From: {self.source_station} to {self.destination_station}")
        y -= 30
        c.drawString(50, y, "Passenger Details:")

        for i, p in enumerate(self.passenger, start=1):
            name, gender, age, coachno, seatno, fare = p
            y -= 20
            c.drawString(60, y, f"{i}. {name} ({age} {gender}) | Coach: {coachno} | Seat: {seatno} | Fare: {fare}")

        c.save()
        print(f"Ticket saved as {filename}")


while True:
    print('''
\n🚆 Railway Ticketing System
----------------------------------------------------------------------------
1. Book Ticket
2. Search Ticket by PNR
3. Exit
        ''')
    ask = int(input("Enter your Choice: "))
    if ask == 2:
        railway.searchbypnr()
    elif ask == 1:
        train_class = input("Enter the Train Class: ")
        train_no = input("Enter the train number: ")
        date = input("Enter the date of journey: ")
        source_station = input("Enter the source station: ")
        destination_station = input("Enter the destination station: ")
        passenger = railway(train_class,train_no,date,source_station,destination_station)
        while True:
            name = input("Enter the passesnger name: ")
            gender = input("Enter the Gender: ")
            age = input("Enter the passesnger age: ")
            passenger.addpassenger(name,gender,age)
            more = input("Add more passengers? (y/n): ")
            if more.lower() != 'y':
                break
        passenger.display()
        passenger.store()
        passenger.save_ticket_txt()
        passenger.save_ticket_pdf()

    else:
        break

