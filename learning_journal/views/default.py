from pyramid.view import view_config
from learning_journal.data import entry_history
from pyramid.exceptions import HTTPNotFound


@view_config(route_name='home', renderer='learning_journal:templates/list.jinja2')
def list_view(request):
    """List of journal entries."""
    return {
        'entries': sorted(entry_history.ENTRIES, key=lambda e: -e['id'])
    }


@view_config(route_name='detail', renderer='learning_journal:templates/detail.jinja2')
def detail_view(request):
    """A single journal entry."""
    entry_id = int(request.matchdict['id'])
    if entry_id < 0 or entry_id > len(entry_history.ENTRIES):
        raise HTTPNotFound
    entry = list(filter(lambda entry: entry['id'] == entry_id, entry_history.ENTRIES))[0]
    return {
        'entry': entry
    }


@view_config(route_name='create', renderer='learning_journal:templates/create.jinja2')
def create_view(request):
    """Create a new entry."""
    return {}


@view_config(route_name='update', renderer='learning_journal:templates/edit.jinja2')
def update_view(request):
    """Update an existing entry."""
    entry_id = int(request.matchdict['id'])
    if entry_id < 0 or entry_id > len(entry_history.ENTRIES):
        raise HTTPNotFound
    entry = list(filter(lambda entry: entry['id'] == entry_id, entry_history.ENTRIES))[0]
    return {
        'entry': entry
    }
