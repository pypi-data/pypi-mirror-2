from Products.CMFCore.utils import getToolByName
default_profile = 'profile-uwosh.northstar:default'

def upgrade_to_0_3(context):
    context.runImportStepFromProfile(default_profile, 'action-icons')
    
def upgrade_to_0_5b1(context):
    context.runImportStepFromProfile(default_profile, 'controlpanel')
    context.runImportStepFromProfile(default_profile, 'action-icons')
    
    
def upgrade_to_0_5b2(context):
    pass #nothing to upgrade in this step