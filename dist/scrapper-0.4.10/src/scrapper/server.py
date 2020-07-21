from flask import request, Blueprint
site = Blueprint('site', __name__)


@site.route('/',methods=['POST'])
def get_name():
    # from scrapper.tasks import scrappe_url
    from scrapper import celery_app
    name = request.json
    print(name)
    for url in name["urls"]:
        celery_app.send_task("scrapper.tasks.scrappe_url", (url,))
        # scrappe_url.delay(url)

    return "ok"

