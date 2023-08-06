from controlpanel import Base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from zope.component import getUtility, getMultiAdapter, queryUtility
from plone.contentrules.engine.interfaces import IRuleStorage, \
    IRuleAssignmentManager
from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.interfaces._events import IActionSucceededEvent
from plone.app.contentrules.conditions.wftransition import \
    IWorkflowTransitionCondition, WorkflowTransitionCondition
from plone.contentrules.engine import utils
from plone.app.contentrules.rule import Rule, get_assignments
from Products.CMFCore.utils import getToolByName
from uwosh.northstar.actionmanager import RuleAdapter, ActionManager
from urllib import urlencode
       
        
class DeleteActionView(Base):
    template = ViewPageTemplateFile('templates/delete-action.pt')
    
    def __call__(self):
        self.errors = {}

        if self.request.get('form.actions.delete', False) == 'Delete':
            rule = self.actions.get_rule(self.selected_transition)
            rule.delete_action(int(self.request.get('action_index')))
            return self.handle_response(
                message=u"Action has been deleted successfully."
            )
        elif self.request.get('form.actions.cancel', False) == 'Cancel':
            return self.handle_response()
        else:
            return self.handle_response(tmpl=self.template)

class AddActionView(Base):
    
    template = ViewPageTemplateFile('templates/add-action.pt')
    
    def __call__(self):
        self.errors = {}

        if self.request.get('form.actions.add', False) == 'Add':
            am = ActionManager()
            rule = am.get_rule(self.selected_transition)
            if rule is None:
                id = '--workflowmanager--%s' % self.selected_transition.id
                r = Rule()
                r.title = u"%s transition content rule" % self.selected_transition.id
                r.description = u"""This content rule was automatically created
the workflow manager to create actions on workflow events. If you want the 
behavior to work as expected, do not modify this out of the workflow manager."""
                am.storage[id] = r
                rule = RuleAdapter(r, self.selected_transition)
                rule.activate()
                
            editurl = '%s/%s/+action' % (self.portal.absolute_url(), rule.id)
            data = urlencode({
                ':action' : self.request.get('action-type', 'plone.actions.Mail'),
                'form.button.AddAction' : 'Add'
            })
            
            return self.handle_response(load=editurl + '?' + data)
        else:
            return self.handle_response(tmpl=self.template)
        