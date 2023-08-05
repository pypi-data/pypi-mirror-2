""" Apply patches.
"""

import logging

# Import the modules and classes that we want to patch
from collective.dancing.browser.channel import EditChannelForm
from collective.dancing.channel import Channel
from collective.singing import subscribe
from collective.singing.subscribe import Subscriptions

# Import our patches.
from snd.PloneMemberChannel.form import edit_channel_form_fields
from snd.PloneMemberChannel.subscriptions import subscriptions_channel
from snd.PloneMemberChannel.subscriptions import subscription_event
from snd.PloneMemberChannel.subscriptions import subscriptions_values

logger = logging.getLogger('snd.PloneMemberChannel')


def apply_channel_edit_patch():
    """Patching EditChannelForm to put an extra field in it.
    """
    logger.info("Applying patch to "
                "collective.dancing.browser.EditChannelForm")

    if hasattr(EditChannelForm, '_old_fields'):
        logger.warn("Patch is already applied! Are you applying twice?!?")
        return
    EditChannelForm._old_fields = EditChannelForm.fields
    EditChannelForm.fields = edit_channel_form_fields

    # Add the property to the channel class as well, otherwise we get
    # an AttributeError when saving the edit form; an interface on the
    # field should help, but it doesn't.
    logger.info("Applying patch to "
                "collective.dancing.channel.Channel")
    if hasattr(Channel, 'snd_extra_subscriptions'):
        logger.warn("Patch is already applied! Are you applying twice?!?")
        return
    Channel.snd_extra_subscriptions = []


def unapply_channel_edit_patch():
    """Unapply patched to EditChannelForm.
    """
    EditChannelForm.fields = EditChannelForm._old_fields
    del EditChannelForm._old_fields
    del Channel.snd_extra_subscriptions


def apply_subscriptions_patch():
    """ Patching Subscriptions so it reports all members as well.
    """
    logger.info("Applying patch to "
                "collective.singing.subscribe.Subscriptions.")

    if hasattr(Subscriptions, 'channel'):
        logger.warn("Patch is already applied! Are you applying twice?!?")
        return
    Subscriptions.channel = subscriptions_channel

    if hasattr(Subscriptions, '_old_values'):
        logger.warn("Patch is already applied! Are you applying twice?!?")
        return
    Subscriptions._old_values = Subscriptions.values
    Subscriptions.values = subscriptions_values


def unapply_subscriptions_patch():
    """Unapply this patch.

    We have just added a property that we can now remove, and added a
    method that overrides a method from a parent class, so we can
    delete that too.
    """
    Subscriptions.values = Subscriptions._old_values
    del Subscriptions._old_values
    del Subscriptions.channel


def apply_subscription_added_patch():
    """ Patching subscription_add event.
    """
    logger.info("Applying patch to subscription_add event from "
                "collective.singing.subscribe.")

    if hasattr(subscribe, '_old_subscription_added'):
        logger.warn("Patch is already applied! Are you applying twice?!?")
        return
    subscribe._old_subscription_added = subscribe.subscription_added
    subscribe.subscription_added = subscription_event


def unapply_subscription_added_patch():
    """ Patching subscription_add event.
    """
    subscribe.subscription_added = subscribe._old_subscription_added
    del subscribe._old_subscription_added


def apply_all():
    """Apply all patches.

    This should normally happen only once at Zope startup.
    """
    apply_channel_edit_patch()
    apply_subscriptions_patch()
    apply_subscription_added_patch()


def unapply_all():
    """Unapply all patches.

    This should not normally be needed, as these patches are just
    dynamically done at Zope startup, but if for some reason you want
    to unapply the patches when Zope is already running, you can call
    this function.
    """
    unapply_subscriptions_patch()
    unapply_subscription_added_patch()
    unapply_channel_edit_patch()
