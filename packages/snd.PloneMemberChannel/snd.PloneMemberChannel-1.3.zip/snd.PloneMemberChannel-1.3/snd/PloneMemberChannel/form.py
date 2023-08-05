from zope import schema
from z3c.form import field

from snd.PloneMemberChannel.i18n import SNDMessageFactory as _

@property
def edit_channel_form_fields(self):
    fields = self._old_fields
    snd_extra_subscriptions = schema.List(
        __name__='snd_extra_subscriptions',
        title=_(u'Extra Subscriptions'),
        description=_(u'Add groups or all members to the subscriptions'),
        required=False,
        value_type=schema.Choice(vocabulary='SND Groups Vocabulary'))

    fields += field.Fields(snd_extra_subscriptions)
    return fields
