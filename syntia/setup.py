from setuptools import setup

setup(
    name='syntia',
    version='1.0',
    packages=['syntia', 'syntia.mcts', 'syntia.mcts.grammars', 'syntia.utils'],
    url='https://github.com/arnaugamez/syntia',
    license='GPLv2',
    author='Arnau Gàmez i Montolio (@arnaugamez)',
    author_email='me@arnaugamez.com',
    description='A program synthesis framework for binary code deobfuscation'
)
