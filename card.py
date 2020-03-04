from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

def hello(c):
    c.drawString(100, 100, "Example")
c = canvas.Canvas(
    ".\\output\\hello.pdf",
    pagesize=LETTER,

)
width, height = LETTER
print("Width:", width, "Height:", height)
hello(c)
c.showPage()
c.save()