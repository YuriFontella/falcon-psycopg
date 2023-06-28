from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

pool = ConnectionPool(conninfo="postgresql://postgres:123456@localhost:5432/blocks")

class PoolMiddleware:
    def process_request(self, req, resp):
        pool.check()

def query():
    with pool.connection() as conn:
        conn = conn.cursor(row_factory=dict_row)
        return conn
