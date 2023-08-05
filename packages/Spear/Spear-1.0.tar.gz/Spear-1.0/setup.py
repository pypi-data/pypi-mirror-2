#!/usr/bin/env python
from distutils.core import setup

setup(
    name="Spear",
    version="1.0",
    keywords='research SPEAR ranking folksonomies expertise HITS spam information retrieval',
    description="The reference implementation of the SPEAR ranking algorithm in Python",
    long_description="""
    The purpose of this implementation is to make the inner workings of
    the algorithm easy to understand and not to distract or confuse
    the reader with highly optimized code.

    The SPEAR algorithm takes a list of user activities on resources
    as input, and returns ranked lists of users by expertise scores
    and resources by quality scores, respectively.

    You can also use this library to simulate the HITS algorithm of
    Jon Kleinberg. Simply supply a credit score function C(x) = 1 to
    the SPEAR algorithm (see documentation of Spear.run()).

    More information about the SPEAR algorithm is available at:
    * http://www.spear-algorithm.org/
    * "Telling Experts from Spammers: Expertise Ranking in Folksonomies"
      Michael G. Noll, Ching-man Au Yeung, et al.
      SIGIR 09: Proceedings of 32nd International ACM SIGIR Conference
      on Research and Development in Information Retrieval, Boston, USA,
      July 2009, pp. 612-619, ISBN 978-1-60558-483-6

    The code is licensed to you under version 2 of the GNU General Public
    License.

    Copyright 2009-2010 Michael G. Noll <http://www.michael-noll.com/>
                        Ching-man Au Yeung <http://www.albertauyeung.com/>

    """,
    author="Michael G. Noll",
    author_email="michael[AT]quuxlabs[DOT]com",
    license='GNU General Public License version 2',
    url="http://www.quuxlabs.com/",
    py_modules=['spear'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Sociology',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=["scipy", "numpy"],
)
