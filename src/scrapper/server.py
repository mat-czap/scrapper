from flask import Flask, request
from bs4 import BeautifulSoup
import requests



app = Flask(__name__)

@app.route('/',methods=['POST'])
def get_name():
    name = request.json
    for url in name["urls"]:
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'html.parser')
        for link in soup.find_all('a'):
            print(link.get('href'))

    # content = requests.get(name["url"])
    # import pdb; pdb.set_trace()

    return "ok"

# {"urls": ["http://onet.pl", "http://google.pl"]}

if __name__ == '__main__':
    app.run(debug=True)
