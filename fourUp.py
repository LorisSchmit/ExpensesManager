#!/usr/bin/env python

'''
usage:   fourUp.py my.pdf

Creates 4up.my.pdf with a single output page for every
4 input pages.
'''

import sys
import os

from pdfrw import PdfReader, PdfWriter, PageMerge


def scale(fact):
    writer = PdfWriter('test.pdf')
    writer.addpage()

def getFour(srcpages):
    scale = 0.5
    srcpages = PageMerge() + srcpages
    x_increment, y_increment = (scale * i for i in srcpages.xobj_box[2:])
    print(x_increment)
    print(y_increment)
    for i, page in enumerate(srcpages):
        page.scale(scale)
        page.x = x_increment if i & 1 else 0
        page.y = 0 if i & 2 else y_increment
    return srcpages.render()

def toFourUp(inpfn):
    #inpfn, = sys.argv[1:]
    months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober"]
    outfn = os.path.basename(inpfn)
    pages = []

    for month in months:
        dir = "images/"+month+" 2019.pdf"
        pages.append(PdfReader(dir).getPage(0))

    writer = PdfWriter(outfn)
    for index in range(0, len(pages), 10):
        writer.addpage(getFour(pages[index:index + 10]))
    writer.write()

