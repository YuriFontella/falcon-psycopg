import falcon

from src.hooks.secure import secure
from src.storage.limits import limiter

@falcon.before(secure)
class User:
    async def on_get(self, req, resp):
        try:
            pool = req.context.pool

            print(req.get_param('id', False))
            print(req.params)

            async with pool.connection() as conn:
                cur = await conn.execute("select name from users limit 1")
                records = await cur.fetchall()

            print(records)
            
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        else:
            resp.media = True


    @limiter.limit()
    async def on_post(self, req, resp):
        try:
            pool = req.context.pool

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

            async with pool.connection() as conn:
                await conn.execute(query, data)

        except Exception as e:
            print(e)
            raise falcon.HTTPBadRequest()

        else:
            resp.media = True
