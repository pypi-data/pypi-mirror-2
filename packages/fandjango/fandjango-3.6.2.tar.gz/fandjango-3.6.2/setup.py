from distutils.core import setup

setup(
  name = 'fandjango',
  version = '3.6.2',
  description = "Fandjango makes it easy to create Facebook applications powered by Django",
  author = "Johannes Gorset",
  author_email = "jgorset@gmail.com",
  url = "http://github.com/jgorset/fandjango",
  packages = ['fandjango', 'fandjango.migrations']
)
