# coding=utf-8
# output parsers for pieberry
from pieberry_config import *
import string, re, os, sys
import traceback

class pieAllWriter:
    '''Meta-class that directs different types of output'''
    def __init__(self, entries=[]):
        '''entries is a list of bibdata dicts'''
        self._entries = entries
        self._location = config.get('PBoptions', 'default_bibliography')
        if PYBTEX:
            self._bibtex_writer = piePybtexWriter()
        else:
            self._bibtex_writer = pieBibtexWriter()
        self._tsv_writer = pieTSVWriter()

    def addEntry(self, bibdata):
        '''Add an entry to the output file'''
        self._bibtex_writer.addEntry(bibdata)
        if config.getboolean('PBoptions', 'export_tsv'):
            self._tsv_writer.addEntry(bibdata)

    def setLocation(self, location):
        '''Set the location of the file'''
        self._bibtex_writer.setLocation(location)
        if config.getboolean('PBoptions', 'export_tsv'):
            self._tsv_writer.setLocation(location)

    def write(self):
        '''Write to file. 'types' is a tuple of "contexts" to exclude
        from the write-out process, such as submissions.'''
        self._bibtex_writer.write()
        if config.getboolean('PBoptions', 'export_tsv'):
            self._tsv_writer.write()

class piePybtexWriter:
    '''Class to write out bibliographies as BibTex'''
    def __init__(self, entries=None):
        '''entries is a list of bibdata dicts'''
        self._entries = []
        self._location = config.get('PBoptions', 'default_bibliography')

    def addEntry(self, bibdata):
        '''Add an entry to the output file'''
        self._entries.append(bibdata)

    def setLocation(self, location):
        '''Set the location of the file'''
        self._location = location

    def write(self, backup=True):
        '''Write to file. 'types' is a tuple of "contexts" to exclude
        from the write-out process, such as submissions.'''
        if os.path.exists(self._location):
            try:
                # backup 
                f = open(self._location, 'r')
                if backup:
                    b = open(os.path.join(os.path.split(self._location)[0], 'backup.bib'), 'w')
                    b.write(f.read())
                    b.close()
                f.close()
            except:
                raise 'Could not open file'
        else:
            f = open(self._location, 'w')
            f.write('')
            f.close()
        try:
            from pybtex.database.input import bibtex
            from pybtex.database.output.bibtex import Writer
            from pybtex.database import BibliographyDataError
            from pybtex.core import Entry, Person
            from pybtex.bibtex.utils import split_name_list
            from pieberry_pybtex import pieberry_to_pybtex
        except:
            traceback.print_exc()
            raise 'Could not import pybtex'

        parser = bibtex.Parser()
        bib_object = parser.parse_file(self._location)
        for ent in self._entries:
            if ent['exclude'] == True:
                continue
            new_pybtex_entry = pieberry_to_pybtex(ent, texify=True)
            bib_key = autogen_bibtex_key(ent)
            invalid_key = True
            while invalid_key:
                invalid_key = False
                try:
                    bib_object.add_entry(bib_key, new_pybtex_entry)
                except BibliographyDataError:
                    invalid_key = True
                    bib_key = increment_bibtex_key(bib_key)
        # import latex_codec
        # latex_codec.register()
        writer = Writer(encoding='utf-8')
        writer.write_file(bib_object, self._location)
                    
