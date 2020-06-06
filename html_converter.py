import os

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
    <div class="col-7" style="white-space: pre-wrap;">"""

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
        fonts = self.get_fonts()
        html = ''
        prev_line = ''
        for line in self.xml_root.iter('text'):
            html_line = ''
            line_text = ''

            for text in line.itertext():
                line_text += text

            if not str(line_text).strip():
                html_line += '\n'
                html += html_line
                prev_line += html_line
                continue

            html_line = fonts[line.attrib['font']]['tag']
            html_line += line_text
            html_line += fonts[line.attrib['font']]['endtag']
            html += html_line
            prev_line = html_line

        with open(export_path, 'w') as f:
            f.write(test_header + html.replace('\n\n\n', '\n').replace('\n\n', '\n') + test_endheader)

        # if line.find('a'):
        #     html_line = \
        #         """<a href="{0.attrib['href']}">{0.text}</a>""".format(line.find('a'))
        # if line.find('b'):
        #     html_line = \
        #         """<b>{0.text}</b>""".format(line.find('b'))
        # if line.find('i'):
        #     html_line = \
        #         """<i>{0.text}</i>""".format(line.find('i'))

    def get_fonts(self):
        from font_config import font_parser
        return font_parser(self.xml_root)

    def get_b64_img(self):
        pass

    def _convert2xml(self):
        import xml.etree.ElementTree as ET
        os.system('pdftohtml -c -xml {} {}'.format(self.pdf_path, self.xml_path))
        return ET.parse(self.xml_path).getroot()
