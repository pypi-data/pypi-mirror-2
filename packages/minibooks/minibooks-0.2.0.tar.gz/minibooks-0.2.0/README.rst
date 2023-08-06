minibooks
=========

minibooks is a simple CRM, bookkeeping and double entry accounting
package for the Django web framework.

Example Project
---------------

Clone project and bootstrap virtual environment::

    ~$ hg clone http://bitbucket.org/caktus/minibooks
    ~$ cd minibooks/example_project/portal
    ~/minibooks/example_project/portal$ mkvirtualenv --distribute portal
    (portal)~/minibooks/example_project/portal$ ./bootstrap.py

Create local_settings.py file, syncdb, and runserver::

    (portal)~/minibooks/example_project/portal$ cp local_settings.py.example local_settings.py
    (portal)~/minibooks/example_project/portal$ ./manage.py syncdb
    (portal)~/minibooks/example_project/portal$ ./manage.py runserver

Visit http://localhost:8000/ in your browser.

Development sponsored by `Caktus Consulting Group, LLC.
<http://www.caktusgroup.com/services>`_.

