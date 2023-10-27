import falcon.asgi

from src.resources.user import User
from src.middlewares.auth import Auth
from src.storage.limits import Limiter

from config.database import Pool

app = falcon.asgi.App(middleware=[Auth(), Pool(), Limiter()])

app.add_route('/users', User())
