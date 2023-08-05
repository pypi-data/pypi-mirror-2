from setuptools import setup, find_packages

setup(
    name = "greatape",
    version = "0.3.2",
    url = 'http://github.com/threadsafelabs/greatape',
    license = 'BSD',
    description = "A MailChimp API client.",
    author = 'Jonathan Lukens',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
