# Copyright 2009-2010 numero, theothernumber.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages


setup(name='prospero',
      version='0.5',
      description='Prospero - RESTful Datastore',
      long_description = """
        Prospero is a datastore which addresses content using a RESTful interface. 
        """,
      author='numero',
      author_email='hi@theothernumber.com',
      url='http://pypi.python.org/pypi/prospero',
      packages=['prospero', 'prospero/security/', 'prospero/utils/','tests'],
      keywords = ('mongo', 'tornado', 'REST'),
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: Apache Software License',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
          license = "Apache License, Version 2.0",
        requires=['pymongo (>=1.52)', 'simplejson (>=2.1.0)', 'tornado (>=0.2)', 'amfast (>=0.5.1)', 'pygments (>=1.3.1)'],
      )

