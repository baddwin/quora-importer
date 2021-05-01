import locale
from bs4 import BeautifulSoup
from dateutil import parser
from dateutil.tz import tzoffset
from exporter import export


def get_data(location: str) -> list:
    # print(f'Simpan ke {location}')
    result = []
    with open('content/index.html', 'r') as html:
        # result = []
        soup = BeautifulSoup(html.read(), features='html.parser')
        para = soup.find_all(name='p', class_='')
        # print(soup.prettify())
        for konten in para:
            content = {}
            isi = konten.find_all(name='div')
            for data in isi:
                if data.strong is not None:
                    text = data.strong.string.strip()
                    judul = ['Question:', 'Content:', 'Creation time:']
                    if text in judul:
                        # print(text)
                        # print(data.span.contents)
                        contents = data.span.contents
                        if len(contents) > 1:
                            content[text] = data.span.contents
                        else:
                            content[text] = data.span.string

                        # for tulisan in contents:
                        #     print(f'\t{tulisan}')
                            # if text == judul[2]:
                            #     tgl = parser.parse(tulisan, tzinfos={'PDT': -7 * 3600})
                            #     print('\t' + tgl.astimezone(tzoffset(None, 0)).strftime('%Y-%m-%d %H:%M:%S'))
                    # print(f'Isi: \n{data.strong.string}')

                # elif 'ui_qtext_image' in data.attrs['class'][0]:
                #     print('Gambar:')
                #     print('https://qph.fs.quoracdn.net/main-{}'.format(data.img.attrs['src'].split('/')[1]))

                # print(f'\t{data}')
            # print('==========================================')
            result.append(content)

            break

        html.close()

    return result


def process_data(extype: str, outpath: str) -> int:
    try:
        html = get_data(outpath)
        data = {'html': html, 'path': outpath, 'name': extype}
        success = export.save(data=data)
        return success

    except Exception as e:
        print(e)
        return False
