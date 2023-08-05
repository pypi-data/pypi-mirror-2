from zope import interface

from collective.singing.interfaces import ISubscriptions
from collective.singing.subscribe import Subscriptions


class PloneMemberSubscriptions(Subscriptions):
    """Special Subscriptions class that reports back all Plone members as well.

    This is deprecated as we now just add some patches to the
    Subscriptions class directly, which avoids the need for a patch to
    the Channel class.  So in new installations this class is not used
    anymore; we only keep it so old installations remain working.
    """
    interface.implements(ISubscriptions)

    def values(self):
        """ Returns all Subscriptions + fake subscriptions
        created from the plone members.
        """
        subscriptions = super(PloneMemberSubscriptions, self).values()
        return subscriptions
