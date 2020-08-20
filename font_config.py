def font_parser(root):
    fonts = {}
    for child in root.iter('fontspec'):
        fonts[child.attrib['id']] = {'color': child.attrib['color'],
                                     'size': int(child.attrib['size']),
                                     'tag': '',
                                     'endtag': '',
                                     'font': child.attrib['family']}
        if fonts[child.attrib['id']]['size'] >= 25:
            fonts[child.attrib['id']]['tag'] = '<h1 style="font-size: {}px;X">'.format(fonts[child.attrib['id']]['size'])
            fonts[child.attrib['id']]['endtag'] = '</h1>'
        elif fonts[child.attrib['id']]['size'] >= 21:
            fonts[child.attrib['id']]['tag'] = '<h2 style="font-size: {}px;X">'.format(fonts[child.attrib['id']]['size'])
            fonts[child.attrib['id']]['endtag'] = '</h2>'
        else:
            if 'Math' in child.attrib['family']:
                fonts[child.attrib['id']]['tag'] = '<p style="font-size: {}px;margin:0;display:inline-block">'.format(
                    fonts[child.attrib['id']]['size'])
                fonts[child.attrib['id']]['endtag'] = '</p>'
            elif fonts[child.attrib['id']]['size'] <= 11:
                fonts[child.attrib['id']]['tag'] = '<sub style="font-size: {}px;margin:0;display:inline-block">'.format(
                    fonts[child.attrib['id']]['size'])
                fonts[child.attrib['id']]['endtag'] = '</sub>'
            else:
                fonts[child.attrib['id']]['tag'] = '<p style="font-size: {}px;margin:0;X">'.format(
                    fonts[child.attrib['id']]['size'])
                fonts[child.attrib['id']]['endtag'] = '</p>'
    return fonts
