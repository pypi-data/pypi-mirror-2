Signals
=======

Query and create Socialtext Signals to accounts, groups, and users.

.. seealso::
	For detailed information abou the Signals URI, please see the `Socialtext Documentation`__

	__ https://www.socialtext.net/st-rest-docs/index.cgi?data_signals

Classes
-------

.. currentmodule:: socialtext

.. autoclass:: SignalManager
   :members: get, list, delete, create
   
             
.. autoclass:: Signal
   :members: delete, get_id, get_mentioned_user_ids, is_user_mentioned

   .. attribute:: signal_id
   
        The signal's primary key.
   
   .. attribute:: body
   
        The full text of the signal as an HTML string.

   .. attribute:: at
   
        String representation of the time when the signal was created
   
   .. attribute:: user_id
   
        The id of the :class:`User` who created the signal.
   
   .. attribute:: best_full_name
   
        The name of the person who created the signal
   
   .. attribute:: annotations
   
        User defined metadata. See the `signals annotation`__ docs.
				
				__ https://www.socialtext.net/st-rest-docs/index.cgi?signals_annotations
   
   .. attribute:: account_ids
   
        A list of the ID for each account this signal was posted to.
   
   .. attribute:: group_ids
   
        A list of the ID for each group this signal was posted to.
   
   .. attribute:: in_reply_to
   
        A :class:`BasicObject` representing the signal that this is a reply to. The object has the attributes "signal_id", "uri", and "user_id"
  
   .. attribute:: mentioned_users

        A list of dictionaries representing the users who were mentioned in the Signal. Each dictionary contains the keys "id", "username", and "best_full_name".