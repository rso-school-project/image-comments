from starlette.config import Config

# Config values will be given from environment variables and/or ".env" file.
# Also note that if we dont provide configuration file, the defauts act as development enviroment.
config = Config('.env')


# for all other settings we first try to fetch them from etcd server. If not found/available
# we get them from project lvl enviroment variables.
test_x = config('test_x', cast=str, default='This is test variable x')
