Changelog
=========

1.0.1 (2011-06-29)
------------------

Fix
~~~

- ReST title consistency corrected in docs. [Valentin Lab]

1.0.0 (2011-06-29)
------------------

New
~~~

- Set up ``setuptools`` packaging. [Valentin Lab]

- Use ``GITCHANGELOG_CONFIG_FILENAME`` environ variable (if set) to get
  the default location of config file. [Valentin Lab]

Changes
~~~~~~~

- Extracted the main code in a function ``main`` [Valentin Lab]

Fix
~~~

- Adds a period to subject message only if last char of subject is alpha
  numeric. [Valentin Lab]

0.1.4 (2011-06-29)
------------------

Changes
~~~~~~~

- Removed ``stdin`` from ``cmd()`` function. [Valentin Lab]

- Forced MULTILINE regexps on ``paragraph_wrap`` which is used to wrap
  body of commit messages. [Valentin Lab]

Fix
~~~

- Fixed the ``body_split_regexp`` to keep title words. [Valentin Lab]

- Corrected big bad bug due to ``Popen.wait()`` usage instead of
  ``Popen.communicate()`` [Valentin Lab]

0.1.3 (2011-06-29)
------------------

New
~~~

- Can now compare two commit. [Valentin Lab]

- Added ``LAST`` virtual identifier to get the last element coming from
  ``HEAD``. [Valentin Lab]

Fix
~~~

- Last revision is now displayed in changelog. [Valentin Lab]

  new: dev: added new option ``tag_filter_regexp`` to filter tags we
  want to use in the changelog.

0.1.2 (2011-06-29)
------------------

New
~~~

- Sections in changelog are now in the order given in ``git-
  changelog.rc`` in the ``section_regexps`` option. [Valentin Lab]

- Added ``body_split_regexp`` option to attempts to format correctly
  body of commit. [Valentin Lab]

- Use a list of tuple instead of a dict for ``section_regexps`` to be
  able to manage order between section on find match. [Valentin Lab]

- New ``unreleased_version_label`` option in ``git-changelog.rc`` to
  change label of not yet released code. [Valentin Lab]

- Use ``git-changelog`` section in ``git config`` world appropriately.
  [Valentin Lab]

Changes
~~~~~~~

- Commented code to toggle doctest mode. [Valentin Lab]

Fix
~~~

- Doctests were failing on this. [Valentin Lab]

- Bad sorting of tags (alphanumerical). Changed to commit date sort.
  [Valentin Lab]

- Support of empty commit message. [Valentin Lab]

- ``git`` in later versions seems to fail on ``git config <key>`` with
  errlvl 255, that was not supported. [Valentin Lab]

- Removed Traceback when there were no tags at all in the current git
  repository. [Valentin Lab]

0.1.1 (2011-06-29)
------------------

New
~~~

- Added section classifiers (ie: New, Change, Bugs) and updated the
  sample rc file. [Valentin Lab]

- Added a succint ``--help`` support. [Valentin Lab]

Fix
~~~

- Fixed case where exception was thrown if two tags are on the same
  commit. [Valentin Lab]


