from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

from snd.PloneMemberChannel.i18n import SNDMessageFactory as _

ALL_MEMBERS_MARKER = 'snd.allmembers'


def groups_vocabulary(context):
    terms = []
    all_members = SimpleTerm(
        value=ALL_MEMBERS_MARKER,
        token=ALL_MEMBERS_MARKER,
        title=_(u"All members"))
    terms.append(all_members)
    pas = getToolByName(context, 'acl_users')
    for group in pas.getGroups():
        if group.id == 'AuthenticatedUsers':
            # It does not make sense to add this one.
            continue
        terms.append(
            SimpleTerm(
                value=group.id,
                token=group.id,
                title=group.title_or_id()))
    return SimpleVocabulary(terms)

alsoProvides(groups_vocabulary, IVocabularyFactory)
