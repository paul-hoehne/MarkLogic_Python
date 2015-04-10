Contributing to MarkLogic_Python
================================

MarkLogic_Python welcomes new contributors. This document will guide
you through the process.

-  `Question or Problem?`_
-  `Issues and Bugs`_
-  `Feature Requests`_
-  `Submission Guidelines`_

Note that I have no idea if you’re using this and enjoying it or
suffering through it. If you contact me through the issue tracker I’ll
have a better idea of what’s going on. So please, don’t feel shy about
contacting me.

.. _question:

Got a Question or Problem?
--------------------------

If you have questions about how to use MarkLogic_Python, please `submit
a ticket here on GitHub`_ or ask on `Stack Overflow with the “marklogic”
tag`_.

.. _issue:

Found an Issue?
---------------

If you find a bug in the source code or a mistake in the documentation, you
can help by submitting an issue to the `issue tracker`_. Even better you can
submit a Pull Request with a fix for the issue you filed.

.. _feature:

Want a Feature?
---------------

You can request a new feature by submitting an issue to the [issue
tracker][]. If you would like to implement a new feature then first
create a new issue and discuss it with one of our project maintainers.

.. _submit:

Submission Guidelines
---------------------

Submitting an Issue
~~~~~~~~~~~~~~~~~~~

If your issue appears to be a bug, and hasn’t been reported, open a new
issue. Help to maximize the effort spent fixing issues and adding new
features by not reporting duplicate issues. Providing the following
information will increase the chances of your issue being dealt with
quickly:

-  **Overview of the Issue** - if an error is being thrown a stack trace
   helps
-  **Motivation for or Use Case** - explain why this is a bug for you
-  **MarkLogic_Python Version** - is it a named version?
-  **Python Version** - what version of Python are you working with?
-  **Operating System** - Mac, windows? details help
-  **Suggest a Fix** - if you can’t fix the bug yourself, perhaps you
   can point to what might be causing the problem (line of code or
   commit)

Submitting a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~

Fork MarkLogic_Python
^^^^^^^^^^^^^^^^^^^^^^

Fork the project `on GitHub`_ and clone your copy.

.. code:: console

   $ git clone git@github.com:username/MarkLogic_Python.git
   $ cd MarkLogic_Python
   $ git remote add upstream git://github.com/paul-hoehne/MarkLogic_Python.git

I ask that you open an issue in the `issue tracker`_ and get agreement
from me before you start coding.

Nothing is more frustrating than seeing your hard work go to waste
because your vision does not align.

Create a branch for your changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Okay, so you have decided to fix something. Create a feature branch and
start hacking:

.. code:: console

   $ git checkout -b my-feature-branch -t origin/master

Formatting code
^^^^^^^^^^^^^^^

We use `.editorconfig`_ to configure our editors for proper code formatting.
If you don’t use a tool that supports editorconfig be sure to configure your
editor to use the settings equivalent to our `.editorconfig`_ file.

Commit your changes
^^^^^^^^^^^^^^^^^^^

Make sure git knows your name and email address:

.. code:: console

   $ git config --global user.name "J. Random User"
   $ git config --global user.email "j.random.user@example.com"

Writing good commit logs is important. A commit log should describe what
changed and why. Follow these guidelines when writing one:

1. The first line should be 50 characters or less and contain a short
   description of the change including the Issue number prefixed by a
   hash (#).
2. Keep the second line blank.
3. Wrap all other lines at 72 columns.

A good commit log looks like this:

::

    Fixing Issue #123: make the whatchamajigger work in MarkLogic 8

    Body of commit message is a few lines of text, explaining things
    in more detail, possibly giving some background about the issue
    being fixed, etc etc.

    The body of the commit message can be several paragraphs, and
    please do proper word-wrap and keep columns shorter than about
    72 characters or so. That way `git log` will show things
    nicely even when it is indented.

The header line should be meaningful; it is what other people see when
they run ``git shortlog`` or ``git log --oneline``.

Rebase your repo
^^^^^^^^^^^^^^^^

Use ``git rebase`` (not ``git merge``) to sync your work from time to
time.

.. code:: console

   $ git fetch upstream
   $ git rebase upstream/master

Test your code
^^^^^^^^^^^^^^

There currently aren’t any automated tests. This section will be updated
when there are. In the meantime, please do your best to make sure your
changes do something good while not breaking existing features. Run
example.py to ensure that it still works correctly.

Push your changes
^^^^^^^^^^^^^^^^^

.. code:: console

   $ git push origin my-feature-branch

Submit the pull request
^^^^^^^^^^^^^^^^^^^^^^^

Go to https://github.com/username/MarkLogic_Python and select your
feature branch. Click the ‘Pull Request’ button and fill out the form.

Pull requests are usually reviewed within a few days. If you get
comments that need to be to addressed, apply your changes in a separate
commit and push that to your feature branch. Post a comment in the pull
request afterwards; GitHub does not send out notifications when you add
commits to existing pull requests.

That’s it! Thank you for your contribution!

After your pull request is merged
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After your pull request is merged, you can safely delete your branch and
pull the changes from the main (upstream) repository:

-  Delete the remote branch on GitHub either through the GitHub web UI
   or your local shell as follows:

.. code:: console

   git push origin --delete my-feature-branch

-  Check out the master branch:

.. code:: console

   git checkout master -f

-  Delete the local branch:

.. code:: console

   git branch -D my-feature-branch

-  Update your master with the latest upstream version:

.. code:: console

   git pull --ff upstream master

.. _Question or Problem?: #question
.. _Issues and Bugs: #issue
.. _Feature Requests: #feature
.. _Submission Guidelines: #submit
.. _submit a ticket here on GitHub: #issue
.. _Stack Overflow with the “marklogic” tag: http://stackoverflow.com/tags/marklogic
.. _on GitHub: https://github.com/paul-hoehne/MarkLogic_Python/fork
.. _issue tracker: https://github.com/paul-hoehne/MarkLogic_Python/issues
.. _.editorconfig: http://editorconfig.org/
