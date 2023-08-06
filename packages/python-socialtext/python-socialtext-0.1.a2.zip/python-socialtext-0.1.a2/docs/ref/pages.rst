Pages
=======

Query and create Socialtext Pages.

.. seealso::
	For detailed information about the Pages URI, please see the `Socialtext Documentation`__

	__ https://www.socialtext.net/st-rest-docs/index.cgi?data_workspaces_ws_pages

Classes
-------

.. currentmodule:: socialtext

.. autoclass:: PageManager
   :members: get, get_html, list, delete, create
   
             
.. autoclass:: Page
   :members: delete, get_html, get_id, name_to_id

   .. attribute:: name
   
        The title of the page.
   
   .. attribute:: uri

        The uri of the page.

   .. attribute:: page_id
   
        A unique slug of the page name.
   
   .. attribute:: page_uri
   
        The fully qualified URI of the page as used by the Socialtext browser UI.
   
   .. attribute:: tags
   
        A list of strings of all the tags the page has.
   
   .. attribute:: last_editor
   
        The username of the last :class:`User` to edit the page.
   
   .. attribute:: last_edit_time
   
        String representation of the date the page was last modified.
   
   .. attribute:: modified_time
   
        Time in seconds since the Unix Epoch the page was last modified.
   
   .. attribute:: revision_id
   
        The identifier for the current revision of the page.
  
   .. attribute:: revision_count

        The total count of revisions for this page.

   .. attribute:: workspace_name

        The name of the :class:`Workspace` containing the page.

   .. attribute:: type

        The type of page. Currently, only type "wiki" is supported.
