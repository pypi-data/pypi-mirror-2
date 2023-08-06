from Products.CMFCore.utils import ContentInit
from Products.LinguaPlone.public import *
from Products.LinguaPlone import config
from Products.LinguaPlone import permissions

from zope.i18nmessageid import MessageFactory
LinguaPloneMessageFactory = MessageFactory('linguaplone')

def checkVersion():
    from Products.CMFPlone.utils import getFSVersionTuple
    if getFSVersionTuple()[:3] < (3,0,1):
        import logging, sys
        logger=logging.getLogger("LinguaPlone")
        logger.log(logging.ERROR,
                "Unsupported Plone version: " 
                "LinguaPlone 2.0 requires Plone 3.0.1 or later")
        sys.exit(1)

checkVersion()

def initialize(context):
    # Apply monkey patches
    from Products.LinguaPlone import patches

    if config.INSTALL_DEMO_TYPES:
        import examples

    # Initialize content types
    content_types, constructors, ftis = process_types(
        listTypes(config.PKG_NAME), config.PKG_NAME)

    ContentInit(
        '%s Content' % config.PKG_NAME,
        content_types = content_types,
        permission = permissions.AddPortalContent,
        extra_constructors = constructors,
        fti = ftis,
    ).initialize(context)
    
    from Products.LinguaPlone import LanguageIndex
    context.registerClass(
        LanguageIndex.LanguageIndex, 
        permission=permissions.AddLanguageIndex,
        constructors=(LanguageIndex.manage_addLanguageIndexForm,
                      LanguageIndex.manage_addLanguageIndex),
        icon='www/index.png',
        visibility=None)

    # Make selection criteria available for the LanguageIndex
    from Products.ATContentTypes.criteria import _criterionRegistry
    from Products.ATContentTypes.criteria.selection import ATSelectionCriterion
    crit_id = ATSelectionCriterion.meta_type
    crit_reg = _criterionRegistry
    index = LanguageIndex.LanguageIndex.meta_type

    indices = crit_reg.criterion2index.get(crit_id, ())
    crit_reg.criterion2index[crit_id] = indices + (index, )

    value = crit_reg.index2criterion.get(index, ())
    crit_reg.index2criterion[index] = value + (crit_id,)
