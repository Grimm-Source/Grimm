from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from config import BASE_DIR

pdfmetrics.registerFont(TTFont('SimHei', os.path.join(BASE_DIR, 'static/SimHei.ttf')))


def generate_certification(certification_info):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)  # choose your font colour
    can.setFont("SimHei", 10)  # choose your font type and font size
    # can.drawString(120, 350, "赵丽媛")  # name
    # can.drawString(120, 315, "居民身份证")  # type of certificate
    # can.drawString(235, 315, "220402198705126466")  # code of certificate
    # can.drawString(70, 255, "爱心牵手你我同行支援陪走活动")  # activities
    # can.drawString(155, 218, "3.0小时")  # service time
    # can.drawString(120, 150, "王臻")  # director
    # can.drawString(250, 150, "刘莉娟")  # manager
    # can.drawString(250, 123, "1388888888")  # contact
    can.drawString(120, 350, certification_info.get("name", None))  # name
    can.drawString(120, 315, certification_info.get("certificate_type", None))  # type of certificate
    can.drawString(235, 315, certification_info.get("certificate_code", None))  # code of certificate
    can.drawString(70, 255, certification_info.get("activity_title", None))  # activities
    can.drawString(155, 218, certification_info.get("activity_during", None))  # service time
    can.drawString(120, 150, certification_info.get("director", None))  # director
    can.drawString(250, 150, certification_info.get("manager", None))  # manager
    can.drawString(250, 123, certification_info.get("contact_code", None))  # contact
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    certification_template = os.path.join(BASE_DIR, "static/certificationempty.pdf")
    existing_pdf = PdfFileReader(open(certification_template, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    certification_file = certification_info.get("name", None) + "_certification.pdf"
    certification_files_path = os.path.join(BASE_DIR, "static/certificationfiles/" + certification_file)
    outputStream = open(certification_files_path, "wb")
    output.write(outputStream)
    outputStream.close()
    # print(certification_files_path)

    return certification_files_path


if __name__ == '__main__':
    certification_info = {"name": "彭涛",
                          "certificate_type": "居民身份证",
                          "certificate_code": "220402198705126466",
                          "activity_title": "爱心牵手你我同行支援陪走活动",
                          "activity_during": "3.0小时",
                          "director": "王臻",
                          "manager": "刘莉娟",
                          "contact_code": "1388888888"
                          }
    generate_certification(certification_info)
