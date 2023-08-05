
mailer_action_script = \
"""

to_ = "%(to)s"
from_ = "%(from)s"
cc = "%(cc)s"
to_ = to_ + ',' + cc # since we can't add cc in a PythonScript since it'll have an invalid import...
# can't add a cc the correct way since this is
# restricted python and the imports needed for
# adding header info are not accessible
subject = "%(subject)s"
body = \"\"\"%(body)s\"\"\"

from Products.CMFCore.utils import getToolByName

utool = getToolByName(context, 'portal_url')
portal = utool.getPortalObject()
pm = getToolByName(portal, 'portal_membership')

object = state_info.object

member = pm.getAuthenticatedMember()
authenticated_userid = member.getId()

data = {
    'object_url' : object.absolute_url(),
    'portal_url' : portal.absolute_url(),
    'object_title' : object.Title(),
    'portal_title' : portal.title,
    'member_fullname' : member.getProperty('fullname', None),
    'previous_state' : state_info.old_state.title,
    'new_state' : state_info.new_state.title,
    'transition' : state_info.transition.title,
}

# I know, why do our own template... Well, we don't want
# to depend on anything for this script to work and
# we can't import re or Expression here...
def parse(body, open=False):
    if open:
        pos = body.find('}}')
        sub = body[:pos].strip()
        return str(data.get(sub, '')) + parse(body[pos+2:])
    else:
        pos = body.find('{{')
        if pos == -1:
            return body
        else:
            return body[:pos] + parse(body[pos+2:], open=True)

body = parse(body)
subject = parse(subject)

def get_emails(emails):
    # Can't do regular expressions here.... So just do simple check..
    res = []
    for email in emails.split(','):
        if "@" not in email:
            try:
                user = pm.getMemberById(email)
                res.append(user.getProperty('email'))
            except:
                pass
        else:
            res.append(email)
            
    return ','.join(res)

to_ = to_.replace('authenticated_user', authenticated_userid)
to_ = get_emails(to_)
from_ = from_.replace('authenticated_user', authenticated_userid)
from_ = get_emails(from_)

mailhost = getToolByName(context, 'MailHost')
mailhost.send(body, mto=to_, mfrom=from_, subject=subject)

"""

variable_start_delimiter = "# /*---- VARIABLE DEFINITION ----*\\"
variable_end_delimiter = "# /*---- END VARIABLE DEFINITION ----*\\"

class MailerAction(object):
    
    to_ = None
    from_ = None
    cc = None
    subject = "{{object_title}} -> {{transition}}"
    body = """{{object_title}} at {{object_url}} has changed its state. The previous state was {{previous_state}}. 
              The {{transition}} was performed on it and the object was moved to the {{new_state}} state."""
    
    def __init__(self, script=None):
        self.script = script
        self.parse_script()
            
            
    def parse_script(self):
        if self.script:
            
            reading = False
            current_value = None
            current_name = None

            for line in self.script.body().splitlines():
                
                if line.startswith(variable_end_delimiter):
                    setattr(self, current_name, current_value)
                    reading = False
                
                if reading:
                    if current_value is None:
                        current_value = line.lstrip('# ')
                    else:
                        current_value += "\n" + line.lstrip('# ')
                        
                if line.startswith(variable_start_delimiter):
                    current_name = line.lstrip(variable_start_delimiter).strip()
                    current_value = None
                    reading = True
            
    def write_script(self):
        
        actual_script = mailer_action_script % {
            'to' : self.to_, 'from' : self.from_, 'subject' : self.subject, 'body' : self.body, 'cc' : self.cc
        }
        body = '\n'.join(['# ' + l for l in self.body.splitlines()])
        text = \
"""%(start)s to_
#%(to)s
%(end)s
%(start)s from_
#%(from)s
%(end)s
%(start)s cc
#%(cc)s
%(end)s
%(start)s subject
#%(subject)s
%(end)s
%(start)s body
%(body)s
%(end)s

%(script)s

""" % { 
            'start' : variable_start_delimiter, 'end' : variable_end_delimiter,
            'to' : self.to_, 'from' : self.from_, 'subject' : self.subject, 'body' : body,
            'cc' : self.cc, 'script' : actual_script
        }
        
        self.script.write(text)
        