from plone.memoize.instance import memoize
from plone.app.workflow.remap import remap_workflow
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from Products.CMFCore.utils import getToolByName
from uwosh.northstar.permissions import managed_permissions, allowed_guard_permissions
from Globals import PersistentMapping
from Acquisition import aq_get
from Products.DCWorkflow.Transitions import TRIGGER_AUTOMATIC, TRIGGER_USER_ACTION
from urllib import urlencode
from uwosh.northstar.actions import MailerAction
from Products.PythonScripts.PythonScript import PythonScript
from Products.validation.validators.BaseValidators import EMAIL_RE
import re
from uwosh.northstar.utils import clone_transition, clone_state, generate_id, json
from zope.schema.interfaces import IVocabularyFactory
from OFS.CopySupport import CopyError
from OFS.ObjectManager import checkValidId

email_validator = re.compile(r'^' + EMAIL_RE)
comma_seperated_email_validator = re.compile(r'^' + EMAIL_RE[:-1] + '(,\s*' + EMAIL_RE[:-1] + ')*$')

plone_shipped_workflows = [
    'folder_workflow',
    'intranet_folder_workflow',
    'intranet_workflow',
    'one_state_workflow',
    'plone_workflow',
    'simple_publication_workflow'
]          
        

class UWOshProjectNorthStar(BrowserView):
    """
    We have so many different page templates so that they can
    be rendered independently of each of for ajax calls.
    It's also nice to break of the huge template files too.
    """
    errors = {}    
    next_id = None # the id of the next workflow to be viewed
    
    label = u'Workflow Manager'
    description = u'Manage your custom workflows TTW.'
    
    template = ViewPageTemplateFile('templates/controlpanel.pt')    
    content_template = ViewPageTemplateFile('templates/content.pt')
    
    workflow_state_template = ViewPageTemplateFile('templates/workflow-state.pt')
    workflow_states_template = ViewPageTemplateFile('templates/workflow-states.pt')
    delete_state_template = ViewPageTemplateFile('templates/delete-state.pt')
    add_new_state_template = ViewPageTemplateFile('templates/add-new-state.pt')
    
    workflow_transitions_template = ViewPageTemplateFile('templates/workflow-transitions.pt')
    workflow_transition_template = ViewPageTemplateFile('templates/workflow-transition.pt')
    delete_transition_template = ViewPageTemplateFile('templates/delete-transition.pt')
    add_new_transition_template = ViewPageTemplateFile('templates/add-new-transition.pt')
    
    wrapped_dialog_template = ViewPageTemplateFile('templates/wrapped-dialog.pt')
    
    add_new_workflow_template = ViewPageTemplateFile('templates/add-new-workflow.pt')
    delete_workflow_template = ViewPageTemplateFile('templates/delete-workflow.pt')
    
    managed_permissions = managed_permissions
    
    def __call__(self):
        return self.template()
        
    @property
    @memoize
    def has_newish_jquery_installed(self):
        try:
            from Products.CMFPlone.migrations import v3_3
            return True
        except ImportError:
            try:
                from plone.app.upgrade import v40
                return True
            except:
                return False
    
    @property
    @memoize
    def allowed_guard_permissions(self):
        return allowed_guard_permissions
        
    @property
    @memoize
    def portal_workflow(self):
        return getToolByName(self.context, 'portal_workflow')
    
    @property
    @memoize
    def available_workflows(self):
        return [w for w in self.workflows if w.id not in plone_shipped_workflows]
        
    @property
    @memoize
    def workflows(self):
        pw = self.portal_workflow
        
        ids = pw.portal_workflow.listWorkflows()
        
        return [pw[id] for id in sorted(ids)]
    
    @property
    @memoize
    def selected_workflow(self):
        selected = self.request.get('selected-workflow')
        if type(selected) == list and len(selected) > 0:
            selected = selected[0]
            
        if selected and selected in self.portal_workflow.objectIds():
            return self.portal_workflow[selected]
        else:
            return None
        
    @property
    @memoize
    def selected_state(self):
        state = self.request.get('selected-state')
        if type(state) == list and len(state) > 0:
            state = state[0]
            
        if state in self.selected_workflow.states.objectIds():
            return self.selected_workflow.states[state]
            
        return None
        
    @property
    @memoize
    def selected_transition(self):
        transition = self.request.get('selected-transition')
        if type(transition) == list and len(transition) > 0:
            transition = transition[0]
            
        if transition in self.selected_workflow.transitions.objectIds():
            return self.selected_workflow.transitions[transition]
            
        return None
    
    @property
    @memoize
    def available_states(self):
        wf = self.selected_workflow
        if wf is not None:
            states = [wf.states[state] for state in wf.states.objectIds()]
            states.sort(lambda x, y: cmp(x.title.lower(), y.title.lower()))
            return states
        else:
            return []
        
    @property
    @memoize
    def available_transitions(self):
        wf = self.selected_workflow
        if wf is not None:
            transitions = [wf.transitions[transition] for transition in wf.transitions.objectIds()]
            transitions.sort(lambda x, y: cmp(x.title.lower(), y.title.lower()))
            return transitions
        else:
            return []
        
    def render_transitions_template(self):
        return self.workflow_transitions_template(
            available_states=self.available_states,
            available_transitions=self.available_transitions
        )
    
    def render_states_template(self):
        return self.workflow_states_template(
            available_states=self.available_states,
            available_transitions=self.available_transitions
        )

    def render_content_template(self):
        return self.content_template()
        
    def get_transition(self, id):
        if id in self.selected_workflow.transition.objectIds():
            return self.selected_workflow.transitions[id]
        else:
            return None
     
    @property
    @memoize
    def assignable_types(self):
        vocab_factory = getUtility(IVocabularyFactory,
                                   name="plone.app.vocabularies.ReallyUserFriendlyTypes")
        types = []
        for v in vocab_factory(self.context):
            types.append(dict(id=v.value, title=v.title) )
        def _key(v):
            return v['title']
        types.sort(key=_key)
        return types
     
    @property
    def assigned_types(self):
        types = []
        try:
            nondefault = [info[0] for info in self.portal_workflow.listChainOverrides()]
            for type_ in self.assignable_types:
                if type_['id'] in nondefault:
                    chain = self.portal_workflow.getChainForPortalType(type_['id'])
                    if len(chain) > 0 and chain[0] == self.selected_workflow.id:
                        types.append(type_)
        except:
            pass

        return types
             
    def get_transition_list(self, state):
        transitions = state.getTransitions()
        return [t for t in self.available_transitions if t.id in transitions]
        
    def get_state(self, id):
        if id in self.selected_workflow.states.objectIds():
            return self.selected_workflow.states[id]
        else:
            return None
        
    @property
    @memoize
    def next_url(self):
        return self.get_url()

    def get_url(self, relative=None, workflow=None, transition=None, state=None, **kwargs):
        url = self.context.absolute_url()
        if relative:
            url = url + '/' + relative.lstrip('/')
        else:
            url = url + '/@@uwosh-northstar'

        params = {}
        if not workflow:
            if self.next_id:
                params['selected-workflow'] = self.next_id
            elif self.selected_workflow:
                params['selected-workflow'] = self.selected_workflow.id
        else:
            params['selected-workflow'] = workflow.id

        if transition:
            params['selected-transition'] = transition.id

        if state:
            params['selected-state'] = state.id
            
        params.update(kwargs)

        if len(params) > 0:
            url = url + "?" + urlencode(params)

        return url
        
    @memoize
    def getGroups(self):
        gf = aq_get(self.context, '__allow_groups__', None, 1)
        if gf is None:
            return ()
        try:
            groups = gf.searchGroups()
        except AttributeError:
            return ()
        else:
            return groups

    def parse_set_value(self, key):
        val = self.request.get(key)
        if val:
            if type(val) in (str, unicode):
                return set(val.split(','))
            elif type(val) in (tuple, list):
                return set(val)
        else:
            return set(())
        return val
        
    def has_mailer_action(self, transition):
        return transition.after_script_name and transition.after_script_name.endswith('mailer-action') \
            and transition.after_script_name in self.selected_workflow.scripts.objectIds()
        
    def get_mailer_action(self, transition=None):
        if transition is None:
            transition = self.selected_transition
            
        if self.has_mailer_action(transition):
            return MailerAction(self.selected_workflow.scripts[transition.after_script_name])
            
        return MailerAction()
        
    def comma_seperated_email_validator(self, name, required=False):

        v = self.request.get(name)
        if v and len(v) > 0:
            v = v.replace(' ', '')
            membership = getToolByName(self.context, 'portal_membership')
            for email in v.split(','):
                if email in ('{{authenticated_user_email}}', '{{site_owner_email}}'):
                    self.authenticate_replacement_emails(name, v)
                elif not email_validator.match(email):
                    user = membership.getMemberById(email)
                    if not user or not user.getProperty('email', False):
                        self.errors[name] = 'The email address "%s" is not a valid email or username.' % email
        else:
            if required:
                self.errors[name] = 'You must enter an email address.'

        return v
        
    def authenticate_replacement_emails(self, name, v):
        if v == '{{authenticated_user_email}}':
            pm = getToolByName(self.context, 'portal_membership')
            member = pm.getAuthenticatedMember()
            email = member.getProperty('email')
            
            if not email or len(email) == 0:
                self.errors[name] = "Authenticated user has no email specified."
            
        elif v == '{{site_owner_email}}':
            
            utool = getToolByName(self.context, 'portal_url')
            portal = utool.getPortalObject()
            email = portal.email_from_address
            
            if not email or len(email) == 0:
                self.errors[name] = "The site has no email from address setup."
            
        else:
            self.errors[name] = "You specified an incorrect subsitution value here."

    def email_validator(self, name, required=False):
        v = self.request.get(name)
        
        # if it's using a check boxed widget, only take the checkbox value it's its checked
        checked_v = self.request.get(name + '-checkbox', None)
        if checked_v:
            v = checked_v
        
        if v and len(v) > 0:
            v = v.strip().replace(' ', '')
            if v in ('{{authenticated_user_email}}', '{{site_owner_email}}'):
                self.authenticate_replacement_emails(name, v)
            elif not email_validator.match(v):
                membership = getToolByName(self.context, 'portal_membership')
                user = membership.getMemberById(v)
                if not user or not user.getProperty('email', False):
                    self.errors[name] = 'The email address or username "%s" is not valid.' % v
        else:
            if required:
                self.errors[name] = 'You must enter an email address.'

        return v

    @property
    @memoize
    def context_state(self):
        return getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

    def not_empty_validator(self, name):
        v = self.request.get(name, '').strip()
        if v is None or (type(v) in (str, unicode) and len(v) == 0) or (type(v) in (tuple, set, list) and len(v) == 0):
            self.errors[name] = 'This field is required.'

        return v

    def id_validator(self, name, container):
        id = self.request.get(name, '').strip()
        putils = getToolByName(self.context, 'plone_utils')
        id = generate_id(putils.normalizeString(id), container.objectIds())
        try:
            checkValidId(container, id)
        except:
            self.errors[name] = 'Invalid workflow name. Please try another.'
            
        return id

    def wrap_template(self, tmpl, **options):
        ajax = self.request.get('ajax', None)
        if ajax:
            return tmpl(options=options)
        else:
            return self.wrapped_dialog_template(content=tmpl, options=options)

    def handle_response(self, message=None, tmpl=None, redirect=None, load=None, justdoerrors=False, slideto=False, **kwargs):
        ajax = self.request.get('ajax', None)

        status = {}
        if len(self.errors) > 0:
            status['status'] = 'error'
            if ajax:
                status['errors'] = [[k, v] for k, v in self.errors.items()]
            else:
                status['errors'] = self.errors
        elif redirect:
            status['status'] = 'redirect'
            
            if type(redirect) in (str, unicode):
                status['location'] = redirect
            else:
                status['location'] = self.next_url
                
        elif slideto:
            status['status'] = 'slideto'
            status['url'] = self.get_url(**kwargs) # either state or transition here...
        elif load:
            status['status'] = 'load'
            status['url'] = load
        else:
            status['status'] = 'ok'        

        if message:
            status['message'] = message

        if ajax:
            if tmpl and not justdoerrors:
                return tmpl.__of__(self.context)(**kwargs)
            else:
                return json(status)
        else:
            if redirect:
                return self.request.response.redirect(status['location'])
            elif tmpl:
                return self.wrap_template(tmpl, **kwargs)
            else:
                return self.request.response.redirect(self.next_url)
        
        
