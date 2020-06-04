from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch as INCH
from datetime import datetime as DateTime, timedelta as TimeDelta
from typing import List

class Rider:
    def __init__(self, name: str = '', addr1: str = '', addr2: str = '', city: str = '',
            prov: str = '', country: str = '', postal: str = '', phone: str = '', email: str = ''):
        self.name = name
        self.addr1 = addr1
        self.addr2 = addr2
        self.city = city
        self.prov = prov
        self.country = country
        self.postal = postal
        self.phone = phone
        self.email = email

    def __str__(self):
        return f'Rider {self.name} from {self.city}, {self.prov if self.prov else self.country}'

class Control:
    # Determine open/close times for controls by a min/max speed
    # Open/close times are determined by total ride distance
    # Keep this list in ascending order by distance
    SPEED = [
        # { dist: km, min/max: kph }
        { 'dist': 200, 'min': 15, 'max': 100 / 3 }
    ]

    def __init__(self, distance: int = 0, location: str = '', establishment: str = ''):
        self.distance = distance
        self.location = location
        self.establishment = establishment

    def __str__(self):
        return f'{self.distance}: {self.establishment} ({self.location})'

    def _findSpeed(self, rideLength: int = 200) -> dict:
        # Find the appropriate speeds
        # Use the longest ride length that's below or equal to the given one
        speeds = Control.SPEED[0]
        for s in Control.SPEED:
            if s['dist'] > rideLength:
                break
            speeds = s
        return speeds
    
    def openTime(self, rideLength: int = 200) -> TimeDelta:
        speeds = self._findSpeed(rideLength)
        return TimeDelta(hours=self.distance / speeds['min'])

    def closeTime(self, rideLength: int = 200) -> TimeDelta:
        speeds = self._findSpeed(rideLength)
        return TimeDelta(hours=self.distance / speeds['max'])
        

