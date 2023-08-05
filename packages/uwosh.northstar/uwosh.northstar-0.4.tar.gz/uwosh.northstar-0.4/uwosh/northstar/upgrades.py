from Products.CMFCore.utils import getToolByName
default_profile = 'profile-uwosh.northstar:default'

def upgrade_to_0_3(context):
    context.runImportStepFromProfile(default_profile, 'action-icons')