import requests
from bs4 import BeautifulSoup
from scrapper.worker.Worker import ScrappedData


class StatusCode500Error(Exception):
    pass


def scrap_by_url(url: str) -> ScrappedData:
    if "http://" not in url:
        url = "http://" + url

    content = str()
    try:
        content = requests.get(str(url))
        if content.status_code >= 500:
            raise StatusCode500Error

    except StatusCode500Error as exc:
        print("500 error")

    soup = BeautifulSoup(content.text, 'html.parser')

    scrapped_links: ScrappedData = ScrappedData(str(), set())

    try:
        for link in soup.find_all('a'):
            if link is not None:
                scrapped_links.data.add(link.get('href'))
            else:
                continue
        scrapped_links.status = "ok"
    except Exception as ex:
        print(ex)
    return scrapped_links
