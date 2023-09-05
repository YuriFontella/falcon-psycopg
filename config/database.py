import psycopg, configparser, os

config = configparser.ConfigParser()

env = os.environ.get('ENV', 'development')

if env:
    config.read('config.ini')

def row_factory(cursor):
    fields = [c.name for c in cursor.description]

    def make_row(values):
        return dict(zip(fields, tuple(map(str, values))))

    return make_row

db = psycopg.connect(config.get(env, 'CONNINFO'), row_factory=row_factory)
