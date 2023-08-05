from tw.api import Widget

__all__ = ["Gravatar"]

GRAVATAR_URL = "http://www.gravatar.com/avatar/"

from tw.gravatar.gravatar import get_uri
from tw.gravatar.gravatar import get_image

class Gravatar(Widget):

    template = """<img class="tw-gravatar" src="${uri}"/>"""

    # g: suitable for display on all websites with any audience type.
    # pg: may contain rude gestures, provocatively dressed individuals, the lesser swear words, or mild violence.
    # r: may contain such things as harsh profanity, intense violence, nudity, or hard drug use.
    # x: may contain hardcore sexual imagery or extremely disturbing violence

    params = {
          "uri": "http adress of the gravatar",
          "size": "size in pixels of the expected image",
          "rating": "a string chosen from 'G', 'PG' 'R' or 'X'",
          "default": "identicon, monsterid, mm, wavatar"
          }

    size = 32
    rating = 'G'
    uri = ''
    default = 'identicon'

    def __init__(self, id=None, parent=None, children=[], **kw):
        """Initialize the widget here. The widget's initial state shall be
        determined solely by the arguments passed to this function; two
        widgets initialized with the same args. should behave in *exactly* the
        same way. You should *not* rely on any external source to determine
        initial state."""
        super(Gravatar, self).__init__(id, parent, children, **kw)

    def update_params(self, d):
        email = d.get('email', "waitfor.me@somewhere.com") # for sample purpose
        d['uri'] = get_uri(email, default=self.default, size=self.size, rating=self.rating, border="f00")
        super(Gravatar, self).update_params(d)
