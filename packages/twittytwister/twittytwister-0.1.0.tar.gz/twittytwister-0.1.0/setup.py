try:
    from setuptools import setup
except:
    from distutils.core import setup


def getVersion():
    import os
    packageSeedFile = os.path.join("twittytwister", "_version.py")
    ns = {"__name__": __name__, }
    execfile(packageSeedFile, ns)
    return ns["version"]

version = getVersion()


setup(
    name = version.package,
    version = version.short(), 
    description = "Twitter client for Twisted Python",

    author = "Dustin Sallings",
    author_email = "dustin@spy.net",
    url = "http://github.com/dustin/twitty-twister/",

    maintainer = "Oliver Gould",
    maintainer_email = "ver@olix0r.net",
    download_url = "http://pypi.python.org/pypi/twittytwister",

    license = 'MIT',
    classifiers = [
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
         ],

    platforms = "any",
    packages = ["twittytwister", ],
    requires = ["oauth", "twisted", "twisted.web", ]
    )

