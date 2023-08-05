# Dagny

Dagny is a [Django][] adaptation of [Ruby on Rails][]’s Resource-Oriented
Architecture (a.k.a. ‘RESTful Rails’). The name is [a reference][dagny taggart].

  [django]: http://djangoproject.com/
  [ruby on rails]: http://rubyonrails.org/
  [dagny taggart]: http://en.wikipedia.org/wiki/List_of_characters_in_Atlas_Shrugged#Dagny_Taggart

At present, this project is in an experimental phase. APIs are liable to change,
and code listings in this README may not work or may even be purely speculative
explorations of what the final API might look like. **You have been warned.**


## Example Project

The rest of this README is a pretty thorough introduction to Dagny’s concepts
and API. If you’d rather dive right in, there’s an [example project][] which
showcases a user management app, built in very few lines of code on top of the
standard `django.contrib.auth` app.

  [example project]: http://github.com/zacharyvoase/dagny/tree/master/example/

To get it running:

    git clone 'git://github.com/zacharyvoase/dagny.git'
    cd dagny/
    pip install -r REQUIREMENTS  # Installs runtime requirements
    pip install -r REQUIREMENTS.test  # Installs testing requirements
    cd example/
    ./manage.py syncdb  # Creates db/development.sqlite3
    ./manage.py test users  # Runs all the tests
    ./manage.py runserver

Then just visit <http://localhost:8000/users/> to see it in action!


## Resources

Dagny’s fundamental unit is the **resource**. A resource is identified by, and
can be accessed at, a single HTTP URI. A resource may be singular or plural; for
example, `/users` is a collection of users, and `/users/31215` is a single user.

In your code, resources are defined as classes with several **actions**. An
action is essentially a method, routed to based on the request path and method,
which is in charge of processing that particular request and returning a
response.


### URIs

For collections, the URIs and their interaction with the standard HTTP methods
follows the Rails convention:

    Method  Path             Action        Behavior
    ---------------------------------------------------------------
    GET     /users/          User.index    List all users
    GET     /users/new/      User.new      Display new user form
    POST    /users/          User.create   Create new user
    GET     /users/1/        User.show     Display user 1
    GET     /users/1/edit/   User.edit     Display edit user 1 form
    PUT     /users/1/        User.update   Update user 1
    DELETE  /users/1/        User.destroy  Delete user 1

Note that not all of these actions are required; for example, you may not wish
to provide `/users/new` and `/users/1/edit`, instead preferring to display the
relevant forms under `/users/` and `/users/1/`.

To work around the fact that `PUT` and `DELETE` are not typically supported in
browsers, you can add a `method` parameter over `POST` to override the request
method.

For singular resources, the URI scheme is similar:

    Method  Path            Action            Behavior
    --------------------------------------------------------------------
    GET     /account/        Account.show      Display the account
    GET     /account/new/    Account.new       Display new account form
    POST    /account/        Account.create    Create the new account
    GET     /account/edit/   Account.edit      Display edit account form
    PUT     /account/        Account.update    Update the account
    DELETE  /account/        Account.destroy   Delete the account

The same point applies here: you don’t need to specify all of these actions
every time.


#### URLconf

Pointing to a collection resource from your URLconf is relatively simple:

    from dagny.urls import resources  # plural!
    from django.conf.urls.defaults import *
    
    urlpatterns = patterns('',
        (r'^users/', resources('myapp.resources.User'))
    )

You can customize this; for example, to use a slug/username instead of a numeric
ID:

    urlpatterns = patterns('',
        (r'^users/', resources('myapp.resources.User', id=r'[\w\-_]+')),
    )

You can also restrict the actions that are routed to. `resources()` will
recognize `index`, `new`, `show` and `edit` (the other three actions are all
based on the request method). Pass the `actions` keyword argument to specify
which of these you would like to be available:

    urlpatterns = patterns('',
        (r'^users/', resources('myapp.resources.User', actions=('index', 'show'))),
    )

This is useful if you’re going to display the `new` and `edit` forms on the
`index` and `show` pages, for example. It may also prevent naming clashes if
you’re using slug identifiers in URIs.

