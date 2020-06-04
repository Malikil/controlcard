import cardgen
from datetime import datetime as DateTime

filename = input("Enter source file (default: input.txt): ").strip()
if (filename == ''):
    filename = 'input.txt'
output = input("Enter destination file (default: card.pdf): ").strip()
if (output == ''):
    output = 'card.pdf'
print(f'Loading {filename}')

# Load info from file
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
        if line == "" or line[0] == "#":
            continue
        elif line in ["[info]", "[controls]", "[riders]"]:
            section = line
        elif section == "[info]":
            infoargs = line.split("=")
            info = infoargs[0].strip()
            value = infoargs[1].strip()
            if info == "Distance":
                ridelen = int(value)
            elif info == "Title":
                title = value
            elif info == "BrevetNo":
                brevno = value
            elif info == "Start":
                start = DateTime.strptime(value, "%d-%b-%Y %I:%M %p")
        elif section == "[controls]":
            controlargs = line.split("|")
            controls.append(cardgen.Control(
                distance=int(controlargs[0].strip()),
                location=controlargs[1].strip(),
                establishment=controlargs[2].strip()
            ))
        elif section == "[riders]":
            riderargs = line.split("|")
            addr = riderargs[1].split("/")
            if len(addr) < 2:
                addr.append('')
            riders.append(cardgen.Rider(
                name=riderargs[0].strip(),
                addr1=addr[0].strip(),
                addr2=addr[1].strip(),
                city=riderargs[2].strip(),
                prov=riderargs[3].strip(),
                country=riderargs[4].strip(),
                postal=riderargs[5].strip(),
                phone=riderargs[6].strip(),
                email=riderargs[7].strip()
            ))
print(ridelen, title, brevno, start)
print("Controls")
for c in controls:
    print(c)
print("Riders")
for r in riders:
    print(r)
# Set up generator and save info
gen = cardgen.CardGen(f'.\\output\\{output}')
gen.setRideInfo(ridelen, title, brevno, start, '.\\images\\logo.png', controls)
gen.printableList(riders)
gen.save()

print(f'Wrote to file: {output} in output folder')