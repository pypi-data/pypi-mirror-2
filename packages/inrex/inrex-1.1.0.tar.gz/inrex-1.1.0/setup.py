
from distutils.core import setup

setup(name='inrex',
      description='Regular expressions as infix operations', 
      author='Krister Hedfors', 
      author_email='krister.hedfors+inrex@gmail.com', 
      version='1.1.0', 
      #py_modules=['inrex'],
      packages=['inrex'], 
      #data_files=[('inrex','__init__.py'),  ('inrex', 'inrex.py')], 
      long_description='''
from inrex import  match, search, split, findall, finditer

if 'asd 123' |match| r'(\w+) (\d+)':
    print 'word is', match[0]
    print 'digit is', match[1]

if 'asd 123' |match| r'(?P<word>\w+) (?P<digit>\d+)':
    print 'word is', match['word']
    print 'digit is', match['digit']

print 'asd 123 qwe 456' |findall| r'\d+'
print 'asd 123 qwe 456' |split| r'\d+'
print 'asd 123 qwe 456' |split(maxsplit=1)| r'\d+'
'''
)

