from reportlab.pdfgen import canvas
import os
from pdfrw import pdfwriter
from fourUp import toFourUp


def drawMyRuler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')
    pdf.drawString(600, 810, 'x600')
    pdf.drawString(700, 810, 'x700')
    pdf.drawString(800, 810, 'x800')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')



def drawPDF():

    file_name = "test.pdf"
    document_title = "This is the title"
    title = "This is the real title"
    text = ["This pdf is just a dummy pdf to test if","the module even works"]

    pdf = canvas.Canvas(file_name)

    pdf.setTitle(document_title)

    drawMyRuler(pdf)

    pdf.save()


def getGraphs():
    dir = 'images'
    entries = os.listdir(dir)
    path = dir+"/"+"Januar 2019.pdf"
    toFourUp(path)


getGraphs()

