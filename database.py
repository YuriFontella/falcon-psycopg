import psycopg
from psycopg.rows import dict_row

db = psycopg.connect(conninfo="postgresql://postgres:123456@localhost:5432/blocks", row_factory=dict_row)
