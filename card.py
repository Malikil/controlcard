from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch as INCH
from datetime import datetime as DateTime, timedelta as TimeDelta

# Can define paragraph style stuff here, see chapter 5/6

def cardFront(c, width, height,
              description="", brevno="", start="",
              rider={'name':'',
                     'addr1': '',
                     'addr2': '',
                     'city': '',
                     'prov': '',
                     'country': '',
                     'post': '',
                     'phone': '',
                     'email': ''}):
    # ================= Card Front =======================
    # Image should be centered, and take up about 2/3 of the page width
    # Actual values are for 1/5 page width margin on either side, 1 inch top margin
    # Image height capped at 1.5 inches
    c.drawImage(".\\images\\logo.png", width / 5, height - INCH * 0.6,
        width=(width * 3 / 5),
        height=-(INCH * 1.5),
        preserveAspectRatio=True
    )
    # Print the "control card" text
    c.setFont("Helvetica", 36)
    c.drawCentredString(width / 2, height - INCH * 2.9, "Control Card")
    # Description
    # Should be smaller text, centered, and italics
    c.setFont("Helvetica-Oblique", 16)
    c.drawCentredString(width / 2, height - INCH * 3.35, description)
    # Name, address: Title with single line
    c.setFont("Helvetica", 14)
    underline = "_______________________________________________"
    linespace = 0.4 * INCH
    topline = height - INCH * 4.1
    lmarg = INCH
    rmarg = width - INCH
    infoOffset = INCH * 1.5
    c.drawString(lmarg, topline, "Name") # Labels
    c.drawString(lmarg, topline - linespace, "Address")
    c.drawRightString(rmarg, topline, underline) # Lines
    c.drawRightString(rmarg, topline - linespace, underline)
    c.drawRightString(rmarg, topline - linespace * 1.8, underline)
    c.drawString(lmarg + infoOffset, topline + 2, rider['name']) # Values
    c.drawString(lmarg + infoOffset, topline - linespace + 2, rider['addr1'])
    c.drawString(lmarg + infoOffset, topline - linespace * 1.8 + 2, rider['addr2'])
    # City, Province, Country, Postal Code, Phone, Email: Two columns
    topline = topline - linespace * 1.8
    shortline = "_______________"
    midmarg = INCH / 4.3
    c.drawString(lmarg, # Labels
                 topline - linespace,
                 "City")
    c.drawString(width / 2 + midmarg,
                 topline - linespace,
                 "Province/State")
    c.drawString(lmarg,
                 topline - linespace * 2,
                 "Country")
    c.drawString(width / 2 + midmarg,
                 topline - linespace * 2,
                 "Postal Code")
    c.drawString(lmarg,
                 topline - linespace * 3,
                 "Telephone")
    c.drawString(width / 2 + midmarg,
                 topline - linespace * 3,
                 "Email")
    c.drawRightString(rmarg, # Lines
                      topline - linespace,
                      shortline)
    c.drawRightString(width / 2 - midmarg,
                      topline - linespace,
                      shortline)
    c.drawRightString(rmarg,
                      topline - linespace * 2,
                      shortline)
    c.drawRightString(width / 2 - midmarg,
                      topline - linespace * 2,
                      shortline)
    c.drawRightString(rmarg,
                      topline - linespace * 3,
                      shortline + "_______")
    c.drawRightString(width / 2 - midmarg,
                      topline - linespace * 3,
                      shortline)
    c.drawString(lmarg + infoOffset, # Values
                 topline - linespace + 2,
                 rider['city'])
    c.drawString(width / 2 + midmarg + infoOffset,
                 topline - linespace + 2,
                 rider['prov'])
    c.drawString(lmarg + infoOffset,
                 topline - linespace * 2 + 2,
                 rider['country'])
    c.drawString(width / 2 + midmarg + infoOffset,
                 topline - linespace * 2 + 2,
                 rider['post'])
    c.drawString(lmarg + infoOffset,
                 topline - linespace * 3 + 2,
                 rider['phone'])
    c.drawRightString(rmarg,
                      topline - linespace * 3 + 2,
                      rider['email'])
    # Static text
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, INCH * 4.4, "Founding member of LES RANDONNEURS MONDIAUX (1983)")
    c.drawCentredString(width / 2, INCH * 3.9, "Each Randonneur must carry a Control Card, have it signed at the control between the opening")
    c.drawCentredString(width / 2, INCH * 3.9 - 15, "and closing times, and return it to the organizer.")
    # Date, start/finish/elapsed times, signature line: Two columns, different sizes
    c.setFont("Helvetica", 14)
    topline = INCH * 3.9 - 40
    c.drawString(lmarg, topline, "Date   " + shortline)
    c.drawString(lmarg + INCH * 0.6,
                 topline + 2,
                 start.strftime("%B %d, %Y")) # Date value
    c.drawString(width / 2 - midmarg, topline, "Start time")
    c.drawString(width / 2 - midmarg,
                 topline - linespace,
                 "Finish Time")
    c.drawString(width / 2 - midmarg,
                 topline - linespace * 2,
                 "Elapsed Time")
    shortline = shortline + "_____"
    c.drawRightString(rmarg, topline, shortline)
    c.drawRightString(rmarg, topline - linespace, shortline)
    c.drawRightString(rmarg, topline - linespace * 2, shortline)
    c.drawString(lmarg, topline - linespace * 2, shortline)
    c.setFont("Helvetica", 10)
    c.drawString(lmarg,
                 topline - linespace * 2 - 12,
                 "Rider's signature at completion")
    # Stamp boxes
    c.drawCentredString(width / 2, INCH * 1.9, "Randonneur Committee Authorization")
    c.rect(width / 2, INCH * 1.9 - 5, -(INCH * 1.5), -INCH)
    c.rect(width / 2, INCH * 1.9 - 5, INCH * 1.5, -INCH)
    # Brevet No.
    c.drawRightString(width / 2 - 10, INCH * 0.5, "Brevet No.")
    if brevno == '':
        c.drawString(width / 2 + 10, INCH * 0.5, "__________")
    else:
        c.drawString(width / 2 + 10, INCH * 0.5, brevno)