To point to a singular resource, use the `resource()` helper:

    from dagny.urls import resource  # singular!
    from django.conf.urls.defaults import *
    
    urlpatterns = patterns('',
        (r'^account/', resource('myapp.resources.User'))
    )

`resource()` is similar to `resources()`, but it only generates `show`, `new`
and `edit`, and doesn’t take an `id` parameter of any sort.


#### Reversing URLs

`resource()` and `resources()` both attach names to the patterns they generate.
This allows you to use the `{% url %}` templatetag, for example:

    A user creation form:
    <form method="post" action="{% url myapp.resources.User#index %}">
      ...
    </form>
    
    Signup link:
    <a href="{% url myapp.resources.User#new %}">Sign Up!</a>
    
    A user profile link:
    <a href="{% url myapp.resources.User#show user.id %}">View user</a>
    
    A user editing link:
    <a href="{% url myapp.resources.User#edit user.id %}">Edit user</a>
    
    A user editing form:
    <form method="post" action="{% url myapp.resources.User#show user.id %}">
      ...
    </form>

You can also write some nice `get_absolute_url()` methods:

    from django.db import models
    
    class User(models.Model):
        # ... snip! ...
        
        @models.permalink
        def get_absolute_url(self):
            return ("myapp.resources.User#show", self.id)

Of course, having to write out the full path to the resource is quite
cumbersome, so you can give a `name` keyword argument to either of the URL
helpers, and use the shortcut:

    # In urls.py:
    urlpatterns = patterns('',
        (r'^users/', resources('myapp.resources.User', name='User'))
    )
    
    # In models.py:
    class User(models.Model):
        @models.permalink
        def get_absolute_url(self):
            return ("User#show", self.id)

Likewise for the templates, and any calls to `django.shortcuts.redirect()` or
`django.core.urlresolvers.reverse()`.


### Defining Resources

Resources are subclasses of `dagny.Resource`. Actions are methods on these
subclasses, decorated with `@action`. Here’s a short example:

    from dagny import Resource, action
    from django.shortcuts import get_object_or_404, redirect
    
    from authapp import forms, models
    
    class User(Resource):
        
        @action
        def index(self):
            self.users = models.User.objects.all()
        
        @action
        def new(self):
            self.form = forms.UserForm()
        
        @action
        def create(self):
            self.form = forms.UserForm(request.POST)
            if self.form.is_valid():
                self.user = self.form.save()
                return redirect(self.user)
            
            response = self.new.render()
            response.status_code = 403 # Forbidden
            return response
        
        @action
        def show(self, username):
            self.user = get_object_or_404(models.User, username=username)
        
        @action
        def edit(self, username):
            self.user = get_object_or_404(models.User, username=username)
            self.form = forms.UserForm(instance=self.user)
            return self.new.render()
        
        @action
        def update(self, username):
            self.user = get_object_or_404(models.User, username=username)
            self.form = forms.UserForm(self.request.POST, instance=self.user)
            if self.form.is_valid():
                self.form.save()
                return redirect(self.user)
            
            response = self.edit.render()
            response.status_code = 403
            return response
        
        @action
        def destroy(self, username):
            self.user = get_object_or_404(models.User, username=username)
            self.user.delete()
            return redirect('/users')

`Resource` uses [django-clsview][] to define class-based views; the extensive
use of `self` is safe because a new instance is created for each request.

  [django-clsview]: http://github.com/zacharyvoase/django-clsview

You might notice that there are no explicit calls to `render_to_response()`;
most of the time you’ll want to render the same templates: `"user/index.html"`,
`"user/new.html"`, `"user/show.html"` and `"user/edit.html"`. Therefore, if your
action doesn’t return anything (i.e. returns `None`), a template corresponding
to the resource and action will be rendered. See the next section for a more
in-depth explanation.


### Renderers

An action actually comes in two parts: one part does the processing, the other
returns a response to the client. This allows for transparent content
negotiation, and means you never have to write a separate ‘API’ for your site,
or call `render_to_response()` at the bottom of every view function.

Usage is as follows:

    class User(Resource):
        
        @action
        def show(self, username):
            self.user = get_object_or_404(User, username=username)
        
        @show.render.json
        def show(self):
            return HttpResponse(content=simplejson.dumps(self.user.to_dict()),
                                mimetype='application/json')

