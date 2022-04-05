import requests
import lxml.html
import validators
import helpers
import csv
import yaml

def get_file_name(url):
    try:
        return url.split('/')[-1].split('.')[0] + '.csv'
    except Exception as e:
        print('Something went wrong:', e)
        return ''


def get_text(url):
    try:
        session = requests.session()
        session.mount('https://', helpers.TLSAdapter())
        resp = session.get(url)
    except Exception as e:
        print(e)
        return None

    return lxml.html.document_fromstring(resp.text)


def write_to_csv(url, html_tree):
    text_orig = html_tree.xpath('//*[@id="click_area"]/div//div[@class="original"]/text()')
    text_transl = html_tree.xpath('//*[@id="click_area"]/div//div[@class="translate"]/text()')

    fname = get_file_name(url)

    if fname == '':
        return

    with open(fname, 'w', newline='', encoding='UTF-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for i in range(len(text_orig)):
            if (text_orig[i] == '\n') and (text_transl[i] == '\n'):
                continue
            csv_writer.writerow([text_orig[i].replace('\n', '')])
            csv_writer.writerow([text_transl[i].replace('\n', '')])


def parse(url):
    if not ('http' in url):
        url = 'http://' + url

    result = validators.url(url)

    if isinstance(result, validators.ValidationFailure) or not result:
        print('Wrong url!')
        return

    html_tree = get_text(url)

    if html_tree is None:
        return

    write_to_csv(url, html_tree)

def get_urls():
    with open('urls.yml', 'r') as yaml_file:
        objects = yaml.load(yaml_file, yaml.Loader)
        return objects


def main():
    urls = get_urls()
    for url in urls:
        parse(url.strip())


if __name__ == '__main__':
    main()
