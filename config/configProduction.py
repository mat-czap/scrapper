SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://user:password@scrapper_db_1:3306/db"
SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 499, 'pool_timeout': 10, 'pool_pre_ping': True}
RABBITMQ_URL="amqp://rabbitmq?connection_attempts=5&retry_delay=5"
FLASK_PIKA_PARAMS = {
    'host':'rabbitmq',      #amqp.server.com
    'username': 'guest',  #convenience param for username
    'password': 'guest',  #convenience param for password
    'port': 5672,            #amqp server port
    'virtual_host':'vhost'   #amqp vhost
}