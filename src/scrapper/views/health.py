from flask import Blueprint


health = Blueprint('health', __name__)


@health.route('/health',methods=['GET'])
def get_state():
    return "ok"
