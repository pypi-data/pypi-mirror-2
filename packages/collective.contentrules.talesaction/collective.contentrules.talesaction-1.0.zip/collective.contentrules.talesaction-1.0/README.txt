Introduction
============

Installation
------------

Add collective.contentrules.talesaction to the 'egg' parameter of your buildout section ::

    [buildout]
    ...
    eggs +=
        ...
        collective.contentrules.talesaction

Or add it to the install_requires parameter of the setup.py of your module ::

    setup(
        ...
       install_requires=[
        ...
        'collective.contentrules.talesaction',
        ]

Then restart your buildout and your instance.

Use
---

Go to the `Rules` section of `Site configuration`.
You can now add `TALES Expression action` to the actions of your rules.