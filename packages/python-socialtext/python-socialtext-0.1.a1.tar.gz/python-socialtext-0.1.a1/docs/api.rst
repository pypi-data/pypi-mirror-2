The :mod:`socialtext` Python API
==================================

.. module:: socialtext
   :synopsis: A client for the Socialtext ReST API.
   
.. currentmodule:: socialtext

Usage
-----

First create an instance of :class:`Socialtext` with your credentials::

    >>> from socialtext import Socialtext
    >>> st = Socialtext(ST_URL, USERNAME, PASSWORD)

Then call methods on the :class:`Socialtext` object:

.. class:: Socialtext
    
    .. attribute:: pages
    
        A :class:`PageManager` - query and create :class:`Page` resources
    
    .. attribute:: signals
    
        A :class:`SignalManager` - query and create :class:`Signal` resources.
        
    .. attribute:: users
    
        An :class:`UserManager` - query :class:`User` resources

    .. attribute:: webhooks

        A :class:`WebhookManager` - query and create :class:`Webhook` resources.
    
    .. attribute:: workspaces
    
        A :class:`WorkspaceManager` - query :class:`Workspace` resources.
    
For example::

    >>> socialtext.pages.list('ws-name')
    [<Page: test_page_1>, <Page: test_page_2>]

    >>> socialtext.users.list()
    [<User: ABC123>,
     <User: 987>,
     <User: ZYX444>,
     <User: 789>]

    >>> signal = socialtext.signals.create("Hello world!")
    <Signal: 567>

    >>> signal.delete()

For more information, see the reference:

.. toctree::
   :maxdepth: 2
   
   ref/index