class pieBibtexWriter:
    '''Class to write out bibliographies as BibTex'''
    def __init__(self, entries=None):
        '''entries is a list of bibdata dicts'''
        self._entries = []
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
        savedata = ''
        for entry in self._entries:
            if entry['exclude'] == False:
                try:
                    savedata = savedata + format_bibtex_entry(entry)
                except UnicodeDecodeError:
                    print 'Bad unicode - omitting'
                except: 
                    traceback.print_exc()
                    print 'Unknown formatting error'
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
    def __init__(self, entries=None):
        self._entries = []
        self._location = os.path.splitext(config.get('PBoptions', 'default_bibliography'))[0] + '.tsv'

    def addEntry(self, bibdata):
        '''Add an entry to the output file'''
        self._entries.append(bibdata)

    def setLocation(self, location):
        '''Set the location of the file'''
        self._location = os.path.splitext(location)[0] + '.tsv'

    def write(self):
        '''Write to file. 'types' is a tuple of "contexts" to exclude
        from the write-out process, such as submissions.'''
        from pprint import pprint
        lines = []
        header = []
        if os.path.exists(self._location):
            f = open(self._location, 'r')
            lines = [line.rstrip().split('\t') for line in f.readlines()]
            f.close()
        if lines:
            header = lines[0]
        else:
            header = ('bibtex_key', 'author', 'title', 'year', 'month', 'howpublished', 'url', 'final_fn')
            lines.append(header)
        pprint(header)
        for ent in self._entries:
            if ent['exclude'] == True:
                continue
            row = []
            for col in header:
                if ent.has_key(col):
                    row.append(ent[col])
                else:
                    row.append('')
            lines.append(row)
        pprint(lines)
        f = open(self._location, 'w')
        f.writelines(['%s\n' % string.join(line, '\t') for line in lines])
        f.close()

def escape_bad_latex_chars(texstring):
    '''ensure that LaTeX-unsafe characters are escaped'''
    print 'eblc'
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

def unescape_bad_latex_chars(texstring):
    '''get rid of LaTeX-friendly escaping'''
    invalidchars = (r'#', r'$', r'%', r'&') # , r'_') #, '{', '}'
    valid_escapes = (r'\#', r'\$', r'\%', r'\&') # , r'\_')
    for k in range(len(invalidchars)):
        texstring = string.replace(texstring, valid_escapes[k], invalidchars[k])
    return texstring

def untexify(texstring):
    '''remove curly braces and other tex-related stuff'''
    # TODO this is unlikely to work if there's more than one latex macro
    re_tex = re.compile(r'\\.+?\{(.+)\}')
    tex_match = re_tex.search(texstring)
    if tex_match:
        texstring = re_tex.sub(tex_match.group(1), texstring)
    texstring = unescape_bad_latex_chars(texstring)
    transtbl = {ord('{'): None, ord('}'): None}
    texstring = texstring.translate(transtbl)
    return texstring

def format_bibtex_entry(bibdict):
    '''format a single bibtex entry'''
    if bibdict.has_key('bibtex_key'):
        key = bibdict['bibtex_key']
    else:
        key = autogen_bibtex_key(bibdict)
    author = bibdict['author']
    if bibdict.has_key('corporate_author'):
        if bibdict['corporate_author']:
            author = "{%s}" % bibdict['author']
    ent = """
@%s{%s,
  author = {%s},
  title = {%s},
  howpublished = {\href{%s}{On the web}},
  month = {%s},
  year = %s,
  annote = {%s}}

""" % (
        bibdict['bibtex_type'].encode('utf-8'),
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

def increment_bibtex_key(keytext):
     '''add digits to end of key to try to avoid identical keys'''
     try:
         last_digit = int(keytext[-1])
         if last_digit == 9:
             key_base = keytext
             last_digit = -1
         else:
             key_base = keytext[:-1]
     except:
         last_digit = -1
         key_base = keytext
     last_digit += 1
     print 'generated key %s%d' % (key_base, last_digit)
     return '%s%d' % (key_base, last_digit)

if __name__ == '__main__':
    import time
    spoofdata = {
        'title': 'Spoof title',
        'author': '{Goldman Saks}',
        'year': '1833',
        'month': 'January',
        'howpublished': 'Mungdinügn',
        'url': 'http://www.themong.spo.nn/a%20b.html',
        'annote': 'notey',
        'ancillary_downloadtime': time.localtime(),
        'ancillary_creationtime': time.localtime(),
        'ancillary_outfilename': 'C:noodles',
        'ancillary_locofdoc': 'http://www.hell.no',
        'exclude': True,
        'internal_author': 'Jon Hoo',
        'internal_title': 'Noh Wai'
        }
    

    w = piePybtexWriter()
    w.addEntry(spoofdata)
    w.write()
