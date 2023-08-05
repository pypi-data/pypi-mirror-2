from datetime import datetime

from zope.app.component.hooks import getSite
from zope import interface

from Products.CMFCore.utils import getToolByName

from collective.dancing.channel import Channel
from collective.dancing.browser.channel import EditChannelForm

from collective.singing.interfaces import ISubscriptions
from collective.singing.subscribe import Subscriptions, SimpleSubscription

class PloneMemberSubscriptions(Subscriptions):
    interface.implements(ISubscriptions)

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

    def values(self):
        """ Returns all Subscriptions + fake subscriptions
        created from the plone members.
        """
        subscriptions = super(PloneMemberSubscriptions, self).values()

        # We build a copy of subscriptions.
        res = [sub for sub in subscriptions]

        channel = self.channel
        if channel is None:
            # We did not find the channel using this subscriptions.
            return res

#        We'll finally monkeypatch collective.dancing.channel and our
#        new subscription class will be applied to all channels.
#        So we do not need the code below anymore as we won't have custom
#        channels implementations.

#         if not 'includePloneMembers' in dir(channel):
#             # This is not a PloneMemberChannel.
#             return res

#         if not channel.includePloneMembers:
#             # User decided not to send the mail to plone members.
#             return res

        # Now we can finally add our fake subscriptions.

        # We check which addresses are already is use.
        addresses = []

        for subscription in subscriptions:
            if 'composer_data' in dir(subscription):
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
