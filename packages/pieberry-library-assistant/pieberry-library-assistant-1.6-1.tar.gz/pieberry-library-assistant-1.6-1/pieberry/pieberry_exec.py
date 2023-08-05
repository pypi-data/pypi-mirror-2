#!/bin/python

# for python 2.6
# dependencies - wxpython, beautiful soup, pypdf

import sys, os, os.path, getopt, re, time
import urllib
import urllib2
import string
import traceback
from htmlentitydefs import name2codepoint as n2cp
from BeautifulSoup import *
import urlparse
import wx
import re
from pyPdf import PdfFileWriter, PdfFileReader
from pieberry_config import *
from pieberry_events import *

user_agent = 'Mozilla/Linux'
headers = { 'User-Agent' : user_agent }
re_submission = re.compile(r'^(.+?)(\'s)?( -)? [sS]ubmission')

def wxdate2pydate(date): 
     import datetime 
     assert isinstance(date, wx.DateTime) 
     if date.IsValid(): 
         ymd = map(int, date.FormatISODate().split('-')) 
         return datetime.date(*ymd) 
     else: 
         return None 

def substitute_entity(match):
    ent = match.group(2)
    if match.group(1) == "#":
        return unichr(int(ent))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute_entity, string)[0]

def translate_non_alphanumerics(to_translate, translate_to=u'_'):
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    if isinstance(to_translate, unicode):
        translate_table = dict((ord(char), unicode(translate_to))
                               for char in not_letters_or_digits)
    else:
        assert isinstance(to_translate, str)
        translate_table = string.maketrans(not_letters_or_digits,
                                           translate_to
                                              *len(not_letters_or_digits))
    return to_translate.translate(translate_table)

def fetch_page(notify_winddow, url):
    '''fetch a page. that is all'''
    try:    
        thepage = urllib2.urlopen(url)
    except ValueError:
        traceback.print_exc()
        wx.PostEvent(notify_window, pieUpdateEvent('warn', "Not a valid or recognised url"))
        raise ValueError
    except urllib2.HTTPError: 
        traceback.print_exc()
        wx.PostEvent(notify_window, pieUpdateEvent('warn', "Could not access website"))
        raise Exception
    thehtml = thepage.read()
    return thehtml

def snarf_pdfs(notify_window, html, url):
    '''get all pdfs on a given page. return list of dicts:
    { pdflink, pdflink_text, pdflink_context } 
    pdflink_context can be one of "submissions" ... '''
    try:
        readup = BeautifulSoup(html)
    except Exception, err:
        traceback.print_exc()
        wx.PostEvent(notify_window, pieUpdateEvent('warn', "Invalid or unparseable HTML"))
        raise Exception
    pdflinks = readup.findAll('a', href=re.compile("^.*\.(PDF|pdf)"))
    if not pdflinks:
        wx.PostEvent(notify_window, pieUpdateEvent('warn', 'No pdf links found'))
        raise Exception
    wx.PostEvent(notify_window, pieUpdateEvent('blank', 'Starting (Found %d files)' % len(pdflinks)))
    head_re = re.compile('[hH][1-7]')
    sub_re = re.compile('[Ss]ubmission')
    retlist = []
    all_are_submissions = ('ubmissions' in readup.title.string)
    for link in pdflinks:
        ret = {
            'pdflink': '',
            'pdflink_text': '',
            'pdflink_context': ''}
        doctext = link.findChildren(text=True)
        nameofdoc = string.join(doctext, " ").decode('utf-8')
        nameofdoc = decode_htmlentities(nameofdoc)
        # Get rid of filename extension
        if nameofdoc[-4:] in ('.pdf', '.PDF', '.Pdf'):
            nameofdoc = nameofdoc[:-4]
        ret['pdflink_text'] = nameofdoc
        # Determine whether this is a submission and flag accordingly
        if sub_re.search(nameofdoc):
            ret['pdflink_context'] = 'submissions'
        # If 'submission' in the last headings do same
        head_h = link.findPrevious(head_re)
        if head_h:
            if sub_re.search(head_h.text):
                ret['pdflink_context'] = 'submissions'
        if all_are_submissions:
             ret['pdflink_context'] = 'submissions'
        # Finally assign relevant link
        # try to work out if the link is already quoted text or not
        if "%" in  link['href'].encode('utf-8'):
            pathstub = link['href'].encode('utf-8')
        else:
            pathstub = urllib.quote(link['href'].encode('utf-8'))
        ret['pdflink'] = urlparse.urljoin(url, pathstub)
        retlist.append(ret)
    return retlist

