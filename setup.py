from setuptools import setup
from os import path

import formation

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, "requirements.txt"), encoding='utf-8') as req:
    requirements = [i.strip() for i in req.readlines()]

setup(
    name='formation-studio',
    packages=[
        'hoverset', 'hoverset.data', 'hoverset.platform', 'hoverset.ui', 'hoverset.util',
        'formation', 'formation.handlers',
        'studio', 'studio.feature', 'studio.lib', 'studio.parsers', 'studio.ui', 'studio.tools'
    ],
    version=formation.__version__,
    license='MIT',
    description='Simplify GUI development in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hoverset',
    author_email='emmanuelobarany@gmail.com',
    url='https://github.com/ObaraEmmanuel/Formation',
    keywords=['formation', 'gui', 'graphical-user-interface', 'drag drop', 'tkinter', 'hoverset', 'python'],
    install_requires=requirements,
    package_data={
        'hoverset.data': ['image.*'],
        'hoverset.ui': ['themes/*'],
        'studio': ['resources/*/*']
    },
    entry_points={
        'gui_scripts': [
            'formation-studio = studio.main:main',
        ]
    },
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Software Development :: User Interfaces',
        'Operating System :: OS Independent'
    ],
)
