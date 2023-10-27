import configparser
import os

from psycopg_pool import AsyncConnectionPool

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

class Pool:
    def __init__(self):
        self.pool = None

    async def process_startup(self, scope, event):
        self.pool = AsyncConnectionPool(conninfo=conninfo, min_size=2, max_size=4)

    async def process_shutdown(self, scope, event):
        if self.pool:
            await self.pool.close()

    async def process_request(self, req, resp):
        req.context.pool = self.pool
