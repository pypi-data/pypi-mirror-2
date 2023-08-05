#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import setuptools

if __name__ == '__main__':
    version = '0.2'
    setuptools.setup(
        name='OhlohWidgetsMacro',
        version=version,
        
        description='Trac macro to embed Ohloh widgets',
        author='Felix Schwarz',
        author_email='felix.schwarz@oss.schwarz.eu',
        url='http://www.schwarz.eu/opensource/projects/ohloh_widgets_macro',
        download_url='http://www.schwarz.eu/opensource/projects/ohloh_widgets_macro/download/%s' % version,
        license='MIT',
        
        install_requires=['genshi', 'Trac >= 0.11', 'pycerberus >= 0.3'],
        
        # uses simple_super
        zip_safe=False,
        packages=setuptools.find_packages(exclude=['tests']),
        classifiers = [
            'Development Status :: 4 - Beta',
            'Framework :: Trac',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        entry_points = {
            'trac.plugins': [
                'ohloh_widgets.macro = ohloh_widgets.macro',
                'ohloh_widgets.modifiers = ohloh_widgets.modifiers',
            ]
        }
    )


