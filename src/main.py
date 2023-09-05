import falcon.asgi

from src.resources.user import User
from src.middlewares.auth import Auth

app = falcon.asgi.App(middleware=[Auth()])

app.add_route('/users', User())

