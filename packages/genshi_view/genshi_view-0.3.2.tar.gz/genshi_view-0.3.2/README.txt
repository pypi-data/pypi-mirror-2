Setting Up A New Project
========================

from start to editing code

0. Install virtualenv [Optional but highly recommended]::

 easy_install virtualenv

1. Make a virtualenv::

 virtualenv myproject

2. Install genshi_view::

 cd myproject
 . bin/activate
 mkdir src
 cd src
 hg clone http://k0s.org/hg/genshi_view # or `easy_install genshi_view`
 cd genshi_view
 python setup.py develop
 cd ..

3. Instantitate a template.  genshi_view is a pastescript template
that will get you a hello world application OOTB::

 paster create -t genshi_view your_project_name

Answer the questions it asks you regarding the template variables.

4. Serve your application to see that it works::

 cd your_project_name
 paster serve your_project_name.ini

Navigate to the URL that paster displays

5. You're done!  Helloworld works.  Now you just have to edit the
source code:

 - templates are in your_project_name/templates; there is one by default
 - static resources are in your_project_name/static
 - the request dispatcher is at your_project_name/dispatcher
 - the request handlers are at your_project_name/handlers;  if you add
   more, don't forget to add them to dipatcher.py's imports and to
   self.handlers in Dispatcher's __init__ function
 
