from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch as INCH

def hello(c, width, height, description=""):
    # Image should be centered, and take up about 2/3 of the page width
    # Actual values are for 1/5 page width margin on either side, 1 inch top margin
    # Image height capped at 1.5 inches
    c.drawImage(".\\images\\logo.png", width / 5, height - INCH,
        width=(width * 3 / 5),
        height=-(INCH * 2),
        preserveAspectRatio=True
    )
    # Print the control card text
    c.setFontSize(36)
    c.drawCentredString(width / 2, height - INCH * 4, "Control Card")
    # Description
c = canvas.Canvas(
    ".\\output\\hello.pdf",
    pagesize=LETTER
)
width, height = LETTER
print("Width:", width, "Height:", height)
hello(c, width, height)
c.showPage()
c.save()