def download_pdf(notify_window, pdfinfo, author, tag):
    '''download a pdf and return its location.'''
    try:
        tr_fn = translate_non_alphanumerics(pdfinfo['pdflink_text'])[:100] + ".pdf"
        output_directory = os.path.join(config.get('PBoptions', 'workingdir'), author, tag, pdfinfo['pdflink_context'])
        if not os.path.isdir(output_directory): 
            os.makedirs(output_directory)
        existfiles = [fl[9:] for fl in os.listdir(output_directory)] #files with their date prefixes stripped out
        if tr_fn in existfiles: 
            wx.PostEvent(notify_window, pieUpdateEvent('pass', 'Already downloaded', cite=pdfinfo['pdflink_text'], href=pdfinfo['pdflink'], updatelast=True))
            return
        outfilename = os.path.join(output_directory, tr_fn)            
        doc = urllib2.urlopen(pdfinfo['pdflink'])
        docdata = doc.read()
        outfile = open(outfilename, 'wb')
        outfile.write(docdata)
        outfile.close()
        return outfilename
    except Exception, err:
        traceback.print_exc()
        wx.PostEvent(notify_window, pieUpdateEvent('fail', "FAILED to download", cite=pdfinfo['pdflink_text'], href=pdfinfo['pdflink'], updatelast=True))
        raise Exception

def get_internal_pdf_metadata(notify_window, pdfinfo):
    retinfo = {}
    retinfo['creation_date'] = time.localtime()
    retinfo['internal_author'] = ''
    retinfo['internal_title'] = ''
    try:
        pdf_file = file(pdfinfo['outfilename'], 'rb')
        pdfread = PdfFileReader(pdf_file)
        docmetadata = pdfread.getDocumentInfo()
    except:
        traceback.print_exc()
        wx.PostEvent(notify_window, pieUpdateEvent('fail', "Unreadable", cite=pdfinfo['pdflink_text'], href=pdfinfo['outfilename'], updatelast=True))
        pdf_file.close()
        return retinfo
    if docmetadata == None:
        docmetadata = {} #pyPdf appears to send Nonetypes instead of
                         #empty dicts, annoyingly
    # creation date is found here. if not present, fall back to current date
    try:
        if docmetadata.has_key('/CreationDate'):
            rd = docmetadata['/CreationDate'][2:]
            retinfo['creation_date'] = time.strptime("%s %s %s %s %s" % (rd[0:4], rd[4:6], rd[6:8], rd[8:10], rd[10:12]), "%Y %m %d %H %M")
            retinfo['creation_date_guessed'] = False
        else:
            retinfo['creation_date_guessed'] = True
    except: #hack ... but sometimes /creationdate is bunged
        traceback.print_exc()
        retinfo['creation_date_guessed'] = True

    retinfo['download_time'] = time.localtime()
    # some reformatting necessary when author names are computer-inserted
    splre = re.compile("[./_ ]")
    authst = ''
    if not pdfread.documentInfo:
        return retinfo
    if pdfread.documentInfo.author:
        authst = string.join(splre.split(pdfread.documentInfo.author))
        authst = string.capwords(authst)
    retinfo['internal_author'] = authst
    retinfo['internal_title'] = unicode(pdfread.documentInfo.title)
    pdf_file.close()
    return retinfo
        
