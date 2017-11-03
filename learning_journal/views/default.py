from pyramid.view import view_config
from learning_journal.data import entry_history
from pyramid.exceptions import HTTPNotFound


@view_config(route_name='home', renderer='learning_journal:templates/list.jinja2')
def list_view(request):
    """List of journal entries."""
    return {
        'entries': sorted(entry_history.ENTRIES, key=lambda e: -e['id'])
    }


def detail_view(request):
    """A single journal entry."""
    with open(os.path.join(TEMPLATES, 'detail.html')) as file:
        return Response(file.read())


def create_view(request):
    """Create a new entry."""
    with open(os.path.join(TEMPLATES, 'new.html')) as file:
        return Response(file.read())


def update_view(request):
    """Update an existing entry."""
    with open(os.path.join(TEMPLATES, 'update.html')) as file:
        return Response(file.read())
