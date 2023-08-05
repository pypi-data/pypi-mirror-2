# output parsers for pieberry
from pieberry_config import *
import string, re, os, sys

class pieAllWriter:
    '''Meta-class that directs different types of output'''
    def __init__(self, entries=[]):
        '''entries is a list of bibdata dicts'''
        self._entries = entries
        self._location = config.get('PBoptions', 'default_bibliography')

    def addEntry(self, bibdata):
        '''Add an entry to the output file'''
        self._entries.append(bibdata)

    def setLocation(self, location):
        '''Set the location of the file'''
        self._location = location

    def write(self):
        '''Write to file. 'types' is a tuple of "contexts" to exclude
        from the write-out process, such as submissions.'''
        pass

class pieBibtexWriter:
    '''Class to write out bibliographies as BibTex'''
    def __init__(self, entries=None):
        '''entries is a list of bibdata dicts'''
        self._entries = []
        print 'I HAVE %d ENTRIES!!!' % len(self._entries)
        self._location = config.get('PBoptions', 'default_bibliography')

    def addEntry(self, bibdata):
        '''Add an entry to the output file'''
        self._entries.append(bibdata)

    def setLocation(self, location):
        '''Set the location of the file'''
        self._location = location

    def write(self):
        '''Write to file. 'types' is a tuple of "contexts" to exclude
        from the write-out process, such as submissions.'''
        # print self._entries
        savedata = ''
        for entry in self._entries:
            if entry['exclude'] == False:
                savedata = savedata + format_bibtex_entry(entry)
        if os.path.exists(self._location):
            outfile = open(self._location, 'r')
            current_data = outfile.read()
            outfile.close()
            savedata = current_data + savedata
        outfile = open(self._location, 'w')
        outfile.write(savedata)
        outfile.close()

class pieTSVWriter:
    '''Class to write out bibliographies in TSV with potentially
    arbitrary columns'''
    def __init__(self, entries=[]):
        self._entries = entries

    def addEntry(self, bibdata):
        '''Add an entry to the output file'''
        pass

    def setLocation(self, location):
        '''Set the location of the file'''
        self._location = location

    def write(self, excludetypes):
        '''Write to file. 'types' is a tuple of "contexts" to exclude
        from the write-out process, such as submissions.'''
        pass

def escape_bad_latex_chars(texstring):
    '''ensure that LaTeX-unsafe characters are escaped'''
    invalidchars = (r'#', r'$', r'%', r'&') # , r'_') #, '{', '}'
    valid_escapes = (r'\#', r'\$', r'\%', r'\&') # , r'\_')
    replace_chars = ('LATEXHASH', 'LATEXDOLLAR', 'LATEXPERCENT', 'LATEXAMPERSAND')
    for k in range(len(invalidchars)):
        ch = valid_escapes[k]
        texstring = string.replace(texstring, ch, replace_chars[k])
    for k in range(len(invalidchars)):
        ch = invalidchars[k]
        texstring = string.replace(texstring, ch, valid_escapes[k])
    for k in range(len(invalidchars)):
        texstring = string.replace(texstring, replace_chars[k], valid_escapes[k])
    return texstring

def format_bibtex_entry(bibdict):
    '''format a single bibtex entry'''
    if bibdict.has_key('bibtex_key'):
        key = bibdict['bibtex_key']
    else:
        key = autogen_bibtex_key(bibdict)
    if bibdict['corporate_author']:
        author = "{%s}" % bibdict['author']
    else:
        author = bibdict['author']
    ent = """
@Misc{%s,
  author = {%s},
  title = {%s},
  howpublished = {\href{%s}{Web site}},
  month = {%s},
  year = %s,
  annote = {%s}}

""" % (
        key,
        escape_bad_latex_chars(author).encode('utf-8'),
        escape_bad_latex_chars(bibdict['title']).encode('utf-8'),
        escape_bad_latex_chars(bibdict['howpublished']).encode('utf-8'),
        bibdict['month'].encode('utf-8'),
        bibdict['year'].encode('utf-8'),
        escape_bad_latex_chars(bibdict['annote']).encode('utf-8')
        )
    return ent

def autogen_bibtex_key(bibdict):
    keytitlecompact = string.join([i[:3] for i in string.split(bibdict['title'].encode("utf-8").translate(string.maketrans("",""), string.punctuation)) if len(i) > 3], '') #ouch ... this compacts the first three letters of each word in the title together, to make a dependably unique key
    keyauthorcompact = string.join([i[:1] for i in string.split(bibdict['author'].encode("utf-8").translate(string.maketrans("",""), string.punctuation)) if len(i) > 3], '') #same for authors, but just initials
    key = "%s%s_%s" % (
        keyauthorcompact,
        bibdict['year'].encode('utf-8'), 
        keytitlecompact
        )
    return key
