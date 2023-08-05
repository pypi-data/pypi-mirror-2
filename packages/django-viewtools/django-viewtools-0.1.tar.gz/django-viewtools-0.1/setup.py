from distutils.core import setup

setup(name="django-viewtools",
      version="0.1",
      description="Tools for calling URLs for debugging",
      author="Eric Moritz",
      author_email="eric@themoritzfamily.com",
      url="http://launchpad.net/django-viewtools",
      packages=["viewtools",
                "viewtools.management",
                "viewtools.management.commands"])
