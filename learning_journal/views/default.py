"""Set up the default functions for the various views in my app."""


from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from learning_journal.models import Entry
from pyramid.security import remember, forget
from learning_journal.security import is_authenticated


@view_config(route_name='home', renderer='learning_journal:templates/list.jinja2')
def list_view(request):
    """List of journal entries."""
    entries = request.dbsession.query(Entry).all()
    entries = sorted(entries, key=lambda e: e.creation_date, reverse=True)
    entries = [entry.to_dict() for entry in entries]
    return {
        "entries": entries
    }


@view_config(route_name='detail', renderer='learning_journal:templates/detail.jinja2')
def detail_view(request):
    """A single journal entry."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if entry is None:
        raise HTTPNotFound
    else:
        return {
            "entry": entry
        }


@view_config(
    route_name='create',
    renderer='learning_journal:templates/create.jinja2',
    permission='secret'
)
def create_view(request):
    """Create a new entry."""
    if request.method == "GET":
        return {}

    if request.method == "POST":
        if not all([field in request.POST for field in ['title', 'body']]):
            raise HTTPBadRequest
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body'],
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('home'))


@view_config(
    route_name='update',
    renderer='learning_journal:templates/edit.jinja2',
    permission='secret'
)
def update_view(request):
    """Update an existing entry."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        return {
            'title': 'Edit Entry',
            'entry': entry.to_dict()
        }
    if request.method == "POST":
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        request.dbsession.add(entry)
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=entry.id))


@view_config(
    route_name='login',
    renderer='learning_journal:templates/login.jinja2',
)
def login(request):
    """Establish login post method."""
    if request.authenticated_userid:
        return HTTPFound(request.route_url('home'))

    if request.method == "GET":
        return {"route": login}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if is_authenticated(username, password):
            headers = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=headers)

        return {
            'error': 'Username/password combination not recognized.'
        }


@view_config(route_name='logout')
def logout(request):
    """Logout and send user to homepage."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
