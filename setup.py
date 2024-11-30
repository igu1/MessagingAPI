from setuptools import setup, find_packages

setup(
    name='messaging-api-wrapper',
    version='0.1.0',
    description='A Python package for sending WhatsApp and Email messages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Eza',
    author_email='eesaard@gmail.com',
    url='https://github.com/igu1/MessagingAPI',
    packages=find_packages(),
    install_requires=[
        'requests',
        "Jinja2"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
