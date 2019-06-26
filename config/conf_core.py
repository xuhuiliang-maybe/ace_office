# coding=utf-8
import ConfigParser
import os

config_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(config_dir, 'conf')

conf_object = ConfigParser.ConfigParser()
conf_object.read(config_path)

# 数据库相关
DB_ENGINE = conf_object.get("database", "engine")
DB_NAME = conf_object.get("database", "dbname")
DB_USERNAME = conf_object.get("database", "username")
DB_PASSWORD = conf_object.get("database", "password")
DB_HOST = conf_object.get("database", "host")
DB_PORT = conf_object.get("database", "port")

# 系统相关
MEMCACHED = conf_object.get("sys", "memcached")  # 缓存
PAGINATE = conf_object.get("sys", "paginate")  # 分页
SUPERUSERNAMES = conf_object.get("sys", "superusername").split(",")  # 超管用户名列表

# 服务相关
SET_DEBUG = conf_object.get("service", "debug")
