from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    DateTime,
)

from .meta import Base
from datetime import datetime, timedelta
import calendar


def utc_to_local(utc_dt):
    """Set the proper timezone."""
    # Courtesy of jfs on stackoverflow,com
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


class Entry(Base):
    """Create a model for new journal entries."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(DateTime)

    def __init__(self, creation_date=None, *args, **kwargs):
        """Initialize a new journal entry with the current date & time."""
        super(Entry, self).__init__(*args, **kwargs)
        if creation_date:
            self.creation_date = utc_to_local(creation_date)
        else:
            self.creation_date = datetime.now()

    def to_dict(self):
        """Take all model attributes and render them as a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'creation_date': self.creation_date.strftime('%A, %B %d, %Y at %I:%M%p')
        }
