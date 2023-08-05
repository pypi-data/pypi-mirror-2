from Products.CMFCore.utils import getToolByName

def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-plonetheme.colorcontext:uninstall')
    setup_tool.runAllImportSteps()
#    setup_tool.setImportContext('profile-CMFPlone:plone')
    return "Ran all uninstall steps."
