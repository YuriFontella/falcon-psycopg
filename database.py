from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo="postgresql://postgres:123456@localhost:5432/blocks")

class PoolMiddleware:
    def process_request(self, req, resp):
        pool.check()
