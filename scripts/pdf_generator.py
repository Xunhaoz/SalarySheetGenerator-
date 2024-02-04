# -*- coding: utf-8 -*-


import time
from PIL import Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image as reportImage
from reportlab.lib import colors


class PDFFileGenerator:
    def __init__(self):
        self.page = []
        self.styles = {}
        self._set_setting()

    def _set_setting(self):
        pdfmetrics.registerFont(TTFont('JhengHei', "./static/asset/font/JhengHei.ttf"))

        title_style = ParagraphStyle(
            'Title',
            fontName='JhengHei',
            fontSize=16,
            leading=24,
            alignment=TA_CENTER,
            fontWeight='bold',
            textColor=colors.black,
        )

        date_style = ParagraphStyle(
            'Date',
            fontName='JhengHei',
            fontSize=12,
            leading=20,
            alignment=TA_RIGHT,
            fontWeight='bold',
            textColor=colors.black,
        )

        table_header_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'JhengHei'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEADING', (0, 0), (-1, -1), 14),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ])

        table_content_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'JhengHei'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEADING', (0, 0), (-1, -1), 14),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ])

        self.styles['title_style'] = title_style
        self.styles['date_style'] = date_style
        self.styles['table_content_style'] = table_content_style
        self.styles['table_header_style'] = table_header_style

    def add_title(self):
        self.page.append(Paragraph('核果智能科技股份有限公司', self.styles['title_style']))
        self.page.append(Paragraph('勞務報酬單\t簽收單', self.styles['title_style']))

    def add_datetime(self):
        current_date = time.strftime("填表日期： %Y 年 %m 月 %d 日", time.localtime())
        self.page.append(Paragraph(current_date, self.styles['date_style']))

    def add_table_header(self, text):
        header_list = [text]
        self.page.append(Table([header_list], colWidths=[460], style=self.styles['table_header_style']))

    def add_table_content(self, key, value):
        content_list = [key, value]
        self.page.append(Table([content_list], colWidths=[160, 300], style=self.styles['table_content_style']))

    def add_picture_content(self, id_card_front, id_card_back):
        front = reportImage(id_card_front, 220, 150)
        back = reportImage(id_card_back, 220, 150)
        content_list = [front, back]
        self.page.append(
            Table([content_list], colWidths=[230, 230], rowHeights=[150], style=self.styles['table_content_style'])
        )

    def add_sign_content(self):
        content_list = ['(簽名/蓋章) 領款人：']
        self.page.append(
            Table([content_list], colWidths=[460], rowHeights=[50], style=self.styles['table_content_style']))

    def gen_pdf(self, file_name):
        pdf = SimpleDocTemplate(file_name, pagesize=A4)
        pdf.build(self.page)


def gen_pdf(member, project_name, development_fee, payment, category, method, date, dest_path):
    payment = int(payment)
    payee_table = {
        '專案名稱': project_name,
        '軟體開發費': development_fee,
        '領款人姓名': member.name,
        '身份證字號': member.national_id,
        '聯絡電話': member.phone,
        '戶籍地址': member.residence_address,
        '通訊地址': member.mailing_address
    }

    withdraw_table = {
        '銀行匯款帳號': f"{member.bank} {member.bank_account}",
        '支付金額': payment,
        '所得類別': category,
        '-代扣所得稅10%': int(payment * 0.1),
        '-健保補充保費2.11%': int(payment * 0.0211),
        '=支領淨額': payment - int(payment * 0.1) - int(payment * 0.0211),
        '戶籍地址': member.residence_address,
        '付款方式': method,
        '收款日期': date
    }

    pdf_file_gen = PDFFileGenerator()
    pdf_file_gen.add_title()
    pdf_file_gen.add_datetime()

    pdf_file_gen.add_table_header('領款人')
    for table_key, table_value in payee_table.items():
        pdf_file_gen.add_table_content(table_key, table_value)

    pdf_file_gen.add_table_header('領款金額')
    for table_key, table_value in withdraw_table.items():
        pdf_file_gen.add_table_content(table_key, table_value)

    pdf_file_gen.add_table_header('身份證正反面影本')
    pdf_file_gen.add_picture_content(member.id_card_front, member.id_card_back)
    pdf_file_gen.add_sign_content()

    pdf_file_gen.gen_pdf(dest_path)
