from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import mysql.connector


@view_config(
    route_name='hello',
    renderer='templates/home.jinja2'
)
def home(request):
    conn = mysql.connector.connect(
        host="localhost", user="web_user", passwd='0eTnBQz4yE3jfO6R', database="pyramidproject")
    cur = conn.cursor()
    cur.execute('SELECT Id, name, total, link FROM Inventory')
    inv = []
    for (id, name, total, link) in cur:
        inv.append({'id': id, 'name': name, 'total': total, 'link': link})
    return{"greeting": 'Welcome to', "name": 'SanChr Store inventory ', "inv": inv}


@view_config(
    route_name='edit',
    renderer='templates/edit.jinja2'
)
def edit(request):
    conn = mysql.connector.connect(
        host="localhost", user="web_user", passwd='0eTnBQz4yE3jfO6R', database="pyramidproject")
    cur = conn.cursor()

    if request.method == 'POST':
       # print({'name': request.POST['name'], 'total': request.POST['total'],
        #  'link': request.POST['link'], 'id': request.matchdict['id']})
        cur.execute(
            "UPDATE Inventory SET `name`=%(name)s, `total`=%(total)s, `link`=%(link)s WHERE Id = %(id)s",
            {'name': request.POST['name'], 'total': request.POST['total'], 'link': request.POST['link'], 'id': request.matchdict['id']})
        conn.commit()
        return HTTPFound('/')
    else:
        cur.execute(
            "SELECT Id, name, total, link FROM Inventory WHERE Id = %(id)s", {'id': request.matchdict['id']})
        (id, name, total, link) = cur.fetchone()
        return {"greeting": 'Edit Stock Inventory', "name": '', 'item': {'id': id, 'name': name, 'total': total, 'link': link}}


if __name__ == "__main__":
    config = Configurator()
    config.include('pyramid_jinja2')
    config.include('pyramid_debugtoolbar')
    config.add_static_view(name='static',
                           path='static')
    config.add_route('hello', '/')
    config.add_route('edit', '/edit/{id}')

    config.scan()
    app = config.make_wsgi_app()
server = make_server('0.0.0.0', 8080, app)
server.serve_forever()