def gen_title_and_docname(pdfinfo, behaviour):
    '''format the appropriate title and document name'''
    retdata = {}
    if behaviour == 'prepend':
        retdata['title'] = "%s: %s" % (pdfinfo['tag'], pdfinfo['pdflink_text'])
    elif behaviour == 'append_hyphen':
        retdata['title'] = "%s - %s" % (pdfinfo['pdflink_text'], pdfinfo['tag'])
    elif behaviour == 'append_brackets':
        retdata['title'] = "%s (%s)" % (pdfinfo['pdflink_text'], pdfinfo['tag'])
    else:
        retdata['title'] = pdfinfo['pdflink_text']
    final_fn = os.path.join(config.get('PBoptions', 'workingdir'), pdfinfo['author'], pdfinfo['tag'], pdfinfo['pdflink_context'], "%s %s" % (time.strftime("%Y%m%d", pdfinfo['creation_date']), os.path.basename(pdfinfo['outfilename'])))
    retdata['final_fn'] = final_fn
    return retdata

# def scrapeme(url, config, tag='', author='', prefix='', postfix=None, usepostfix=True, notify_window=None):
#     """Read the page and find all pdf links contained within"""
#     try:    
#         thepage = urllib2.urlopen(url)
#     except ValueError:
#         traceback.print_exc()
#         wx.PostEvent(notify_window, pieUpdateEvent('warn', "Not a valid or recognised url"))
#         return
#     except urllib2.HTTPError: 
#         traceback.print_exc()
#         return 

#     thehtml = thepage.read()
#     try:
#         readup = BeautifulSoup(thehtml)
#     except Exception, err:
#         traceback.print_exc()
#         wx.PostEvent(notify_window, pieUpdateEvent('warn', "Invalid or unparseable HTML"))
#         return
#     #TODO use urlparse.urljoin() 

#     thebib = {}
#     pdflinks = readup.findAll('a', href=re.compile("^.*\.(PDF|pdf)"))
#     wx.PostEvent(notify_window, pieUpdateEvent('blank', 'Starting (Found %d files)' % len(pdflinks)))
#     num_pdf_links = len(pdflinks)
#     curr_pdf_link = 0

#     for pdflink in pdflinks:
#         curr_pdf_link += 1
#         bibdata = {}
#         doctext = pdflink.findChildren(text=True)
#         nameofdoc = string.join(doctext, " ").decode('utf-8')
#         nameofdoc = decode_htmlentities(nameofdoc)
#         if '.pdf' in nameofdoc: #in case the web site is quoting full file name
#             nameofdoc = string.split(nameofdoc, '.pdf')[0]
#         if '.PDF' in nameofdoc: #in case the web site is quoting full file name
#             nameofdoc = string.split(nameofdoc, '.PDF')[0]
#         #use page's title bar as postfix if no explicit postfix declared
#         if usepostfix and not postfix: 
#             postfix = readup.title.string.split(' - ')[0].strip()
#             nameofdoc = nameofdoc + ' - ' + postfix
#         elif usepostfix and postfix:
#             nameofdoc = nameofdoc + ' - ' + postfix

#         # try to work out if the link is already quoted text or not
#         if "%" in  pdflink['href'].encode('utf-8'):
#             pathstub = pdflink['href'].encode('utf-8')
#         else:
#             pathstub = urllib.quote(pdflink['href'].encode('utf-8'))

#         locofdoc = urlparse.urljoin(url, pathstub)
#         bibdata['ancillary_locofdoc'] = locofdoc
#         bibdata['title'] = nameofdoc
#         #we want to be able to navigate back to the document in LaTeX
#         #with the aid of hyperref
#         bibdata['howpublished'] = "\href{%s}{Web site}" % string.replace(locofdoc, '%', r'\%')