class UWOshProjectNorthStarActions(UWOshProjectNorthStar):
    """
    Form Action Guidelines...
    
    You can provide an ajax parameters set to true to specify
    that the form is being handled by ajax.
    
    If this is not specified, the form will be redirected to 
    the base workflow form.
    
    Form validation will also be done. If the request is an
    ajax one, the validation will be sent back, if everything
    went well and validated, it'll send a {'status' : 'ok'} back.
    
    """
    
    edit_mail_action_template = ViewPageTemplateFile('templates/edit-mail-action.pt')
    delete_mail_action_template = ViewPageTemplateFile('templates/delete-mail-action.pt')
    sanity_check_template = ViewPageTemplateFile('templates/sanity-check.pt')
    assign_template = ViewPageTemplateFile('templates/assign.pt')
    
    def render_add_new_transition_template(self):
        self.errors = {}
        return self.handle_response(tmpl=self.add_new_transition_template)
        
    def render_add_new_state_template(self):
        self.errors = {}
        return self.handle_response(tmpl=self.add_new_state_template)
            
    def render_add_new_workflow_template(self):
        self.errors = {}
        return self.handle_response(tmpl=self.add_new_workflow_template)
    
    def render_edit_mail_action_template(self):
        self.errors = {}
        return self.handle_response(tmpl=self.edit_mail_action_template, action=self.get_mailer_action())
    
    def submit_add_new_transition(self):
        self.errors = {}
        transition = self.not_empty_validator('transition-name')
        transition_id = self.id_validator('transition-name', self.selected_workflow)
        
        if not self.errors:
            # must have transition to go on
            workflow = self.selected_workflow
            
            workflow.transitions.addTransition(transition_id)
            new_transition = workflow.transitions[transition_id]
            clone_of_id = self.request.get('clone-from-transition')
            if clone_of_id:
                # manage_copy|paste|clone doesn't work?
                clone_transition(new_transition, workflow.transitions[clone_of_id])
            else:
                new_transition.actbox_name = transition
                new_transition.actbox_url = "%(content_url)s/content_status_modify?workflow_action=" + transition_id
                new_transition.actbox_category = 'workflow'
                
            new_transition.title = transition
            
            # if added from state screen
            referenced_state = self.request.get('referenced-state', None)
            if referenced_state:
                state = self.selected_workflow.states[referenced_state]
                state.transitions = state.transitions + (new_transition.id,)
            
            return self.handle_response(
                message='"%s" transition successfully created.' % new_transition.id, 
                slideto=True,
                transition=new_transition)
        else:
            return self.handle_response(tmpl=self.add_new_transition_template, justdoerrors=True)
    
    def submit_add_new_state(self):
        self.errors = {}
        state = self.not_empty_validator('state-name')
        state_id = self.id_validator('state-name', self.selected_workflow)

        if not self.errors:
            # must have state to go on
            workflow = self.selected_workflow
            
            workflow.states.addState(state_id)
            new_state = workflow.states[state_id]
            clone_of_id = self.request.get('clone-from-state')
            if clone_of_id:
                # manage_copy|paste|clone doesn't work?
                clone_state(new_state, workflow.states[clone_of_id])
            
            new_state.title = state
            
            # if added from transition screen
            referenced_transition = self.request.get('referenced-transition', None)
            if referenced_transition:
                new_state.transitions = new_state.transitions + (referenced_transition,)
            
            return self.handle_response(
                message='"%s" state successfully created.' % new_state.id, 
                slideto=True,
                state=new_state
            )
        else:
            return self.handle_response(tmpl=self.add_new_state_template, justdoerrors=True)
    
    def submit_add_new_workflow(self):
        self.errors = {}
        workflow = self.not_empty_validator('workflow-name')
        workflow_id = self.id_validator('workflow-name', self.portal_workflow)

        if self.errors:
            return self.handle_response(tmpl=self.add_new_workflow_template, justdoerrors=True)
        else:
            # must have state to go on
            cloned_from_workflow = self.portal_workflow[self.request.get('clone-from-workflow')]
            
            self.context.portal_workflow.manage_clone(cloned_from_workflow, workflow_id)
            new_workflow = self.context.portal_workflow[workflow_id]
            new_workflow.title = workflow
            self.next_id = new_workflow.id

            return self.handle_response(redirect=True)
            
    
    def submit_edit_mail_action(self):
        self.errors = {}
        workflow = self.selected_workflow
        transition = self.selected_transition

        action = self.get_mailer_action(transition)
        if action.script:
            script = workflow.scripts[transition.after_script_name]
        else:
            script_id = "transition-%s-mailer-action" % transition.id
            workflow.scripts._setObject(script_id, PythonScript(script_id))
            script = workflow.scripts[script_id]
            transition.after_script_name = script_id
            action = MailerAction(script)

        action.script._params = 'state_info'
        action.to_ = self.email_validator('to', required=True)
        action.from_ = self.email_validator('from', required=True)
        action.cc = self.comma_seperated_email_validator('cc')
        action.subject = self.not_empty_validator('subject')
        action.body = self.not_empty_validator('body')
        action.write_script()

        return self.handle_response(message='Mailer action for "%s" successfully updated.' % transition.id)
    
    def update_selected_transitions(self):
        wf = self.selected_workflow
        state = wf.states[self.request.get('selected-state')]
        
        transitions = wf.transitions.objectIds()
        selected_transitions = []
        
        for transition in transitions:
            if self.request.has_key('transition-%s-state-%s' % (transition, state.id)):
                selected_transitions.append(transition)
                
        state.transitions = tuple(selected_transitions)
        
    def update_state_permissions(self):
        wf = self.selected_workflow
        state = wf.states[self.request.get('selected-state')]
        
        perm_roles = PersistentMapping()
        available_roles = state.getAvailableRoles()
        for managed_perm in managed_permissions:
            selected_roles = []
            
            for role in available_roles:
                if self.request.has_key('permission-%s-role-%s-state-%s' % (managed_perm['name'], role, state.id)):
                    selected_roles.append(role)
            
            if len(selected_roles) > 0:
                perm_roles[perm] = tuple(selected_roles)
                
                if perm not in wf.permissions:
                    wf.permissions = wf.permissions + (perm_values['perm'],)
            
            
        state.permission_roles = perm_roles
        
    def update_state_properties(self):
        
        wf = self.selected_workflow
        state = wf.states[self.request.get('selected-state')]
        
        if self.request.has_key('state-%s-initial-state' % state.id):
            wf.initial_state = state.id
            
        title = self.request.get('state-%s-title' % state.id, False)
        if title:
            state.title = title
            
        description = self.request.get('state-%s-description' % state.id, False)
        if description:
            state.description = description
            
    
    def update_state_group_roles(self):
        wf = self.selected_workflow
        state = wf.states[self.request.get('selected-state')]
        
        group_roles = PersistentMapping()
        available_roles = state.getAvailableRoles()
        groups = self.getGroups()
        
        for group in groups:
            selected_roles = []
            
            for role in available_roles:
                if self.request.has_key("group-%s-role-%s-state-%s" % (group['id'], role, state.id)):
                    selected_roles.append(role)
                    
                    
            if len(selected_roles) > 0:
                group_roles[group['id']] = tuple(selected_roles)

                if group['id'] not in wf.groups:
                    wf.groups = wf.groups + (group['id'],)
                    
            
        state.group_roles = group_roles
        
        
    def save_state(self):
        self.errors = {}
        ajax = self.request.get('ajax', None)
        
        self.update_selected_transitions()
        self.update_state_permissions()
        self.update_state_group_roles()
        self.update_state_properties()
        
        return self.handle_response()
    
    def update_guards(self):
        wf = self.selected_workflow
        transition = self.selected_transition
        guard = transition.getGuard()
        
        perms = []
        for key, perm in allowed_guard_permissions.items():
            if self.request.has_key('transition-%s-guard-permission-%s' % (transition.id, key)) and perm not in guard.permissions:
                perms.append(perm)
        guard.permissions = tuple(perms)
                
        roles = self.parse_set_value('transition-%s-guard-roles' % transition.id)
        okay_roles = set(wf.getAvailableRoles())
        guard.roles = tuple(roles & okay_roles)
           
        groups = self.parse_set_value('transition-%s-guard-groups' % transition.id)
        okay_groups = set([g['id'] for g in self.getGroups()])
        guard.groups = tuple(groups & okay_groups)
        
        transition.guard = guard
        
    def update_transition_properties(self):
        wf = self.selected_workflow
        transition = self.selected_transition
        
        if self.request.has_key('transition-%s-autotrigger' % transition.id):
            transition.trigger_type = TRIGGER_AUTOMATIC
        else:
            transition.trigger_type = TRIGGER_USER_ACTION
            
        if self.request.has_key('transition-%s-display-name' % transition.id):
            transition.actbox_name = self.request.get('transition-%s-display-name' % transition.id)
        
        if self.request.has_key('transition-%s-new-state' % transition.id):
            transition.new_state_id = self.request.get('transition-%s-new-state' % transition.id)
            
        if self.request.has_key('transition-%s-title' % transition.id):
            transition.title = self.request.get('transition-%s-title' % transition.id)
            
        if self.request.has_key('transition-%s-description' % transition.id):
            transition.description = self.request.get('transition-%s-description' % transition.id)
            
        for state in self.available_states:
            if self.request.has_key('transition-%s-state-%s-selected' % (transition.id, state.id)):
                if transition.id not in state.transitions:
                    state.transitions = state.transitions + (transition.id,)
            else:
                if transition.id in state.transitions:
                    transitions = list(state.transitions)
                    transitions.remove(transition.id)
                    state.transitions = transitions
    
    def save_transition(self):
        self.errors = {}
        ajax = self.request.get('ajax', None)
        
        self.update_guards()
        self.update_transition_properties()
        
        return self.handle_response()
                    
        
    def delete_transition(self):
        self.errors = {}
        transition = self.selected_transition
        id = transition.id
        
        if self.request.get('button.confirm.delete', False) == 'Delete':
            self.selected_workflow.transitions.deleteTransitions([id])
            # now check if we have any dangling references
            for state in self.available_states:
                if id in state.transitions:
                    transitions = list(state.transitions)
                    transitions.remove(id)
                    state.transitions = tuple(transitions)
                    
            return self.handle_response(message='"%s" transition has been successfully deleted.' % id)
        elif self.request.get('button.cancel.delete', False) == 'Cancel':
            return self.handle_response(message='Deleting the "%s" transition has been canceled.' % id)
        else:
            return self.handle_response(tmpl=self.delete_transition_template)
    
    def delete_state(self):
        self.errors = {}
        state = self.selected_state
        transitions = self.available_transitions
        id = state.id
        
        self.is_using_state = False
        for transition in transitions:
            if transition.new_state_id == id:
                self.is_using_state = True
                break
        
        if self.request.get('button.confirm.delete', False) == 'Delete':
            if self.is_using_state:
                replacement = self.request.get('replacement-state', self.available_states[0].id)
                for transition in self.available_transitions:
                    if id == transition.new_state_id:
                        transition.new_state_id = replacement
                        
                chains = self.portal_workflow.listChainOverrides()
                types_ids = [c[0] for c in chains if self.selected_workflow.id in c[1]]
                remap_workflow(self.context, types_ids, (self.selected_workflow.id,), {id : replacement})
                
            self.selected_workflow.states.deleteStates([id])
                
            return self.handle_response(message='"%s" state has been successfully deleted.' % id)
        elif self.request.get('button.cancel.delete', False) == 'Cancel':
            return self.handle_response(message='Deleting the "%s" state has been canceled.' % id)
        else:
            return self.handle_response(tmpl=self.delete_state_template)
                
    def delete_workflow(self):
        self.errors = {}
        
        self.can_delete = len(self.assigned_types) == 0
        
        if not self.can_delete:
            return self.handle_response(
                tmpl=self.delete_workflow_template, 
                message=u'You can not delete this workflow until no content types are specified to use this workflow.'
            )
        elif self.request.get('button.confirm.delete', False) == 'Delete':
            self.portal_workflow.manage_delObjects([self.selected_workflow.id])
            return self.handle_response(redirect=True)
        elif self.request.get('button.cancel.delete', False) == 'Cancel':
            return self.handle_response()
        else:
            return self.handle_response(tmpl=self.delete_workflow_template)
        
    def delete_mail_action(self):
        self.errors = {}
        ajax = self.request.get('ajax', None)

        if self.request.get('button.confirm.delete', False) == 'Delete':
            self.selected_workflow.scripts.manage_delObjects([self.selected_transition.after_script_name])
            self.selected_transition.after_script_name = None
            
            return self.handle_response()
        elif self.request.get('button.cancel.delete', False) == 'Cancel':
            return self.handle_response()
        else:
            return self.handle_response(tmpl=self.delete_mail_action_template)

    def sanity_check(self):
        self.errors = {}
        states = self.available_states
        transitions = self.available_transitions
        self.errors['state-errors'] = []
        self.errors['transition-errors'] = []
        
        for state in states:
            found = False
            for transition in transitions:
                if transition.new_state_id == state.id:
                    found = True
                    break
            
            if self.selected_workflow.initial_state == state.id and len(state.transitions) > 0:
                found = True
            
            if not found:
                self.errors['state-errors'].append(state)
        
        for transition in transitions:
            found = False
            if not transition.new_state_id:
                found = True
                
            for state in states:
                if transition.id in state.transitions:
                    found = True
                    break
                    
            if not found:
                self.errors['transition-errors'].append(transition)
        
        state_ids = [s.id for s in states]
        if not self.selected_workflow.initial_state or self.selected_workflow.initial_state not in state_ids:
            self.errors['initial-state-error'] = True
        
        self.has_errors = len(self.errors['state-errors']) > 0 or len(self.errors['transition-errors']) > 0 or \
            self.errors.has_key('initial-state-error')
        
        return self.handle_response(tmpl=self.sanity_check_template)
        
    def assign(self):
        self.errors = {}

        if self.request.get('next', False):
            params = urlencode({'type_id' : self.request.get('type_id'), 'new_workflow' : self.selected_workflow.id})
            return self.handle_response(load=self.context_state.portal_url() + '/@@types-controlpanel?' + params)
        else:
            return self.handle_response(tmpl=self.assign_template)
        
    
    def retrieve_item(self):
        state = self.selected_state
        transition = self.selected_transition
        
        if state:
            return self.workflow_state_template(state=state, available_transitions=self.available_transitions)
        elif transition:
            return self.workflow_transition_template(transition=transition, available_states=self.available_states)
        
        
    