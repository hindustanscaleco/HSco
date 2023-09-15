import pymysql
from Hsco.celery import app as celery_app
pymysql.version_info = (1, 0, 3, "final", 0)

pymysql.install_as_MySQLdb()
__all__ = ['celery_app']
    