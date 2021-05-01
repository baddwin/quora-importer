import os.path
import traceback

from bs4 import BeautifulSoup
from exporter import export


def get_data(content_dir: str) -> list:
    result = []
    with open(os.path.join(content_dir, 'index.html'), 'r') as html:
        soup = BeautifulSoup(html.read(), features='html.parser')
        para = soup.find_all(name='p', class_='')

        for inner in para:
            content = {}
            divs = inner.find_all(name='div')
            for div in divs:
                if div.strong is not None:
                    text = div.strong.string.replace(':', '').rstrip()
                    judul = ['Question', 'Content', 'Creation time']
                    if text in judul:
                        if text == judul[1]:
                            content[text] = div.span.contents
                        else:
                            content[text] = div.span.text

                # elif 'ui_qtext_image' in div.attrs['class'][0]:
                #     print('Gambar:')
                #     print('https://qph.fs.quoracdn.net/main-{}'.format(div.img.attrs['src'].split('/')[1]))

                # print(f'\t{div}')
            # print('==========================================')
            result.append(content)
            break

        html.close()

    return result


def process_data(extype: str, inpath: str, outpath: str) -> bool:
    try:
        html = get_data(inpath)
        data = {'html': html, 'path': outpath, 'name': extype}
        success = export.save(data=data)
        return success

    except Exception as e:
        print(e)
        traceback.print_exc()
        return False
