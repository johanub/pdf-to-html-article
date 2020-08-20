from html_converter import HtmlConverter
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('reindex_pdfs/') if isfile(join('reindex_pdfs/', f))]

for pdf in onlyfiles:
    if pdf.split('.')[-1] == 'pdf':
        cnv = HtmlConverter('reindex_pdfs/' + pdf)
        cnv.export_html('html/' + pdf.split('.')[0] + '.html')
        print(pdf.split('.')[0] + '.html')

# cnv = HtmlConverter('test2.pdf')
# cnv.export_html('test2.html')
