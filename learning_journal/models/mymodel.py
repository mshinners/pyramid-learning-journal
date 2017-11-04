from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    DateTime,
)

from .meta import Base
from datetime import datetime


class Entry(Base):
    """Create a model for new journal entries."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(DateTime)

    def __init__(self, *args, creation_date=None, **kwargs):
        """Initialize a new journal entry with the current date & time."""
        super(Entry, self).__init__(*args, **kwargs)
        self.creation_date = creation_date
        if not creation_date:
            self.creation_date = datetime.now()

    def to_dict(self):
        """Take all model attributes and render them as a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'creation_date': self.creation_date.strftime('%A, %B %d, %Y at %I:%M%p')
        }
