import falcon

from src.hooks.secure import secure
from config.database import db

@falcon.before(secure)
class User:
    async def on_get(self, req, resp):
        try:
            print(req.get_param('id', False))
            print(req.params)
            records = db.execute("select * from users limit 1").fetchall()
            
        except Exception:
            raise falcon.HTTPBadRequest()

        else:
            resp.media = records


    async def on_post(self, req, resp):
        try:
            data = await req.media
            query = """
              insert into users (name, group_id)
              values 
                (%(name)s, %(group_id)s) on conflict (name) do
              update
              set
                name = excluded.name
              returning id
            """

            with db.transaction():
                record = db.execute(query, data).fetchone()
                print(record)

        except Exception as e:
            print(e)
            raise falcon.HTTPBadRequest()

        else:
            resp.media = True