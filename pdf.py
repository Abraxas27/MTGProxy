import sys
import os
import param
import math
from log import logger as log

# Inspired from https://github.com/promisedlandt/mtg_proxy_printer/


try:
    import reportlab
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
except ImportError:
    log.critical('ReportLab not installed. Go to http://www.reportlab.org/')
    sys.exit(1)


def print_pdf(max_id, output_file_name):
    canvas = Canvas(output_file_name, pagesize=A4)
    # card size in mm
    CARD_WIDTH = 63
    CARD_HEIGHT = 88
    CARDS_ON_PAGE = 9

    padding_left = (A4[0] - 3 * CARD_WIDTH * mm) / 2
    padding_bottom = (A4[1] - 3 * CARD_HEIGHT * mm) / 2

    def make_page(page, max_id, canvas):
        log.debug("Page : " + str(page))
        canvas.translate(padding_left, padding_bottom)
        x, y = 0, 3
        for i in range(1, 10):
            index = i + 9*(page - 1)
            if index <= max_id:
                log.debug("Image : " + str(index))
                image = os.path.join(param.OUTPUT_PROXY_DIR, str(index) + '.jpg')
                if x % 3 == 0:
                    y -= 1
                    x = 0
                # x and y define the lower left corner of the image you wish to
                # draw (or of its bounding box, if using preserveAspectRation below).
                canvas.drawImage(image, x=x * CARD_WIDTH * mm, y=y * CARD_HEIGHT * mm, width=CARD_WIDTH * mm,
                                 height=CARD_HEIGHT * mm)
                x += 1
            else:
                break
        canvas.showPage()

    def number_of_pages(max_id):
        return int(math.ceil(1.0 * max_id / CARDS_ON_PAGE))

    for page in range(1, number_of_pages(max_id)+1):
        make_page(page, max_id, canvas)

    try:
        canvas.save()
    except IOError:
        log.error('Save of the file {} failed. If you have the PDF file opened, close it.'.format(output_file_name))

    log.info('{} saved.'.format(output_file_name))
