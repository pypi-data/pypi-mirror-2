
Gravatar widget for toscawidget and turbogears
==============================================

This Widget allow for the insertion of gravatar's image

`http://www.gravatar.com/ <gravatar website>`_

A common use in `lib/helpers.py` ::

    from tw.gravatar import Gravatar
    gravatar=Gravatar(size=32, rating="G", default="wavatar")

anywhere in templates::

    ${h.gravatar(email='your.name@domain.com')}

parameters you can use::

    params = {
          "email": "email adress associated to a gravatar",
          "size": "size in pixels of the expected image",
          "rating": "a string chosen from 'G', 'PG' 'R' or 'X'",
          "default": "identicon, monsterid, mm, wavatar"
          }