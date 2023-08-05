from Products.CMFCore.utils import getToolByName

def uninstall(context):
    
    if not context.readDataFile('uwosh.northstar-uninstall.txt'):
        return
    
    cp = getToolByName(context.getSite(), 'portal_controlpanel')
    cp.unregisterApplication("uwosh.northstar")
    cp.unregisterApplication('uwosh.northstar-app-generator')