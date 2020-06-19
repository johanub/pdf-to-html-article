import os
import base64

test_header = """
<html lang="da">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
          integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

    <title>Hello, world!</title>
</head>
<body>
<div class="row justify-content-center">
    <div class="col-5" style="white-space: pre-wrap;max-width:800px;word-wrap: break-word">"""

test_endheader = """


</div>
</div>
<style>
    h1 {
        margin-top: 15px;
        font-size: 30px
    }
    h2 {
        margin-top: 15px;
        font-size: 30px
    }
</style>
</body>
"""


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
        for line in self.xml_root.iter('text'):
            html_line = ''
            line_text = ''

            for img in pics:
                if not img['used']:
                    if int(line.attrib['top']) > int(img['top']):
                        html += '<img src="{}" style="width: {};height: {}">'\
                            .format(img['src'], img['width'], img['height']) + '\n'
                        img['used'] = True

            for text in line.itertext():
                line_text += text

            if not str(line_text).strip():
                if prev_line != '\n\n\n':
                    html_line += '\n'
                    html += html_line
                    if '\n' in prev_line:
                        prev_line += html_line
                    else:
                        prev_line = html_line
                continue

            html_line += fonts[line.attrib['font']]['tag']
            subelem = list(line)
            if subelem:
                if subelem[0].tag == 'a':
                    if not subelem[0].attrib['href'].startswith(export_path):
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

        with open(export_path, 'w') as f:
            f.write(test_header + html.strip() + test_endheader)

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
                                 'src': prefix + base64.b64encode(f.read()).decode('utf-8'),
                                 'used': False})
        return exptimgs

    def _convert2xml(self):
        import xml.etree.ElementTree as ET
        os.system('pdftohtml -c -xml {} {}'.format(self.pdf_path, self.xml_path))
        return ET.parse(self.xml_path).getroot()
