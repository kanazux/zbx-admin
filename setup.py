from setuptools import setup


setup(name='zbx-admin',
      version='0.1',
      license='BSD2CLAUSE',
      install_requires=['zabbix-api', 'requests'],
      packages=['zbx_admin'],
      package_data={'zbx_admin': ['zbx_admin/*']},
      data_files=[('LICENSE')],
      entry_points={'console_scripts': ['zbx_admin=zbx_admin.__main__:main']},
      description='A tool to get and input data on Zabbix Server.',
      long_description=("Use to import configuration, export and get items in json format."),
      author='Silvio Ap Silva a.k.a Kanazuchi',
      author_email='contato@kanazuchi.com',
      url='http://github.com/kanazux/zbx-admin',
      zip_safe=False)