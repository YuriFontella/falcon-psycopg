import falcon, json

from database import PoolMiddleware, query


class StorageError:
    @staticmethod
    def handle(e, req, resp, params):
        raise falcon.HTTPInternalServerError(description=str(e))

class AuthMiddleware:
	def process_request(self, req, resp):
		token = req.get_header('x-access-token')
		print(token)
                
def secure(req, resp, resource, params):
	print('Você está seguro')

@falcon.before(secure)
class UserResource:
    def on_get(self, req, resp):
        print(req.get_param('id', False))
        print(req.params)

        db = query()
        records = db.execute("select name from users limit 10000").fetchall()

        resp.media = records
    
    def on_post(self, req, resp):
        db = query()
        try:
            data = req.media
            query = """
              insert into users (name) 
              values 
                (%(name)s) on conflict (name) do 
              update 
              set 
                name = excluded.name
              returning id
            """

            record = db.execute(query, data).fetchone()
            print(record['id'])

        except Exception as e:
            raise Exception(e)
        
        else:
            resp.text = json.dumps(True)
        

class SuffixResource:
	def on_get_all(self, req, resp):
		resp.text = 'all'

	def on_get_list(self, req, resp):
		resp.text = 'list'

app = falcon.App(middleware=[PoolMiddleware(), AuthMiddleware()])

app.add_route('/users', UserResource())

app.add_route('/all', SuffixResource(), suffix='all')
app.add_route('/list', SuffixResource(), suffix='list')

app.add_error_handler(Exception, StorageError.handle)