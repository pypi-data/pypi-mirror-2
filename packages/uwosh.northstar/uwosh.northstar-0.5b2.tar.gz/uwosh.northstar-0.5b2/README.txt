Introduction
============

Our vision for uwosh.northstar is as a complete through-the-web (TTW)
tool for generating workflow applications, ie. a custom content type
combined with an assigned custom workflow.  

Right now it adds a control panel entry ``Workflow Manager`` where you
can access the workflow tool. It also adds a ``Workflow App Generator``
control panel entry where you can generate your workflow app products.

Creating content types is easily done by using Dexterity. The tool will
simply dump your dexterity content type. If you can not use dexterity,
the tool also supports using PloneFormGen as your modeling tool in which
it'll create a corresponding Archetype for the PloneFormGen form you've
created.

uwosh.northstar is strictly for add-on product workflows and content types.
By design, the tool cannot be used to edit default Plone workflows.

It provides all the functionality you need to manipulate workflows
easily through the web, using an AJAX-powered interface and to generate the
products of the content types and workflows you've created TTW.


Tested with
-----------
* Firefox
* Google Chrome
* Safari
* Opera


Check out the youtube video of the workflow manager in action. 
http://www.youtube.com/watch?v=3-Cks1zeHXc


Installation
============

Just add `uwosh.northstar` to your buildout eggs sections and then install the
"North * " product in the add/remove products control panel. In order for the 
workflow application generator to work, you'll need to also add ZopeSkel, 
PasteScript and Paste to the eggs section in your buildout. Additionally, you'll
need to activate PloneFormGen or Dexterity in your site.


Produced by Secret Laboratory Number 1 at UW Oshkosh.
