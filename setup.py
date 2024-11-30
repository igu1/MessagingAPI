from setuptools import setup, find_packages

setup(
    name='MessagingAPI',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        "Jinja2"
    ],
    description='A package for sending emails and WhatsApp messages',
    author='Eza',
    author_email='eesaard@gmail.com',
    url='https://github.com/igu1/MessagingAPI',
)
