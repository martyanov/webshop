from setuptools import setup, find_packages

setup(name='webshop',
    version='0.1a',
    packages=['paymentform', 'paymentform.i18n', 'mailreceipt',
        'mailreceipt.i18n','webshop'],
    package_data={'paymentform': ['static/epoint.ico', 'static/style.css'],
                  'mailreceipt': ['static/epoint.ico', 'static/style.css']},
    install_requires=[
        "Flask>=0.8",
        "python-gnupg>=0.2.8",
    ],
    test_suite = "tests",
    description='Bob is selling various physical and digital goods over http/https',
    author='Andrey V. Martyanov',
    author_email='realduke@gmail.com',
    url = 'https://www.epointsystem.org/trac/vending_machine/wiki/WebShop'
)
