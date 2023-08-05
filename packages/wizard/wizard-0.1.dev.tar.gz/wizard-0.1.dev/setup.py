import setuptools

setuptools.setup(
    name = 'wizard',
    version = '0.1.dev',
    author = 'The Wizard Team',
    author_email = 'scripts-team@mit.edu',
    description = ('A next-generation autoinstall management system'),
    license = 'MIT',
    url = 'http://scripts.mit.edu/wizard',
    packages = setuptools.find_packages(exclude=["tests", "plugins"]),
    install_requires = ['decorator'], # versions?
    keywords = "autoinstall webapp deploy",
)
