import falcon.asgi

from src.resources.user import User
from src.middlewares.auth import Auth
from src.storage.limits import Limiter

app = falcon.asgi.App(middleware=[Auth(), Limiter()])

app.add_route('/users', User())
