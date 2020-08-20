from html_converter import HtmlConverter
import boto3
import os

s3 = boto3.resource("s3")
s3_bucket = s3.Bucket("notrfiler")


def index(event, context):
    eventkey = event['Records'][0]['s3']['object']['key']
    base = os.path.basename(eventkey)
    nameonly = os.path.splitext(base)[0]
    s3.meta.client.download_file('notrfiler', 'pdf/' + nameonly + '.pdf', '/tmp/' + nameonly + '.pdf')
    cnv = HtmlConverter('/tmp/' + nameonly + '.pdf')
    cnv.export_html('/tmp/' + nameonly + '.html')
    f = open('/tmp/' + nameonly + '.html', 'rb')
    s3_bucket.put_object(Key='html/' + nameonly + '.html', Body=f, ACL="public-read")
    f.close()
    return nameonly + '.html'


