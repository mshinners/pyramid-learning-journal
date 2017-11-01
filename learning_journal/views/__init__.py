from .default import list_view, detail_view, create_view, update_view

def includeme(config):
    """Add views to our configuration."""
    config.add_view(list_view, route_name='home')
    config.add_view(detail_view, route_name='detail')
    config.add_view(create_view, route_name='create')
    config.add_view(update_view, route_name='update')
