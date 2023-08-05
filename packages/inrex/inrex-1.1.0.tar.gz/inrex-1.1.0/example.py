#
# Makes Python stronger than Perl as it now
# competes to become the better text parsing language.
#
from inrex import  match, search, split, findall, finditer

for i in "a1b2c3" |findall| r"\d":
    print i

if 'asd 123' |match| r'(\w+) (\d+)':
    print 'word is', match[0]
    print 'digit is', match[1]

if 'asd 123' |match| r'(?P<word>\w+) (?P<digit>\d+)':
    print 'word is', match['word']
    print 'digit is', match['digit']

print 'asd 123 qwe 456' |findall| r'\d+'
print 'asd 123 qwe 456' |split| r'\d+'

print 'asd 123 qwe 456' |split(maxsplit=1)| r'\d+'

print '\n   files create line-feed generators for regex op:\n'
from StringIO import StringIO
f = StringIO()
f.write('a7b7c7\nx8y8z8\n')
f.seek(0)
for i in f |findall| r'\d': print i

