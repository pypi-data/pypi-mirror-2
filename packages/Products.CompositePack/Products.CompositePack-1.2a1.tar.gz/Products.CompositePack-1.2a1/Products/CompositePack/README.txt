CompositePack is a product that allows the Plone Manager to build composite
pages by manually aggregating archetype content from his site.

Composition of content is made through a pseudo WYSIWYG user interface : the
design view.  A composite page has a layout which defines its structure.
Composite elements are displayed through viewlets. 

Both layouts and viewlets are acquired from the skin, which implies they are
customizable.

Layouts and viewlets are registered through the composite_tool in ZMI (see
below how to register them).

Plone versions supported
========================

    3.3

Products required 
================= 

CompositePage 1.0
    http://pypi.python.org/pypi/Products.CompositePage


Design view 
=========== 

The design view supports Firefox, Mozilla and IE6.
The design view allows the user to manipulate the composite elements : add,
move, delete or change their properties.

The design view allows you to add pieces of content to the slots defined in the
layout. In a slot, each location where a composite element can be added
displays a menu labeled 'add item'. When you click it, you get options :
'Content', 'Title' and 'HTML'. You choose 'Content' to select existing content
from your Plone site. You choose 'Title' or 'HTML' to add decorating content
specific to the instance (see details below). 

When choosing 'Content', you get a popup window wherein you can select the
piece of content that you want to add to this slot.  This window is a kupu
drawer. It only shows instance of "composable" portal types (see below for
setting up composables).  You browse your site until you have found the piece
of content you want to display.  When you click the 'ok' button, the composite
element is added to the composite page.  It is displayed through its default
viewlet.  Another viewlet can be selected later (see below).

Once added, the composite element can be moved by drag and drop from one slot
to another : drag and drop the icon associated with the composite element to
one of the 'add item' bars.

Each composite element has its own 'edit item' menu. It has the following
options : 'Edit', 'Delete' and 'Select viewlet'.

'Edit' sends you to the edit screen of the content pointed at by the element.

'Delete' removes the composite element (not the associated content).

'Select viewlet' lists the available viewlets registered for the content type
of the composite element. Choose one of them to get your content displayed
differently.

Layouts 
=======

A layout is a template that defines the display view. Similar to the template
of a normal view, a layout includes structural HTML and data from the composite
instance. It also includes slots. Slots define the places where content can be
added. The slots are named.

Layouts needs to be registered for composite content types. This happens through
the composite tool. 

At instantiation time, a layout is setup on a composite instance : the layout
registered as default for the content type.

Another layout can be chosen later if needed. This is done through the layout
menu of the design view. The menu proposes the layouts registered for the
content type.

When changing the layout, if the old and new layouts share slot names, the
content placed in a slot of a given name in the old layout will be shown in the
corresponding slot of the new layout.  Content items placed in slots of the old
layout that do not have corresponding names in the new layout are hidden, not
deleted.  Switching back to a layout will show items in their original
location. Hidden slots and composite elements (inaccessible through design
view) can be deleted through ZMI.


Viewlets
========

Viewlets are templates (python scripts) that produce HTML excerpts.
CompositePack does what is needed to get a normal development situation : the
'here' (or 'context') variables are bound correctly to the content item that is
displayed through the viewlet.

Viewlets are mapped to content types : this allows to define different viewlets
for different types (see below how to register viewlets). For instance, image
content types have very specific needs different from the needs of most textual. 


Titles
======

Titles are special composite elements which allows you to add some text when
composing your page.

In the design view, select 'add item' then 'Title'.  You get a popup window
with a prompt for the given title.  This adds a new composite element
displaying the title through its registered viewlet.

If you need to modify the title, access its data through the 'Edit' option of
the 'edit item' menu.

HTML Fragments
==============

Fragments are special composite elements which allow you to create
arbitrary fragments of HTML when composing your page.

In the design view, select 'add item' then 'HTML'. This will insert an empty
fragment. Use the 'Edit' option of the 'edit item' menu to edit the contents of
the fragment.

Setting up composables
======================

- Go to the "composite_tool" in Plone root (i.e. in \manage),

- Go to the "Composables" tab,

- Select the content type you want to add in the Types list (types by control
  clicking),

- Click Select button,

- Refresh your browser cache before to get the new javascript needed by the
  kupu drawers.

Registering a viewlet
=====================

- Create a page template (or python script) that returns an html excerpt,

- Go to the "composite_tool" in Plone root (i.e. in \manage),

- Inside the composite tool, go to the "viewlets" folder and add a
  CompositePack Viewlet using the button at the top.

    The CompositePack Viewlet has three fields :

    * "Short Name" - (Id) as usual,
    * "Title" which is the string that will be displayed under the 'select 
       viewlet' section of the 'edit item' menu,
    * "Skin Method" - the name of the Page Template file created earlier.
            
    Now the viewlet is registered, next it needs to be mapped to the
    content types it should be used for.

- On the viewlet, go to 'Composables' tab
    
    (With some buggy versions of archetypes, you'll need to go through the viewlets
    folder after the viewlet has been added.) 

- If the viewlet is to be used with all content types, select "(Default
  Setup)".

- If the viewlet is to be used for specific types only, select those
  in the types list box.

- Click the Select button. 

Setting up composites
======================

- Go to the "composite_tool" in Plone root (i.e. in \manage),

- Go to the "Composites" tab,

- Select the type you want to add in the Types list (types by control clicking),

- Click Select button,

Layouts can now be mapped for the type you registered.

Registering a layout
====================

- Create a page template which uses TALES slot expression (look at one of the
  existing layouts to understand it). The template should be based on plone
  main_template.

- Go to the "composite_tool" in Plone root (i.e. in \manage),

- Inside the composite tool, go into the "layouts" folder and add a CompositePack Layout using the button at the top.

    The CompositePack Layout has three fields :

    * "Short Name" (Id) as usual,
    * "Title" which is the string that will be displayed in the dropdown widget
      for layout selection,
    * "Skin Method" - the name of the Page Template file created earlier.
            
- On the viewlet, go to 'Composites' tab
    
    (With some buggy versions of archetypes, you'll need to go through the viewlets
    folder after the viewlet has been added.) 

- Choose among the composites in the types list box which types the layout
  should be used with.

- Click the Select button.

GenericSetup extension profile 
===============================

Plone uses GenericSetup for site configuration. To learn more about GenericSetup
please read the following documentation:

- http://plone.org/documentation/tutorial/understanding-and-using-genericsetup-in-plone

This means CompositePack can be configure completely throught xml configuration files.
In the folder profiles/default you will find the base profile for the default
configuration of the compositetool.

- ``toolset.xml`` : Adds the composite_tool to the plone site when running all import
  steps.

- ``types.xml`` : Adds the content types that come with CompositePack

- ``types/*.xml`` : A config file for each type

- ``import_steps.xml`` : This registers the import method 

- ``export_steps.xml`` : This registers the export method.

- ``compositetool.xml`` : This is the xml representation of all viewlets, layouts,
  composables and composites.

Customisation policy script
===========================

An alternative to customising the product through the web with the composite
tool is to write a script to perform the customisations automatically. This
ensures that your customisations are not lost if you reinstall or upgrade
CompositePack.

If there is a script called 'compositepack-customisation-policy.py' present in
any skin folder when CompositePack is installed, it will be run automatically
as part of the installation. A sample script called
'sample-compositepack-customisation-policy.py' is supplied in the compositepack
skin folder. You may rename this and customise it to match your system.
