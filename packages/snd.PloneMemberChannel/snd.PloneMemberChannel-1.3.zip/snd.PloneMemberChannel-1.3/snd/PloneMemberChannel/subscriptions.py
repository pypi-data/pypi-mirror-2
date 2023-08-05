import logging

from Products.CMFCore.utils import getToolByName
from collective.singing import subscribe
from collective.singing.interfaces import ISubscription
from collective.singing.subscribe import Subscriptions, SimpleSubscription
from datetime import datetime
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import IObjectAddedEvent
from zope.component import adapter

from snd.PloneMemberChannel.vocab import ALL_MEMBERS_MARKER

logger = logging.getLogger('snd.PloneMemberChannel')


@property
def subscriptions_channel(self):
    """ Finds the channel that uses this Subscriptions object.
    Quite ugly, but nothing in ISubscription allows finding back the
    channel and we need it to make the fake subscriptions.
    """
    portal = getSite()
    if portal is None:
        # Can at least happen in an instance debug session
        return

    for channel in portal.portal_newsletters.channels.objectValues():
        if not hasattr(channel, 'subscriptions'):
            return
        if channel.subscriptions == self:
            return channel


def subscriptions_values(self):
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

    if not channel.snd_extra_subscriptions:
        return res

    # We check which addresses are already in use.
    addresses = []
    for subscription in subscriptions:
        if hasattr(subscription, 'composer_data'):
            if 'email' in subscription.composer_data:
                addresses.append(subscription.composer_data['email'])

    # We create a fake subscription to be able to use render_message
    secret = ''
    metadata = dict(format='html',
                    date=datetime.now(),
                    pending=False,
                    fake=True)
    portal = getSite()
    membership = getToolByName(portal, 'portal_membership')
    pas = getToolByName(portal, 'acl_users')
    if ALL_MEMBERS_MARKER in channel.snd_extra_subscriptions:
        # All members should be added, so there is no sense in
        # checking the groups.
        users = membership.listMembers()
    else:
        users = set()
        for group in channel.snd_extra_subscriptions:
            group_data = pas.getGroupById(group)
            users = users.union(group_data.getGroupMembers())

    for user in users:
        user_email = user.getProperty('email')
        if user_email in addresses:
            # He already received the newsletter.
            continue
        f_subscription = SimpleSubscription(
            channel, secret, {'email': user_email}, {}, metadata)
        res.append(f_subscription)
        addresses.append(user_email)

    return res


@adapter(ISubscription, IObjectAddedEvent)
def subscription_event(obj, event):
    if obj.metadata.get('fake'):
        # Fake member subscription, we should not call any other
        # code.  This happens when adding a new channel (which may
        # not make sense as a new channel should not have
        # subscriptions yet, but the reasoning is sound enough for
        # ZMI import reasons).
        logger.debug("ignoring event for fake subscription")
        return
    subscribe._old_subscription_added(obj, event)
