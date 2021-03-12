from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config


@view_config(
    route_name="home",
    renderer="json")
def home(request):
    return{"a": 1, "b": 2}  # json data alway in ""


if __name__ == "__main__":
    config = Configurator()
    config.add_route('home', '/')
    config.scan()
    app = config.make_wsgi_app()
# 6543 is defalt port for pyramid
server = make_server('0.0.0.0', 8080, app)
server.serve_forever()