Now, if you fetch `/users/zacharyvoase/`, you’ll see the result of rendering the
`"users/show.html"` template as a HTML page. If you fetch
`/users/zacharyvoase/?format=json`, however, you’ll get a JSON representation of
that user.

Dagny’s ConNeg mechanism is quite sophisticated; `webob.acceptparse` is used to
parse HTTP `Accept` headers, and these are considered alongside explicit
`format` parameters. So, you could also have passed `Accept: application/json`
in that last example, and it would have worked. When using `curl`, this is as
easy as:

    curl -H"Accept: application/json" 'http://mysite.com/users/zacharyvoase/'


#### When Renderers Are Called

When an action is triggered by a request, the main body of the action is first run.
If this does not return a `HttpResponse` outright, the renderer kicks in and
performs content negotiation, to decide which **renderer backend** to use. In
most circumstances, this will be `html`. The default behavior of the `html`
renderer backend looks something like this:

    class User(Resource):
        
        # ... snip! ...
        
        @show.render.html
        def show(self):
            return render_to_response("user/show.html", {
                'self': self
            }, context_instance=RequestContext(self.request))

See the section on generic backends for a more thorough explanation.


#### Skipping Renderers

Sometimes, you’ll define multiple renderer backends for an action, but in
certain cases a single backend won’t be able to generate a response for that
particular request. No biggie—just raise `dagny.renderer.Skip`:

    from dagny.renderer import Skip
    from django.http import HttpResponse
    
    class User(Resource):
        # ... snip! ...
        
        @show.render.rdf_xml
        def show(self):
            if not hasattr(self, 'graph'):
                raise Skip
            return HttpResponse(content=self.graph.serialize(),
                                content_type='application/rdf+xml')

This *really* comes in handy when writing generic backends (keep reading).


#### Additional MIME types

Additional renderers for a single action are defined using the decoration syntax
(`@<action_name>.render.<format>`) as seen above, but since content negotiation
is based on mimetypes, Dagny keeps a global `dict` mapping these **shortcodes**
to full mimetype strings (as `dagny.conneg.MIMETYPES`). You can create your own
shortcodes, and use them in resource definitions:

    from dagny.conneg import MIMETYPES
    
    MIMETYPES['rss'] = 'application/rss+xml'
    MIMETYPES['png'] = 'image/png'
    MIMETYPES.setdefault('json', 'text/javascript')

There is already a relatively extensive list of types defined; see the
[`dagny.conneg` module][dagny.conneg] for more information.

  [dagny.conneg]: http://github.com/zacharyvoase/dagny/blob/master/src/dagny/conneg.py


#### Generic Backends

Dagny also supports **generic renderer backends**; these are type-specific
renderers attached to a `Renderer` instance which will be available on *all*
actions by default. These renderers are simple functions which take both the
action instance and the resource instance. For example, the HTML renderer (which
every action has as standard) looks like:

    from dagny.action import Action
    from dagny.utils import camel_to_underscore, resource_name
    
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    
    @Action.RENDERER.html
    def render_html(action, resource):
        template_path_prefix = getattr(resource, 'template_path_prefix', "")
        resource_label = camel_to_underscore(resource_name(resource))
        template_name = "%s%s/%s.html" % (template_path_prefix, resource_label, action.name)
        
        return render_to_response(template_name, {
          'self': resource
        }, context_instance=RequestContext(resource.request))

`Action.RENDERER` is a globally-shared instance of `dagny.renderer.Renderer`;
the `render` attribute on actions is actually a `BoundRenderer`; this dichotomy
is what allows you to define specific backends that just take `self` (the
resource instance), and generic backends which also take the action.

Each `BoundRenderer` just copies the whole set of generic backends, so you can
operate on them as if they had been defined the normal way:

    class User(Resource):
    
        @action
        def show(self, username):
            self.user = get_object_or_404(User, username=username)
        
        # Remove the generic HTML backend
        del show.render['html']
        
        # Item assignment, even on a `BoundRenderer`, takes generic backend
        # functions (i.e. functions which accept both the action *and* the
        # resource).
        show.render['html'] = my_generic_html_backend