def cardBack(c, width, height, controls):
    # ==================== Card Back ========================
    # Header
    headers = [
        ["DIST (km)", "Open", "Close", "Locale",
            "Establishment", "Signature", "Time of Passage"]
    ]
    # Generate table of controls
    def openTime(dist):
        return start + TimeDelta(hours=dist * 3 / 100)
    def closeTime(dist):
        return start + TimeDelta(hours=dist / 15)
    for control in controls:
        headers.append([
            control['dist'],
            openTime(control['dist']).strftime('%A\n%I:%M %p\n%d/%b/%y'),
            closeTime(control['dist']).strftime('%A\n%I:%M %p\n%d/%b/%y'),
            control['loc'],
            control['est'],
            "", "" # Signature and Time to be filled manually
        ])
    # Draw on the canvas
    t = Table(headers, repeatRows=1)
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), "#A0A0A0"),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), ['#FFFFFF','#F0F0F0'])
    ]))
    (w, h) = t.wrap(width - INCH, height - INCH)
    t.drawOn(c, INCH / 2, height - INCH / 2 - h)
# Collect info from user
filename = input("Enter source file (default: input.txt): ").strip()
if filename == "":
    filename = 'input.txt'
print("Loading", filename)
# Load default values
ridelen = 0
title = "Example Title"
brevno = "MissingNo."
start = DateTime.now()
start = DateTime(start.year, start.month, start.day, hour=start.hour)
controls = []
riders = []
with open(filename) as file:
    section = ""
    for line in file:
        line = line.strip()
        if line == "":
            continue
        elif line in ["[info]", "[controls]", "[riders]"]:
            section = line
        elif section == "[info]":
            infoargs = line.split("=")
            info = infoargs[0].strip()
            value = infoargs[1].strip()
            if info == "Distance":
                ridelen = value
            elif info == "Title":
                title = value
            elif info == "BrevetNo":
                brevno = value
            elif info == "Start":
                start = DateTime.strptime(value, "%d-%b-%Y %I:%M %p")
        elif section == "[controls]":
            controlargs = line.split("|")
            controls.append({
                'dist': int(controlargs[0].strip()),
                'loc': controlargs[1].strip(),
                'est': controlargs[2].strip()
            })
        elif section == "[riders]":
            riderargs = line.split("|")
            addr = riderargs[1].split("/")
            if len(addr) < 2:
                addr.append('')
            riders.append({
                'name': riderargs[0].strip(),
                'addr1': addr[0].strip(),
                'addr2': addr[1].strip(),
                'city': riderargs[2].strip(),
                'prov': riderargs[3].strip(),
                'country': riderargs[4].strip(),
                'post': riderargs[5].strip(),
                'phone': riderargs[6].strip(),
                'email': riderargs[7].strip()
            })
print(ridelen, title, brevno, start)
print("Controls")
for c in controls:
    print(c)
print("Riders")
for r in riders:
    print(r)
# Set up canvas and show info
c = canvas.Canvas(
    ".\\output\\hello.pdf",
    pagesize=LETTER
)
width, height = LETTER
# Show first page with first rider
if len(riders) > 0:
    r = riders.pop(0)
    cardFront(c, width, height, title, brevno, start, r)
else:
    cardFront(c, width, height, title, brevno, start)
c.showPage()
# Show controls page
cardBack(c, width, height, controls)
c.showPage()
# Show rider pages, if needed
for r in riders:
    cardFront(c, width, height, title, brevno, start, r)
    c.showPage()
c.save()
print("Finished")