class CardGen:
    def __init__(self, output: str):
        self.canvas = canvas.Canvas(output, pagesize=LETTER)
        self.width, self.height = LETTER
        # Using these as dev values, should be changed for production
        self.setRideInfo(0, '', '', DateTime.now())

    def setRideInfo(self, distance: int, rideName: str, brevetNo: str,
            start: DateTime, logo: str = None, controls: List[Control] = []) -> None:
        self.distance = distance
        self.ridename = rideName
        self.brevetNo = brevetNo
        self.logo = logo
        self.controls = controls
        # Only include up to hours in start time
        self.start = DateTime(start.year, start.month, start.day, hour=start.hour)

    def setControlList(self, controls: List[Control]) -> None:
        self.controls = controls

    def riderPage(self, rider: Rider) -> None:
        # ================= Card Front =======================
        # Image should be centered, and take up about 2/3 of the page width
        # Actual values are for 1/5 page width margin on either side, 0.9 inch top margin
        # Image height capped at 1.5 inches
        # Only print image if specified
        if self.logo:
            self.canvas.drawImage(self.logo, self.width / 5, self.height - INCH * 0.6,
                width=(self.width * 3 / 5),
                height=-(INCH * 1.5),
                preserveAspectRatio=True
            )
        # Print the "control card" text
        self.canvas.setFont("Helvetica", 36)
        self.canvas.drawCentredString(self.width / 2, self.height - INCH * 2.9, "Control Card")
        # Ride Name
        # Should be smaller text, centered, and italics
        self.canvas.setFont("Helvetica-Oblique", 16)
        self.canvas.drawCentredString(self.width / 2, self.height - INCH * 3.35, self.ridename)
        # Name, address: Title with single line
        self.canvas.setFont("Helvetica", 14)
        underline = "_______________________________________________"
        linespace = 0.4 * INCH
        topline = self.height - INCH * 4.1
        lmarg = INCH
        rmarg = self.width - INCH
        infoOffset = INCH * 1.5
        self.canvas.drawString(lmarg, topline, "Name") # Labels
        self.canvas.drawString(lmarg, topline - linespace, "Address")
        self.canvas.drawRightString(rmarg, topline, underline) # Lines
        self.canvas.drawRightString(rmarg, topline - linespace, underline)
        self.canvas.drawRightString(rmarg, topline - linespace * 1.8, underline)
        self.canvas.drawString(lmarg + infoOffset, topline + 2, rider.name) # Values
        self.canvas.drawString(lmarg + infoOffset, topline - linespace + 2, rider.addr1)
        self.canvas.drawString(lmarg + infoOffset, topline - linespace * 1.8 + 2, rider.addr2)
        # City, Province, Country, Postal Code, Phone, Email: Two columns
        topline = topline - linespace * 1.8
        shortline = "_______________"
        midmarg = INCH / 4.3
        self.canvas.drawString(lmarg, # Labels
                    topline - linespace,
                    "City")
        self.canvas.drawString(self.width / 2 + midmarg,
                    topline - linespace,
                    "Province/State")
        self.canvas.drawString(lmarg,
                    topline - linespace * 2,
                    "Country")
        self.canvas.drawString(self.width / 2 + midmarg,
                    topline - linespace * 2,
                    "Postal Code")
        self.canvas.drawString(lmarg,
                    topline - linespace * 3,
                    "Telephone")
        self.canvas.drawString(self.width / 2 + midmarg,
                    topline - linespace * 3,
                    "Email")
        self.canvas.drawRightString(rmarg, # Lines
                        topline - linespace,
                        shortline)
        self.canvas.drawRightString(self.width / 2 - midmarg,
                        topline - linespace,
                        shortline)
        self.canvas.drawRightString(rmarg,
                        topline - linespace * 2,
                        shortline)
        self.canvas.drawRightString(self.width / 2 - midmarg,
                        topline - linespace * 2,
                        shortline)
        self.canvas.drawRightString(rmarg,
                        topline - linespace * 3,
                        shortline + "_______")
        self.canvas.drawRightString(self.width / 2 - midmarg,
                        topline - linespace * 3,
                        shortline)
        self.canvas.drawString(lmarg + infoOffset, # Values
                    topline - linespace + 2,
                    rider.city)
        self.canvas.drawString(self.width / 2 + midmarg + infoOffset,
                    topline - linespace + 2,
                    rider.prov)
        self.canvas.drawString(lmarg + infoOffset,
                    topline - linespace * 2 + 2,
                    rider.country)
        self.canvas.drawString(self.width / 2 + midmarg + infoOffset,
                    topline - linespace * 2 + 2,
                    rider.postal)
        self.canvas.drawString(lmarg + infoOffset,
                    topline - linespace * 3 + 2,
                    rider.phone)
        self.canvas.drawRightString(rmarg,
                        topline - linespace * 3 + 2,
                        rider.email)
        # Static text
        self.canvas.setFont("Helvetica", 12)
        self.canvas.drawCentredString(self.width / 2, INCH * 4.4, "Founding member of LES RANDONNEURS MONDIAUX (1983)")
        self.canvas.drawCentredString(self.width / 2, INCH * 3.9, "Each Randonneur must carry a Control Card, have it signed at the control between the opening")
        self.canvas.drawCentredString(self.width / 2, INCH * 3.9 - 15, "and closing times, and return it to the organizer.")
        # Date, start/finish/elapsed times, signature line: Two columns, different sizes
        self.canvas.setFont("Helvetica", 14)
        topline = INCH * 3.9 - 40
        self.canvas.drawString(lmarg, topline, "Date   " + shortline)
        self.canvas.drawString(lmarg + INCH * 0.6,
                    topline + 2,
                    self.start.strftime("%B %d, %Y")) # Date value
        self.canvas.drawString(self.width / 2 - midmarg, topline, "Start time")
        self.canvas.drawString(self.width / 2 - midmarg,
                    topline - linespace,
                    "Finish Time")
        self.canvas.drawString(self.width / 2 - midmarg,
                    topline - linespace * 2,
                    "Elapsed Time")
        shortline = shortline + "_____"
        self.canvas.drawRightString(rmarg, topline, shortline)
        self.canvas.drawRightString(rmarg, topline - linespace, shortline)
        self.canvas.drawRightString(rmarg, topline - linespace * 2, shortline)
        self.canvas.drawString(lmarg, topline - linespace * 2, shortline)
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(lmarg,
                    topline - linespace * 2 - 12,
                    "Rider's signature at completion")
        # Stamp boxes
        self.canvas.drawCentredString(self.width / 2, INCH * 1.9, "Randonneur Committee Authorization")
        self.canvas.rect(self.width / 2, INCH * 1.9 - 5, -(INCH * 1.5), -INCH)
        self.canvas.rect(self.width / 2, INCH * 1.9 - 5, INCH * 1.5, -INCH)
        # Brevet No.
        self.canvas.drawRightString(self.width / 2 - 10, INCH * 0.5, "Brevet No.")
        if self.brevetNo == '':
            self.canvas.drawString(self.width / 2 + 10, INCH * 0.5, "__________")
        else:
            self.canvas.drawString(self.width / 2 + 10, INCH * 0.5, self.brevetNo)
        
        # Save the page
        self.canvas.showPage()

    def controlPage(self) -> None:
        # ==================== Card Back ========================
        # Headers
        tableData = [
            ["DIST (km)", "Open", "Close", "Locale",
                "Establishment", "Signature", "Time of Passage"]
        ]
        # Generate table of controls
        for control in self.controls:
            tableData.append([
                control.distance,
                (self.start + control.openTime(self.distance)).strftime('%A\n%I:%M %p\n%d/%b/%y'),
                (self.start + control.closeTime(self.distance)).strftime('%A\n%I:%M %p\n%d/%b/%y'),
                control.location,
                control.establishment,
                "", "" # Signature and Time to be filled manually
            ])
        # Draw on the canvas
        t = Table(tableData, repeatRows=1)
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND', (0,0), (-1,0), "#A0A0A0"),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), ['#FFFFFF','#F0F0F0'])
        ]))
        _, h = t.wrap(self.width - INCH, self.height - INCH)
        t.drawOn(self.canvas, INCH / 2, self.height - INCH / 2 - h)
        self.canvas.showPage()

    def printableList(self, riderList: List[Rider]) -> None:
        # Create an empty rider page that can be printed and filled manually
        self.riderPage(Rider())
        self.controlPage()
        for r in riderList:
            self.riderPage(r)
            # Uncomment if a control page should be printed for each rider
            # self.controlPage()
    
    def save(self) -> None:
        self.canvas.save()