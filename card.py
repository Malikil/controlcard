from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch as INCH

# Can define paragraph style stuff here, see chapter 5/6

def hello(c, width, height, description=""):
    # ================= Card Front =======================
    # Image should be centered, and take up about 2/3 of the page width
    # Actual values are for 1/5 page width margin on either side, 1 inch top margin
    # Image height capped at 1.5 inches
    c.drawImage(".\\images\\logo.png", width / 5, height - INCH * 0.6,
        width=(width * 3 / 5),
        height=-(INCH * 2),
        preserveAspectRatio=True
    )
    # Print the "control card" text
    c.setFont("Helvetica", 36)
    c.drawCentredString(width / 2, height - INCH * 3.2, "Control Card")
    # Description
    # Should be smaller text, centered, and italics
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, height - INCH * 3.66, description)
    # Name, address: Title with single line
    c.setFont("Helvetica", 14)
    underline = "_______________________________________________"
    linespace = 0.4 * INCH
    topline = height - INCH * 4.4
    lmarg = INCH
    rmarg = width - INCH
    c.drawString(lmarg, topline, "Name")
    c.drawString(lmarg, topline - linespace, "Address")
    c.drawRightString(rmarg, topline, underline)
    c.drawRightString(rmarg, topline - linespace, underline)
    c.drawRightString(rmarg, topline - linespace * 1.8, underline)
    # City, Province, Country, Postal Code, Phone, Email: Two columns
    topline = topline - linespace * 1.8
    shortline = "_______________"
    midmarg = INCH / 4.3
    c.drawString(lmarg,
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
    c.drawRightString(rmarg,
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
                      shortline)
    c.drawRightString(width / 2 - midmarg,
                      topline - linespace * 3,
                      shortline)
    # Static text
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, INCH * 3.85, "Founding member of LES RANDONNEURS MONDIAUX (1983)")
    c.drawCentredString(width / 2, INCH * 3.2, "Each Randonneur must carry a Control Card, have it signed at the control between the opening")
    c.drawCentredString(width / 2, INCH * 3.2 - 15, "and closing times, and return it to the organizer.")
    # Date, start/finish/elapsed times, signature line: Two columns, different sizes
    c.setFont("Helvetica", 14)
    topline = INCH * 3.2 - 40
    c.drawString(lmarg, topline, "Date   " + shortline)
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
    # Brevet No.
    # ==================== Card Back ========================
    # Header
    # Generate table of controls
c = canvas.Canvas(
    ".\\output\\hello.pdf",
    pagesize=LETTER
)
width, height = LETTER
print("Width:", width, "Height:", height)
hello(c, width, height, "How long should this description really be? I'll see how it looks by filling the entire box provided, or at least getting pretty close to it")
c.showPage()
c.save()
