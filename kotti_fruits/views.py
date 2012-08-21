from pkg_resources import resource_filename
from pyramid.view import is_response
import colander
from deform import Form
from deform import FileData
from deform.widget import FileUploadWidget
from deform.widget import DatePartsWidget

from kotti.views.view import view_node
from kotti.views.util import TemplateAPI
from kotti.views.util import ensure_view_selector
from kotti.views.edit import ContentSchema
from kotti.views.edit import generic_edit                                                                                                                                                                                                                                
from kotti.views.edit import generic_add

from translationstring import TranslationStringFactory
_ = TranslationStringFactory('deform')

from kotti_fruits.resources import FruitCategoriesFolder
from kotti_fruits.resources import FruitCategory
from kotti_fruits.resources import Fruit

from pyramid.security import remember
from pyramid.security import forget
from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPFound
from formencode.validators import Email
from kotti.resources import get_root
from kotti.resources import Node
from kotti.security import get_principals

import datetime

import uuid

import json

kotti_images = resource_filename('kotti', 'static/images')

class MemoryTmpStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""
    def preview_url(self, uid):
        return 

tmpstore = MemoryTmpStore()

def includeme_view(config):
    config.add_view(
        view_node,
        context=FruitCategoriesFolder,
        name='view',
        permission='view',
        renderer='templates/view/fruit_categories_folder.pt',
        )
    config.add_view(
        view_node,
        context=FruitCategory,
        name='view',
        permission='view',
        renderer='templates/view/fruit_category.pt',
        )
    config.add_view(
        view_node,
        context=Fruit,
        name='view',
        permission='view',
        renderer='templates/view/fruit.pt',
        )

class FruitCategoriesFolderSchema(ContentSchema):
    pass

class FruitCategorySchema(ContentSchema):
    pass

class FruitSchema(ContentSchema):
    pass

@ensure_view_selector
def edit_fruit_categories_folder(context, request):
    return generic_edit(context, request, FruitCategoriesFolderTypeSchema())

def add_fruit_categories_folder(context, request):
    return generic_add(context, request, FruitCategoriesFolderSchema(), FruitCategoriesFolder, u'fruit_categories_folder')

@ensure_view_selector
def edit_fruit_category(context, request):
    return generic_edit(context, request, FruitCategorySchema())

def add_fruit_category(context, request):
    return generic_add(context, request, FruitCategorySchema(), FruitCategory, u'fruit_category')

@ensure_view_selector
def edit_fruit(context, request):
    return generic_edit(context, request, FruitSchema())

def add_fruit(context, request):
    return generic_add(context, request, FruitSchema(), Fruit, u'fruit')

def includeme_edit(config):

    config.add_view(
        edit_fruit_categories_folder,
        context=FruitCategoriesFolder,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/master.pt',
    )

    config.add_view(
        add_fruit_categories_folder,
        name=FruitCategoriesFolder.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/add.pt',
    )

    config.add_view(
        edit_fruit_category,
        context=FruitCategory,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/master.pt',
    )

    config.add_view(
        add_fruit_category,
        name=FruitCategory.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/add.pt',
    )

    config.add_view(
        edit_fruit,
        context=Fruit,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/master.pt',
    )

    config.add_view(
        add_fruit,
        name=Fruit.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/add.pt',
    )
    
def fruit_categories_view(request):
    return FruitCategory.fruit_categories_bunch(FruitCategory.name.desc())

def fruits_view(request):
    return Fruit.fruits_bunch(Fruit.name.desc())

def includeme_bunch_view(config):
    config.add_view(fruit_categories_view, name='fruit_categories', permission='view', renderer='json')
    config.add_view(fruits_view, name='fruits', permission='view', renderer='json')

def fruit_category_view(request):
    if request.method == 'POST':
        return FruitCategory.create_fruit_category(request)
    else:
        return FruitCategory.fruit_category(FruitCategory.name.desc(), request.matchdict['id'])

def fruit_view(request):
    if request.method == 'POST':
        return Fruit.create_fruit(request)
    else:
        return Fruit.fruit(Fruit.name.desc(), request.matchdict['id'])

def includeme_single_view(config):
    config.add_route('fruit_category', 'fruit_category/{id}')
    config.add_view(fruit_category_view, route_name='fruit_category', permission='view', renderer='json')

    config.add_route('fruit', 'fruit/{id}')
    config.add_view(fruit_view, route_name='fruit', permission='view', renderer='json')

def _find_user(login):
    principals = get_principals()
    principal = principals.get(login)
    if principal is None:
        try:
            Email().to_python(login)
        except Exception:
            pass
        else:
            results = [r for r in principals.search(email=login)]
            if results:
                principal = results[0]
    return principal

def auth(context, request):
    root = get_root(request)
    api = TemplateAPI[TemplateAPI.EDIT_MASTER](root, request)
    principals = get_principals()

    body_dict = json.loads(request.body)

    username = body_dict['user']
    print 'username = ', username
    password = body_dict['passwd']
    print 'password = ', password
    user = _find_user(username)

    print username, password, user

    came_from = request.params.get('came_from', request.url)
    #login, password = u'', u''

    print 'user.active ', user.active

    print 'principals.hash_password(password) ', principals.hash_password(u'')

    print 'came_from ', came_from

    print 'session ', request.session

    if (user is not None and user.active and 
        password == principals.hash_password('')):
        print 'hey we are in here'
        headers = remember(request, username)
        h1 = headers[0]
        auth_tkt = h1[1]
        print auth_tkt
        auth_tkt = auth_tkt[10:-9]
        print auth_tkt
        #('Set-Cookie', 'auth_tkt="27144cfdef1c5e545c4436e65cdfc9464db06454amVmZQ%3D%3D!userid_type:b64unicode"; Path=/')
        request.session.flash(
            u"Welcome, %s!" % user.title or user.name, 'success')
        return HTTPOk(headers=headers, body=json.dumps({'sessionCookie':auth_tkt}))
    request.session.flash(u"Login failed.", 'error')

    #if 'submit' in request.POST:
    if 'auth' in request.POST:
        #login = request.params['login']
        #password = request.params['password']
        login = request.body['user']
        password = request.body['passwd']
        user = _find_user(login)

        print login, password, user, came_from

        if (user is not None and user.active and 
            user.password == password):
            #user.password == principals.hash_password(password)):
            headers = remember(request, login)
            request.session.flash(
                u"Welcome, %s!" % user.title or user.name, 'success')
            return HTTPFound(location='http://localhost:4020/fruits', headers=headers)
        request.session.flash(u"Login failed.", 'error')

    if 'reset-password' in request.POST:
        login = request.params['login']
        user = _find_user(login)
        if user is not None:
            send_set_password(user, request, templates='reset-password')
            request.session.flash(
                u"You should receive an email with a link to reset your "
                u"password momentarily.", 'success')
        else:
            request.session.flash(
                "That username or email is not known to us.", 'error')

    return {
        'api': api,
        'url': request.application_url + '/@@login',
        'came_from': came_from
        #'login': login,
        #'password': password,  # [TODO] why is this passed back?! [OK, don't pass it back then]
        }

def includeme(config):
    includeme_edit(config)
    includeme_view(config) 
    includeme_bunch_view(config) 
    includeme_single_view(config) 

    #config.add_route('kottiauth', '/kotti/auth')
    config.add_view(auth, name='auth', context=Node, renderer='json', xhr=True)

