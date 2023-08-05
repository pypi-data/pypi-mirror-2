Introduction
============

This is an ugly hack to patch the Singing and Dancing newsletter
product for Plone.  With this patch all members of your Plone Site are
automatically subscribed to all newsletters.  New in version 1.3: you
need to edit the extra subscriptions field on the edit form of the
channel to use this option.

Note that version 1.1 and higher are bit less hacky than 1.0, as from
1.1 onwards we no longer need an own PloneMemberSubscriptions class,
but only some runtime patches.
