import os.path
import traceback

from bs4 import BeautifulSoup
from exporter import export


def get_data(content_dir: str) -> dict:
    result = {'html': [], 'images': []}
    with open(os.path.join(content_dir, 'index.html'), 'r') as html:
        soup = BeautifulSoup(html.read(), features='html.parser')
        para = soup.find_all(name='p', class_=None)

        for inner in para:
            content, images = {}, []
            divs = inner.find_all(name='div', class_=None)
            date = ''
            for div in divs:
                if div.strong is not None:
                    text = div.strong.string.replace(':', '').rstrip()
                    judul = ['Question', 'Content', 'Creation time']
                    if text in judul:
                        if text == judul[1]:
                            content[text] = div.span.contents
                        else:
                            content[text] = div.span.text
                            date = div.span.text
                # print(f'\t{div}')
            result['html'].append(content)

            div_img = inner.find_all(name='div', class_='ui_qtext_image_outer')
            for image in div_img:
                img = {}
                name = image.img.attrs['src'].split('/')[1]
                img['name'] = name.split('-')[1]
                img['url'] = 'https://qph.fs.quoracdn.net/main-{0}'.format(name)
                img['date'] = date

                result['images'].append(img)
            # break

        html.close()

    return result


def process_data(extype: str, inpath: str, outpath: str) -> bool:
    try:
        html = get_data(inpath)
        # print(html)
        # success = True
        data = {'html': html, 'path': outpath, 'name': extype}
        success = export.save(data=data)
        return success

    except Exception as e:
        print(e)
        traceback.print_exc()
        return False
