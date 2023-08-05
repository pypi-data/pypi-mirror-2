from distutils.core import setup
import os

readme_file = os.path.join(os.path.dirname(__file__),
                           'README')
long_description = open(readme_file).read()    
setup(name='django-emailform',
      version='0.1',
      description='Django app for creating multi-input forms with no default fields, with optional email notification of entries.',
      long_description=long_description,
      author='Glenn Mohre',
      author_email='glenn.mohre@gmail.com',
      url='http://www.bitbucket.org/glennmohre/django-emailform',
      packages=['emailform'],
      license='MIT',
     )
