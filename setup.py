from distutils.core import setup


setup(name='RequestManager',
      version='1.0',
      description='Class used to manage a specific request to a endpoint, and try again if specific errors appear',
      author='Leandro Alves',
      author_email='leandro.augusto.alves@outlook.com.br',
      url='https://bitbucket.org/nappsolutionsdev/scrapping_model/src/scrapping_model/',
      packages=['request_manager'],
      install_requires=[
      'playwright',
      'bs4',
      'requests',
      're']
     )
