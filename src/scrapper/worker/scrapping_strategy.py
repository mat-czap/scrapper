import requests
from bs4 import BeautifulSoup
from scrapper.worker.worker import ScrappedData, EncodedData


class StatusCode500Error(Exception):
    pass


def strategy_1(data: EncodedData) -> ScrappedData:
    if "http://" not in data.url:
        data.url = "http://" + data.url

    content = str()
    try:
        content = requests.get(str(data.url))
        if content.status_code >= 500:
            raise StatusCode500Error

    except StatusCode500Error:
        print("500 error")

    soup = BeautifulSoup(content.text, 'html.parser')
    scrapped_links: ScrappedData = ScrappedData(data)
    try:
        for link in soup.find_all('a'):
            if link is not None:
                scrapped_links.links.add(link.get('href'))
            else:
                continue
        scrapped_links.scrapped_status = True
    except Exception as ex:
        print(ex)
    return scrapped_links
