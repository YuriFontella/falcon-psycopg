import psycopg, configparser, os

config = configparser.ConfigParser()

env = os.environ.get('ENV', 'development')

if env:
    config.read('config.ini')

def row_factory(cursor):
    fields = [c.name for c in cursor.description]

    def conditionals(value):
        if isinstance(value, (int, bool, dict)):
            return value
        else:
            return str(value)

    def make_row(values):
        return dict(zip(fields, map(conditionals, values)))

    return make_row

conninfo = config.get(env, 'CONNINFO')

db = psycopg.connect(
    conninfo=conninfo,
    autocommit=True,
    row_factory=row_factory,
    keepalives=1,
    keepalives_idle=300,
    keepalives_interval=60,
    keepalives_count=5
)
