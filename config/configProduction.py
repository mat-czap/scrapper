SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://user:password@scrapper_db_1:3306/db"
SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 499, 'pool_timeout': 10, 'pool_pre_ping': True}