#         try:
#             wx.PostEvent(notify_window, pieUpdateEvent('warn', '[%d/%d] Downloading' % (curr_pdf_link, num_pdf_links), cite=bibdata['title'], href=locofdoc))
#             tr_fn = translate_non_alphanumerics(nameofdoc)[:100] + ".pdf"
#             # if os.path.exists(outfilename): continue # don't download twice
#             existfiles = [fl[9:] for fl in os.listdir(os.path.join(config.get('PBoptions', 'workingdir'), author, tag))] #files with their date prefixes stripped out
#             if tr_fn in existfiles: 
#                 wx.PostEvent(notify_window, pieUpdateEvent('pass', 'Already downloaded', cite=bibdata['title'], href=locofdoc, updatelast=True))
#                 continue #don't download twice

#             outfilename = os.path.join(config.get('PBoptions', 'workingdir'), author, tag, tr_fn)            
#             doc = urllib2.urlopen(locofdoc)
#             docdata = doc.read()
#             outfile = open(outfilename, 'wb')
#             outfile.write(docdata)
#             outfile.close()
#         except Exception, err:
#             traceback.print_exc()
#             wx.PostEvent(notify_window, pieUpdateEvent('fail', "FAILED to download", cite=bibdata['title'], href=locofdoc, updatelast=True))
#             continue

#         wx.Yield()

#         # Move to reading the pdf's data and get appropriate metadata
#         try:
#             pdf_file = file(outfilename, 'rb')
#             pdfread = PdfFileReader(pdf_file)
#             docmetadata = pdfread.getDocumentInfo()
#         except:
#             wx.PostEvent(notify_window, pieUpdateEvent('fail', "FAILED unreadable", cite=bibdata['title'], href=outfilename, updatelast=True))
#             continue

#         if docmetadata == None:
#             docmetadata = {} #pyPdf appears to send Nonetypes instead
#                              #of empty dicts, annoyingly

#         bibdata['annote'] = 'Downloaded on: %s\n' % time.ctime()
#         # If there's internal data for creation date, use that for the
#         # bibliography. Otherwise, use the current date.
#         if docmetadata.has_key('/CreationDate'):
#             rd = docmetadata['/CreationDate'][2:]
#             encdate = time.strptime("%s %s %s %s %s" % (rd[0:4], rd[4:6], rd[6:8], rd[8:10], rd[10:12]), "%Y %m %d %H %M")
#             bibdata['year'] = unicode(time.strftime("%Y", encdate))
#             bibdata['month'] = unicode(time.strftime("%B", encdate))
#         else:
#             bibdata['year'] = unicode(time.strftime("%Y"))
#             bibdata['month'] = unicode(time.strftime("%B"))
#             bibdata['annote'] = bibdata['annote'] + 'Creation date was unavailable - used date of download\n'
#             encdate = time.localtime()
#         bibdata['ancillary_downloadtime'] = time.localtime()
#         bibdata['ancillary_creationtime'] = encdate

#         # If we've not set a global author for these docs, try to
#         # figure it out from the metadata
#         bibdata['author'] = "{" + author + "}"
#         if docmetadata.has_key('/Author'):
#             splre = re.compile("[./ ]")
#             authst = string.join(splre.split(docmetadata['/Author']))
#             authst = string.capwords(authst)
#             if author == "Unknown":
#                 bibdata['author'] = authst
#             else:
#                 bibdata['annote'] = bibdata['annote'] + 'Auth_from_metadata: ' + authst + '\n'

#         #rather dodgy assumption that submissions are always titled 'person's submission ... '
#         submatch = re_submission.match(nameofdoc)
#         if submatch:
#             bibdata['author'] = "{%s}" % submatch.group(1)

#         if docmetadata.has_key('/Title'):
#             bibdata['annote'] = bibdata['annote'] + 'Title_from_metadata: %s\n' % docmetadata['/Title']
        
