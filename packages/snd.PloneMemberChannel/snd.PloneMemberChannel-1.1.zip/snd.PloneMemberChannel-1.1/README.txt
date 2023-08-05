Introduction
============

This is an ugly hack to patch the Singing and Dancing newsletter
product for Plone.  With this patch all members of your Plone Site are
automatically subscribed to all newsletters.

Note that this seems to affect the search negatively: searching for
currently subscribed addresses does not work anymore.

Note that version 1.1 is a bit less hacky than 1.0, as in 1.1 we no
longer need an own PloneMemberSubscriptions class, but only a runtime
patch.
