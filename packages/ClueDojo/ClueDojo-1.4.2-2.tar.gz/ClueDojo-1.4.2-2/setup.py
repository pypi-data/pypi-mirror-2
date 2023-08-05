from setuptools import setup, find_packages

version = '1.4.2-2'

readme = open('README.txt').read().strip()
history = open('HISTORY.txt').read().strip()

setup(name='ClueDojo',
      version=version,
      description='Simple Python library to access ' \
                  'the Dojo Javascript toolkit',
      long_description=readme + "\n\n" + history,
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Programming Language :: JavaScript',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      keywords='wsgi dojo javascript ajax',
      author='Rocky Burt',
      author_email='rocky@serverzen.com',
      url='https://dev.serverzen.com/svn/cluemapper/ClueDojo/',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Paste',
          ],
      entry_points={
          'paste.app_factory': [
              'main=cluedojo.wsgiapp:make_app',
              'demoapp=cluedojo.demoapp:make_app',
              ],
          },
      )
