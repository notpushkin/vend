vend
=====

**Work in progress**

Vendored dependencies for Python. No more Virtualenv bullshit!

Usage::

    $ vend init
    Creating Pipfile...
    Creating vendor dir (my_package/vendor)...
    Done! Please add the following lines to your __init__.py:

      v_path = os.path.sep.join([
          os.path.dirname(os.path.realpath(__file__)), 'vendor'])
      if os.path.isdir(v_path):
          sys.path.append(v_path)

    $ vend install some dependencies
    $ python3.5 -m my_package  # no venv!


FAQ
-----

Why would you do that?
    I just got tired of all these incompatibilities between venvs (conda,
    pew/pipenv, vanilla virtualenv etc) and stuff.

    Also, this allows you to rename and move and copy project and sync it over
    ``$YOUR_FAVOURITE_STORAGE_PROVIDER`` without breaking anything (i. e.
    virtualenvs).

Should I check my vendored dependencies into the VCS?
    This is actually up to you. Kenneth Reitz does this (pipenv_, requests_),
    I personally just don't like it.


.. _pipenv: https://github.com/kennethreitz/pipenv/tree/master/pipenv/vendor
.. _requests: https://github.com/kennethreitz/requests/tree/master/requests/packages
