def font_parser(root):
    fonts = {}
    for child in root.iter('fontspec'):
        fonts[child.attrib['id']] = {'color': child.attrib['color'],
                                     'size': int(child.attrib['size']),
                                     'tag': '',
                                     'endtag': ''}
        if fonts[child.attrib['id']]['size'] >= 25:
            fonts[child.attrib['id']]['tag'] = '<h1 style="size: {}">'.format(fonts[child.attrib['id']]['size'])
            fonts[child.attrib['id']]['endtag'] = '</h1>'
        elif fonts[child.attrib['id']]['size'] >= 24:
            fonts[child.attrib['id']]['tag'] = '<h2 style="size: {}">'.format(fonts[child.attrib['id']]['size'])
            fonts[child.attrib['id']]['endtag'] = '</h2>'
    return fonts
