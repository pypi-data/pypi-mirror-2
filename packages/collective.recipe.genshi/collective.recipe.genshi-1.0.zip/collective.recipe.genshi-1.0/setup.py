from setuptools import setup

setup(
    name='collective.recipe.genshi',
    version="1.0",
    description="Buildout recipe to generate a text file from a genshi template.",
    long_description="""\
This recipe is just a wrapper around collective.recipe.template_ using the
Genshi_ extras_require to work around a `bug in zc.buildout`_ which causes the
Genshi dependency to not be installed in some cases.

.. _collective.recipe.template: http://pypi.python.org/pypi/collective.recipe.template
.. _Genshi: http://genshi.edgewall.org/wiki/Documentation/text-templates.html
.. _bug in zc.buildout: https://bugs.launchpad.net/bugs/583752
""",
    classifiers=[
      "Framework :: Buildout",
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='template recipe',
    author='Florian Schulze',
    author_email='florian.schulze@gmx.net',
    url='http://svn.plone.org/svn/collective/buildout/collective.recipe.genshi/trunk',
    license='BSD',
    install_requires=[
        'collective.recipe.template [genshi]',
    ],
    entry_points="""
      [zc.buildout]
      default = collective.recipe.template.genshitemplate:Recipe
      """,
)