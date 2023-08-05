hgcampfire
==========

``hgcampfire`` provides a Mercurial hook to notify a `Campfire`_
chatroom about changesets coming in to a repository.

.. _Campfire: http://campfirenow.com

Usage
-----

Add the following to your Mercurial config (in a system, user, or
repo-level hgrc file), replacing the API key, URL, and room ID::

    [campfire]
    api_key = CAMPFIRE_AUTH_TOKEN_FOR_THE_USER_NOTIFICATIONS_WILL_COME_FROM
    url = http://myorg.campfirenow.com
    room = 123456

    [hooks]
    changegroup.campfire = python:hgcampfire.notify

These configs can of course be separated into different hgrc files,
for instance if you want to specify the Campfire data user-wide, but
apply the actual hook only to certain repositories.

Customization
-------------

You can modify the template ``hgcampfire`` uses for its notification
by setting the ``template`` config value in the ``[campfire]``
section. The default value is ``{user} pushed:\n{changesets}``. This
template has the following context available to it: ``root`` is the
repository root path, ``user`` is the value of the ``$USER``
environment variable, and ``changesets`` is the list of changesets
pushed.

You can also modify the template ``hgcampfire`` uses to report each
changeset, by setting the ``cset_template`` config value in the
``[campfire]`` section. This should be a Mercurial changeset template,
of the same form you'd pass to --template. The default value is
``* "{desc}" by {author}``.