#         #append file creation date digits to filename to aid archival
#         pdf_file.close()
#         final_fn = os.path.join(config.get('PBoptions', 'workingdir'), author, tag, "%s %s" % (time.strftime("%Y%m%d", encdate), tr_fn))
#         try:
#             os.rename(outfilename, final_fn)
#             bibdata['annote'] = bibdata['annote'] + 'Saved to: %s\n' % final_fn
#             bibdata['ancillary_outfilename'] = final_fn
#         except:
#             traceback.print_exc()
#             print 'Could not rename file'
#             bibdata['annote'] = bibdata['annote'] + 'Saved to: %s\n' % outfilename
#             bibdata['ancillary_outfilename'] = outfilename

#         data_id = wx.NewId()
#         thebib[data_id] = bibdata
#         wx.PostEvent(notify_window, pieUpdateEvent('success', 'Success', cite="%s (%s). %s" % (bibdata['author'][1:-1], bibdata['year'], bibdata['title']), href=locofdoc, data_id=data_id, updatelast=True))

#     return thebib

# def autogen_bibtex_key(bibdict):
#     keytitlecompact = string.join([i[:3] for i in string.split(bibdict['title'].encode("utf-8").translate(string.maketrans("",""), string.punctuation)) if len(i) > 3], '') #ouch ... this compacts the first three letters of each word in the title together, to make a dependably unique key
#     keyauthorcompact = string.join([i[:1] for i in string.split(bibdict['author'].encode("utf-8").translate(string.maketrans("",""), string.punctuation)) if len(i) > 3], '') #same for authors, but just initials
#     key = "%s%s_%s" % (
#         keyauthorcompact,
#         bibdict['year'].encode('utf-8'), 
#         keytitlecompact
#         )
#     return key

# def increment_bibtex_key(keytext):
#      '''add digits to end of key to try to avoid identical keys'''
#      try:
#           last_digit = int(keytext[-1])
#           if last_digit == 9:
#                key_base = keytext
#                last_digit = 0
#           else:
#                key_base = keytext[:-1]
#      except:
#           last_digit = 0 
#           key_base = keytext
#           last_digit += 1
#      return '%s%d' % (key_base, last_digit)

# def format_bibtex_entry(bibdict):
#     '''format a single bibtex entry'''
#     if bibdict.has_key('bibtex_key'):
#         key = bibdict['bibtex_key']
#     else:
#         key = autogen_bibtex_key(bibdict)
#     ent = """
# @Misc{%s,
#   author = {%s},
#   title = {%s},
#   howpublished = {%s},
#   month = {%s},
#   year = %s,
#   annote = {%s}}

# """ % (
#         key,
#         bibdict['author'].encode('utf-8'),
#         bibdict['title'].encode('utf-8'),
#         bibdict['howpublished'].encode('utf-8'),
#         bibdict['month'].encode('utf-8'),
#         bibdict['year'].encode('utf-8'),
#         bibdict['annote'].encode('utf-8')
#         )
#     return ent


def prefetch_page_info(notify_window, url):
    '''pre-fetch a page header to assist determing pre/postfix'''
    try:    
        wx.PostEvent(notify_window, pieUpdateEvent('pass', "Reading..."))
        if sys.version_info >= (2,6):
            thepage = urllib2.urlopen(url, data=None, timeout=1) 
        else:
            thepage = urllib2.urlopen(url, data=None) 
        # timeout is 1s, we don't want to hang the UI waiting 
    except ValueError:
        traceback.print_exc()
        wx.PostEvent(notify_window, pieUpdateEvent('warn', "Not a valid or recognised url", updatelast=True))
        return 
    except: 
        wx.PostEvent(notify_window, pieUpdateEvent('warn', "Not a valid or recognised url", updatelast=True))
        traceback.print_exc()
        return 
    thehtml = thepage.read()
    try:
        readup = BeautifulSoup(thehtml)
    except Exception, err:
        traceback.print_exc()
        wx.PostEvent(notify_window, pieUpdateEvent('warn', "Invalid or unparseable HTML", updatelast=True))
        return 
    tag = translate_non_alphanumerics(readup.title.string.split(' - ')[0][:90].strip())
    wx.PostEvent(notify_window, pieUpdateEvent('pass', "Read.", updatelast=True))
    return tag

    

