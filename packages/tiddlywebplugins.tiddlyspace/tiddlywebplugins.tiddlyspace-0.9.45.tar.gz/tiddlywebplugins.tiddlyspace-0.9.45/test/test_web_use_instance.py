
from test.fixtures import make_test_env, make_fake_space

from wsgi_intercept import httplib2_intercept
import wsgi_intercept
import httplib2
import simplejson

from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe


def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('thing.0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('other.0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('foo.0.0.0.0', 8080, app_fn)


def teardown_module(module):
    import os
    os.chdir('..')


def test_home_page_exist():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/', method='GET')

    assert response['status'] == '200'
    assert 'Welcome to TiddlySpace' in content


def test_space_not_exist():
    http = httplib2.Http()
    response, content = http.request('http://thing.0.0.0.0:8080/', method='GET')

    assert response['status'] == '404'


def test_space_does_exist():
    make_fake_space(store, 'thing')
    http = httplib2.Http()
    response, content = http.request('http://thing.0.0.0.0:8080/', method='GET')

    assert response['status'] == '200'


def test_space_has_limited_view():
    make_fake_space(store, 'other')
    http = httplib2.Http()
    response, content = http.request('http://thing.0.0.0.0:8080/recipes',
            method='GET')

    assert response['status'] == '200'
    assert 'other_' not in content, content
    assert 'thing_' in content, content

    response, content = http.request('http://thing.0.0.0.0:8080/bags',
            method='GET')

    assert response['status'] == '200'
    assert 'other_' not in content, content
    assert 'thing_' in content, content

    response, content = http.request(
            'http://thing.0.0.0.0:8080/bags/thing_public/tiddlers',
            method='GET')
    assert response['status'] == '200'

    response, content = http.request(
            'http://thing.0.0.0.0:8080/bags/other_public/tiddlers',
            method='GET')
    assert response['status'] == '404', content

    response, content = http.request(
            'http://other.0.0.0.0:8080/bags',
            method='GET')
    assert response['status'] == '200', content
    assert 'other_' in content, content
    assert 'thing_' not in content, content

    response, content = http.request(
            'http://0.0.0.0:8080/bags',
            method='GET')
    assert response['status'] == '200', content
    assert 'other_' in content, content
    assert 'thing_' in content, content

    response, content = http.request(
            'http://thing.0.0.0.0:8080/bags/thing_public/tiddlers',
            method='GET')
    assert response['status'] == '200', content

    response, content = http.request(
            'http://thing.0.0.0.0:8080/bags/other_public/tiddlers',
            method='GET')
    assert response['status'] == '404', content

    tiddler1 = Tiddler('tiddler1', 'thing_public')
    tiddler2 = Tiddler('tiddler2', 'other_public')
    tiddler1.text = tiddler2.text = 'ohhai'
    store.put(tiddler1)
    store.put(tiddler2)

    response, content = http.request(
            'http://thing.0.0.0.0:8080/search?q=ohhai',
            headers={'Accept': 'application/json'},
            method='GET')
    assert response['status'] == '200', content

    info = simplejson.loads(content)
    assert len(info) == 1
    assert info[0]['title'] == tiddler1.title

    response, content = http.request(
            'http://other.0.0.0.0:8080/search?q=ohhai',
            headers={'Accept': 'application/json'},
            method='GET')
    assert response['status'] == '200', content

    info = simplejson.loads(content)
    assert len(info) == 1
    assert info[0]['title'] == tiddler2.title

    response, content = http.request(
            'http://0.0.0.0:8080/search?q=ohhai',
            headers={'Accept': 'application/json'},
            method='GET')
    assert response['status'] == '200', content

    info = simplejson.loads(content)
    assert len(info) == 2


def test_space_not_expose_subscription_recipes():
    make_fake_space(store, 'foo')
    make_fake_space(store, 'bar')
    make_fake_space(store, 'baz')

    # add subscription (manual as this is currently insufficiently encapsulated)
    public_recipe = store.get(Recipe('foo_public'))
    private_recipe = store.get(Recipe('foo_private'))
    public_recipe_list = public_recipe.get_recipe()
    private_recipe_list = private_recipe.get_recipe()
    public_recipe_list.insert(-1, ('bar_public', ''))
    private_recipe_list.insert(-2, ('bar_public', ''))
    public_recipe.set_recipe(public_recipe_list)
    private_recipe.set_recipe(private_recipe_list)
    store.put(public_recipe)
    store.put(private_recipe)

    http = httplib2.Http()

    response, content = http.request('http://foo.0.0.0.0:8080/recipes',
            method='GET')

    assert response['status'] == '200'
    assert 'foo_public' in content, content
    assert 'foo_private' not in content, content # not auth'd
    assert 'bar_public' not in content, content
    assert 'bar_private' not in content, content
    assert 'baz_' not in content, content

    response, content = http.request('http://foo.0.0.0.0:8080/recipes/foo_public',
            method='GET')
    assert response['status'] == '200'

    response, content = http.request('http://foo.0.0.0.0:8080/recipes/foo_private',
            method='GET')
    assert response['status'] == '200'

    response, content = http.request('http://foo.0.0.0.0:8080/recipes/bar_public',
            method='GET')
    assert response['status'] == '404'

    response, content = http.request('http://foo.0.0.0.0:8080/recipes/bar_private',
            method='GET')
    assert response['status'] == '404'

    response, content = http.request('http://foo.0.0.0.0:8080/recipes/baz_public',
            method='GET')
    assert response['status'] == '404'

    response, content = http.request('http://foo.0.0.0.0:8080/recipes/baz_private',
            method='GET')
    assert response['status'] == '404'


def test_disable_ControlView():
    make_fake_space(store, 'foo')
    make_fake_space(store, 'bar')
    http = httplib2.Http()

    response, content = http.request('http://foo.0.0.0.0:8080/recipes',
            method='GET')

    assert 'foo_public' in content, content
    assert 'bar_public' not in content, content

    response, content = http.request('http://foo.0.0.0.0:8080/recipes',
            headers={'X-ControlView': 'false'},
            method='GET')

    assert 'foo_public' in content, content
    assert 'bar_public' in content, content

    response, content = http.request('http://foo.0.0.0.0:8080/recipes',
            headers={'X-ControlView': 'true'},
            method='GET')

    assert 'foo_public' in content, content
    assert 'bar_public' not in content, content
