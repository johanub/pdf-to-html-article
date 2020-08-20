import os
import base64

test_header = """"""

test_endheader = """"""


class HtmlConverter:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        pre, ext = os.path.splitext(self.pdf_path)
        self.xml_path = pre + '.xml'
        self.xml_root = self._convert2xml()

    def export_html(self, export_path):
        pics = self.get_b64_imgs()

        fonts = self.get_fonts()
        html = ''
        prev_line = ''
        prev_top = 0
        for page in self.xml_root.iter('page'):
            for line in page.iter('text'):
                html_line = ''
                line_text = ''
                same_line = False

                if -25 <= int(line.attrib['top']) - prev_top <= 25:
                    same_line = True

                for img in pics:
                    if not img['used']:
                        print(int(img['page']), int(page.attrib['number']))
                        if int(page.attrib['number']) == int(img['page']):
                            print(int(line.attrib['top']), int(img['top']))
                            if int(line.attrib['top']) > int(img['top']):
                                html += '<img src="{}" style="width: {}px;height: {}px">'\
                                    .format(img['src'], img['width'], img['height']) + '\n'
                                img['used'] = True

                for text in line.itertext():
                    line_text += text

                if not str(line_text).strip():
                    if prev_line != '\n\n':
                        html_line += '\n'
                        html += html_line
                        if '\n' in prev_line:
                            prev_line += html_line
                        else:
                            prev_line = html_line
                    continue

                if same_line:
                    html_line += fonts[line.attrib['font']]['tag'].replace('X', 'display: inline-block')
                else:
                    html_line += fonts[line.attrib['font']]['tag']

                subelem = list(line)
                if subelem:
                    if subelem[0].tag == 'a':
                        _, tail = os.path.split(export_path)
                        if not subelem[0].attrib['href'].startswith(tail):
                            html_line += \
                                """<a href="{}">{}</a>""".format(subelem[0].attrib['href'], line_text)
                        else:
                            html_line += line_text
                    elif subelem[0].tag == 'b':
                        html_line += \
                            """<b>{}</b>""".format(line_text)
                    elif subelem[0].tag == 'i':
                        html_line += \
                            """<i>{}</i>""".format(line_text)
                else:
                    html_line += line_text
                html_line += fonts[line.attrib['font']]['endtag']

                html += html_line
                prev_line = html_line
                prev_top = int(line.attrib['top'])

        with open(export_path, 'w') as f:
            f.write(test_header + html.strip() + test_endheader)
        # os.remove(self.xml_path)

    def get_fonts(self):
        from font_config import font_parser
        return font_parser(self.xml_root)

    def get_b64_imgs(self):
        imgs = self.xml_root.iter('image')
        exptimgs = []
        for img in imgs:
            with open(img.attrib['src'], 'rb') as f:
                ext = img.attrib['src'].split('.')[-1]
                prefix = f'data:image/{ext};base64,'
                exptimgs.append({'height': img.attrib['height'],
                                 'width': img.attrib['width'],
                                 'top': img.attrib['top'],
                                 'page': self.xml_root.find('.//image[@src="{}"]...'.format(img.attrib['src'])).attrib['number'],
                                 'src': prefix + base64.b64encode(f.read()).decode('utf-8'),
                                 'used': False})
            os.remove(img.attrib['src'])
        return exptimgs

    def _convert2xml(self):
        import xml.etree.ElementTree as ET
        os.system('pdftohtml -c -xml {} {}'.format(self.pdf_path, self.xml_path))
        return ET.parse(self.xml_path).getroot()
