""" Apply patches.
"""

import logging
logger = logging.getLogger('snd.PloneMemberChannel')

import zope
from zope.app.component.hooks import getSite
from zope import component
from datetime import datetime

import collective
from collective.singing import subscribe
from Products.CMFCore.utils import getToolByName

from collective.singing.subscribe import Subscriptions, SimpleSubscription


def apply_subscriptions_patch():
    """ Patching Subscriptions so it reports all members as well.
    """
    logger.info("Applying patch to "
                "collective.singing.subscribe.Subscriptions.")

    @property
    def channel(self):
        """ Finds the channel that uses this Subscriptions object.
        Quite ugly, but nothing in ISubscription allows finding back the
        channel and we need it to make the fake subscriptions.
        """
        portal = getSite()

        for channel in portal.portal_newsletters.channels.objectValues():
            if not hasattr(channel, 'subscriptions'):
                return

            if channel.subscriptions == self:
                return channel

    Subscriptions.channel = channel

    def values(self):
        """ Returns all Subscriptions + fake subscriptions
        created from the plone members.
        """
        subscriptions = super(Subscriptions, self).values()

        # We build a copy of subscriptions.
        res = [sub for sub in subscriptions]

        channel = self.channel
        if channel is None:
            # We did not find the channel using this subscriptions.
            return res

        # Now we can finally add our fake subscriptions.

        # We check which addresses are already in use.
        addresses = []
        for subscription in subscriptions:
            if hasattr(subscription, 'composer_data'):
                if 'email' in subscription.composer_data:
                    addresses.append(subscription.composer_data['email'])

        portal = getSite()
        membership = getToolByName(portal, 'portal_membership')
        users = membership.listMembers()

        for user in users:
            user_email = user.getProperty('email')
            if user_email in addresses:
                # He already received the newsletter.
                continue

            # We create a fake subscription to be able to
            # use render_message
            secret = ''
            metadata = dict(format='html',
                            date=datetime.now(),
                            pending=False)
            f_subscription = SimpleSubscription(channel,
                                                secret,
                                                {'email': user_email},
                                                {},
                                                metadata)

            res.append(f_subscription)

        return res

    Subscriptions.values = values

    logger.info("Patch applied.")


def unapply_subscriptions_patch():
    """Unapply this patch.

    We have just added a property that we can now remove, and added a
    method that overrides a method from a parent class, so we can
    delete that too.
    """
    del Subscriptions.values
    del Subscriptions.channel


def apply_subscription_added_patch():
    """ Patching subscription_add event.
    """
    logger.info("Applying patch to subscription_add event from "
                "collective.singing.subscribe.")

    subscribe._old_subscription_added = subscribe.subscription_added

    @component.adapter(collective.singing.interfaces.ISubscription,
                       zope.app.container.interfaces.IObjectAddedEvent)
    def new_event(obj, event):
        try:
            subscribe._old_subscription_added()
        except TypeError:
            # We failed but do not care.
            pass

    subscribe.subscription_added = new_event


def unapply_subscription_added_patch():
    """ Patching subscription_add event.
    """
    subscribe.subscription_added = subscribe._old_subscription_added


def apply_all():
    apply_subscriptions_patch()
    apply_subscription_added_patch()


def unapply_all():
    unapply_subscriptions_patch()
    unapply_subscription_added_patch()
