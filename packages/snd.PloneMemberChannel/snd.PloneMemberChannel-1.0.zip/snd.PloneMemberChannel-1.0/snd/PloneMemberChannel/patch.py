""" Apply patches.
"""

import logging
logger = logging.getLogger('snd.PloneMemberChannel')

import zope
from zope import component

import collective
from collective.dancing.channel import Channel
from collective.singing import subscribe

from channel import PloneMemberSubscriptions


def apply_channel_init_patch():
    """ Patching Channel so it uses our custom Subscriptions class.
    """
    logger.info("Applying patch to edit __init__ of "
                "collective.dancing.channel.")

    Channel._old_init = Channel.__init__

    def new_init(self, *args, **kwargs):
        self._old_init(*args, **kwargs)
        self.subscriptions = PloneMemberSubscriptions()

    Channel.__init__ = new_init

    logger.info("Patch applied.")


def unapply_channel_init_patch():
    Channel.__init__ = Channel._old_init

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
    apply_channel_init_patch()
    apply_subscription_added_patch()


def unapply_all():
    unapply_channel_init_patch()
    unapply_subscription_added_patch()
