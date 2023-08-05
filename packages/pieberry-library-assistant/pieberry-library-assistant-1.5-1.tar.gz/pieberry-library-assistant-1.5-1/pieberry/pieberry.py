#!/bin/python

import wx
import sys, os, os.path, time, string, re
import ConfigParser
import traceback
import subprocess

from threading import Thread
from pieberry_config import *
from pieberry_settings import *
from pieberry_exec import *
from pieberry_validators import *
from pieberry_events import *
from pieberry_worker import *
from pieberry_output import *

DEFAULT_SIZE = wx.Size(720, 480) #main window size
TITLE = 'PieBerry Library Assistant'
BUTTON_SIZE = wx.Size(100, 36) #size of main control buttons
smallspace = (10, 10)
tinyspace = (5, 5)
PY2EXE = False

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()

class UiTimer(wx.Timer):
    '''timer class that updates outputList's tooltip'''
    def __init__(self, parent, *args, **kwargs):
        wx.Timer.__init__(self, *args, **kwargs)
        self._last_iteration = time.time()
        self._f = parent
 
    def Notify(self):
        self._last_iteration = time.time()
        self._f.onMouseUpdateList()
        self._f.onPrefetchTag(self._last_iteration)

class pieMainWindow(wx.Frame):
    '''Main window class for PieBerry'''
    _BUTTON_SIZE = wx.Size(100, 50)
    _DEF_WIDTH = (300, -1)

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None, -1, TITLE, size=DEFAULT_SIZE, name=TITLE)       
        self._do_layout()
        self.urlField.SetFocus()
        
        # data tracking
        self.allData = {} # store of data for all bibliography items fetched
        self.lastDataKeys = () # tuple of the last batch of bibliography items (keys)
        self.savedDataKeys = [] # list of items in allData that have been saved already (keys)

        # set up tooltips for outputList
        self.mouseOverList = False
        self.outputList.Bind(wx.EVT_ENTER_WINDOW, self.onMouseEnterList)
        self.outputList.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseExitList)
        self.uitimer = UiTimer(self)
        self.uitimer.Start(1000)
        self.mouse_last_pos = wx.Point(0,0)
        self.url_text_last_changed = time.time()
        self.tipwindow = None # tooltip for bib data
        self.tipwindow_lastpos = (0,0) # last position tipwindow was created
        self.mouseoveritem = -1 # keep track of where the mouse was hovering
        self.suppress_tipwindow = False # flag to keep the tooltip from popping up in inconvenient places
        # Thread comms
        EVT_RESULT(self, self.onResult)
        EVT_PIEUPDATE(self, self.onUpdate)
        EVT_PIEPREFETCH(self, self.onPrefetchResult)
        self.worker = None

        self.Bind(wx.EVT_CLOSE, self.onClose)

        # # DEBUG - SPOOF DATA
        # wx.PostEvent(self, pieUpdateEvent('success', 'Test item', cite="Test data" , href="Test data", data_id=wx.NewId(), updatelast=False))
        # spoofdata = {
        #     'title': 'Spoof title',
        #     'author': 'Spoof author',
        #     'year': '1833',
        #     'month': 'January',
        #     'howpublished': 'Mungdinugn',
        #     'annote': 'notey',
        #     'ancillary_downloadtime': time.localtime(),
        #     'ancillary_creationtime': time.localtime(),
        #     'ancillary_outfilename': 'C:noodles',
        #     'ancillary_locofdoc': 'http://www.hell.no',
        #     'exclude': True,
        #     'internal_author': 'Jon Hoo',
        #     'internal_title': 'Noh Wai'
        #     }
        # spoof_data_id = wx.NewId()
        # spoofbib = {}
        # spoofbib[spoof_data_id] = spoofdata
        # wx.PostEvent(self, pieUpdateEvent('success', 'Success', cite="%s (%s). %s" % (spoofdata['author'], spoofdata['year'], spoofdata['title']), href=spoofdata['ancillary_locofdoc'], data_id=spoof_data_id, updatelast=False))
        # self.allData.update(spoofbib)
        # self.sc_auth = "Spoof author"
        # self.menu_discard.Enable(True)
        # self.menu_savebibs.Enable(True)
        # # // DEBUG //

    def _do_layout(self):
        _icon = wx.EmptyIcon()
        if PY2EXE:
            _icon.CopyFromBitmap(wx.Bitmap('pie_16.png'))
        else:
            _icon.CopyFromBitmap(wx.Bitmap(os.path.join(GetAppdir(), 'pie_16.png')))
        self.SetIcon(_icon)

        rawlist = os.listdir(config.get('PBoptions', 'workingdir'))
        dirlist = [i for i in rawlist if os.path.isdir(os.path.join(config.get('PBoptions', 'workingdir'), i))]
        dirlist.sort()

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        self.menu_savebibs = wx.MenuItem(fileMenu, -1, '&Save Bibliography Changes [%s]\tCtrl-s' % os.path.basename(config.get('PBoptions', 'default_bibliography')), 'Save')
        self.menu_savebibs.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_MENU, (16, 16)))
        self.menu_discard = wx.MenuItem(fileMenu, -1, '&Discard Bibliography Changes', 'Discard')
        self.menu_quit = wx.MenuItem(fileMenu, -1, '&Quit\tCtrl-q', 'Quit')
        self.menu_quit.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU))
        self.menu_config = wx.MenuItem(fileMenu, -1, 'S&ettings', 'Config')
        self.menu_about = wx.MenuItem(fileMenu, -1, '&About', 'About')
        fileMenu.AppendItem(self.menu_savebibs)
        fileMenu.AppendItem(self.menu_discard)
        fileMenu.AppendItem(self.menu_config)
        fileMenu.AppendItem(self.menu_about)
        fileMenu.AppendItem(self.menu_quit)
        menuBar.Append(fileMenu, '&File')
        self.SetMenuBar(menuBar)
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_MENU, self.onSaveBibs, self.menu_savebibs)
        self.Bind(wx.EVT_MENU, self.onClose, self.menu_quit)
        self.Bind(wx.EVT_MENU, self.onConfig, self.menu_config)
        self.Bind(wx.EVT_MENU, self.onAbout, self.menu_about)
        self.Bind(wx.EVT_MENU, self.onDiscard, self.menu_discard)
        self.menu_savebibs.Enable(False)
        self.menu_discard.Enable(False)

        topSizer = wx.BoxSizer(wx.VERTICAL)

        panel0 = wx.Panel(self, -1, style=wx.RAISED_BORDER|wx.EXPAND|wx.TAB_TRAVERSAL)
        panel1 = wx.Panel(self, -1, style=wx.NO_BORDER|wx.EXPAND|wx.TAB_TRAVERSAL)
        

        #Various controls
        # ofvalid = pieUrlValidator()
        self.pasteButton = wx.BitmapButton(panel0, -1, wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (16, 16)), style=wx.NO_BORDER)
        tt7 = wx.ToolTip('Paste from clipboard')
        self.pasteButton.SetToolTip(tt7)
        self.urlField = wx.TextCtrl(panel0, -1, size=self._DEF_WIDTH, validator = pieUrlValidator(), style=wx.TE_PROCESS_ENTER|wx.TE_BESTWRAP)
        self.urlField.ChangeValue('http://')
        self.urlField.SetBackgroundColour("pink")
        tt1 = wx.ToolTip('Website to scan for PDF documents to download.')
        self.urlField.SetToolTip(tt1)
        lburl = wx.StaticText(panel0, -1, 'URL:')

        self.authorField = wx.ComboBox(panel0, -1, size=self._DEF_WIDTH, choices=dirlist, validator=piePlainTextValidator(), style=wx.EXPAND|wx.CB_DROPDOWN)
        tt2 = wx.ToolTip('Generic "author" to use for downloaded documents. This will also be used as a first level subdirectory in which to store these documents.')
        self.authorField.SetToolTip(tt2)

        self.corpAuthorCb = wx.CheckBox(panel0, -1, label="Author is a corporate entity")
        self.corpAuthorCb.SetValue(True)
        tt5 = wx.ToolTip('Treat this author as a corporate entity rather than person(s). This matters to how bibliographies treat these entries.')
        self.corpAuthorCb.SetToolTip(tt5)

        self.tagField = wx.TextCtrl(panel0, -1, size=self._DEF_WIDTH, validator=piePlainTextValidator(), style=wx.EXPAND)
        tt3 = wx.ToolTip('Category tag and second level subdirectory for downloaded documents.')
        self.tagField.SetToolTip(tt3)
        
        pf_use_choices = (
            'Append to title - " ... - Phrase"', 
            'Append to title - " ... (Phrase)"', 
            'Prepend to title - "Phrase: ..."', 
            'Use as subdirectory only')
        self.use_choice_lookup = ('append_hyphen', 'append_brackets', 'prepend', 'dironly')
        self.pfUseChoice = wx.Choice(panel0, -1, choices=pf_use_choices, style=wx.EXPAND)
        tt6 = wx.ToolTip('Select how to use the category phrase. It will always be used to create a subdirectory for the downloaded documents. It may also be appended to the titles of the downloaded documents')
        self.pfUseChoice.SetToolTip(tt6)
        self.pfUseChoice.SetSelection(0)

        self.scanButton = wx.Button(panel0, -1, label='Scan')
        self.outputList = wx.ListCtrl(panel1, -1, style=wx.LC_REPORT|wx.EXPAND)

        self.iList = wx.ImageList(16, 16)
        if PY2EXE: #py2exe has a problem looking elsewhere for files
            self.iList.Add(wx.Bitmap('ic_blueball16.png'))
            self.iList.Add(wx.Bitmap('ic_redsquare16.png'))
            self.iList.Add(wx.Bitmap('ic_yellowex16.png'))
            self.iList.Add(wx.Bitmap('ic_greensquare16.png'))
            self.iList.Add(wx.Bitmap('ic_greentick16.png'))
            self.iList.Add(wx.Bitmap('ic_blueex16.png'))
        else:
            self.iList.Add(wx.Bitmap(os.path.join(GetAppdir(), 'ic_blueball16.png')))
            self.iList.Add(wx.Bitmap(os.path.join(GetAppdir(), 'ic_redsquare16.png')))
            self.iList.Add(wx.Bitmap(os.path.join(GetAppdir(), 'ic_yellowex16.png')))
            self.iList.Add(wx.Bitmap(os.path.join(GetAppdir(), 'ic_greensquare16.png')))
            self.iList.Add(wx.Bitmap(os.path.join(GetAppdir(), 'ic_greentick16.png')))
            self.iList.Add(wx.Bitmap(os.path.join(GetAppdir(), 'ic_blueex16.png')))

        self.listcols = ('', 'Document', 'Link')
        self.widthcols = (150, 380, 300)
        self.msgtypes = {
            'blank': None,
            'success': 0,
            'fail': 1,
            'warn': 2,
            'pass': 3,
            'tick': 4,
            'exclude': 5
            }
        for i in range(len(self.listcols)):
            self.outputList.InsertColumn(i, self.listcols[i])
            self.outputList.SetColumnWidth(i, self.widthcols[i])
        self.outputList.currentItem = -1
        self.outputList.AssignImageList(self.iList, wx.IMAGE_LIST_SMALL)
        
        sizerA = wx.BoxSizer(wx.HORIZONTAL)

        sizer0 = wx.FlexGridSizer(5, 3, 5, 5)
        sizer0.AddGrowableCol(1, 1)
        sizer0.SetFlexibleDirection(wx.BOTH)
        sizer1 = wx.BoxSizer(wx.VERTICAL)


        sizerA.Add(lburl, 1, wx.EXPAND|wx.ALL, 3)
        sizerA.Add(self.pasteButton, 0, wx.ALL, 3)
        sizer0.Add(sizerA, 1, wx.EXPAND)
        sizer0.Add(self.urlField, 1, wx.EXPAND|wx.ALL, 3)
        sizer0.Add(self.scanButton, 1, wx.EXPAND|wx.ALL, 3)
        sizer0.Add(wx.StaticText(panel0, -1, "Default author:"), 1, wx.EXPAND|wx.ALL, 3)
        sizer0.Add(self.authorField, 1, wx.EXPAND|wx.ALL, 3)
        sizer0.Add(self.corpAuthorCb, 1, wx.EXPAND|wx.ALL, 3)
        sizer0.Add(wx.StaticText(panel0, -1, 'Category phrase:'), 1, wx.EXPAND|wx.ALL, 3)
        sizer0.Add(self.tagField, 1, wx.EXPAND|wx.ALL, 3)
        sizer0.Add(self.pfUseChoice, 1, wx.EXPAND|wx.ALL, 3)

        # sizer1.Add(self.outputField, 1, wx.EXPAND)
        sizer1.Add(self.outputList, 2, wx.EXPAND)
        panel0.SetSizer(sizer0)
        panel1.SetSizer(sizer1)
        topSizer.Add(panel0, 0, wx.EXPAND)
        topSizer.Add(panel1, 1, wx.EXPAND)
        self.SetSizer(topSizer)

        self.Layout()

        wx.EVT_LIST_ITEM_RIGHT_CLICK(self.outputList, -1, self.onListRightClick)
        self.list_item_clicked = None
        self.urlField.Bind(wx.EVT_TEXT_ENTER, self.onScan)
        wx.EVT_LIST_ITEM_ACTIVATED(self.outputList, -1, self.onListDoubleClick)
        self.authorField.Bind(wx.EVT_TEXT, self.onAuthorValidate)
        self.tagField.Bind(wx.EVT_TEXT, self.onTagValidate)
        self.scanButton.Bind(wx.EVT_BUTTON, self.onScan)
        # self.urlField.Bind(wx.EVT_KILL_FOCUS, self.onUrlTextChanged)
        self.urlField.Bind(wx.EVT_TEXT, self.onUrlTextChanged)
        self.pasteButton.Bind(wx.EVT_BUTTON, self.onPasteButton)

    def _do_repop_authlist(self):
        #list of candidates for authors - take from subdir names in data directory
        rawlist = os.listdir(config.get('PBoptions', 'workingdir'))
        dirlist = [i for i in rawlist if os.path.isdir(os.path.join(config.get('PBoptions', 'workingdir'), i))]
        dirlist.sort()
        dirlist.reverse()
        self.authorField.Clear()
        for rd in dirlist:
            self.authorField.Insert(rd, 0)

    def outputMsg(self, idx, msgtype, msg='', cite=None, href=None, data_id=None, updatelast=False):
        '''posts a message with appropriate icon to the display 
        types - blank, success, fail, warn, pass'''
        if updatelast: 
            self.outputList.DeleteItem(self.outputList.currentItem)
            thisidx = self.outputList.currentItem
        else: 
            thisidx = idx
        if msgtype == 'blank':
            nexidx = self.outputList.InsertStringItem(thisidx, msg)
        else:
            nexidx = self.outputList.InsertImageStringItem(thisidx, msg, self.msgtypes[msgtype])
        # set reference to store of bibliography data against the item
        if not data_id is None:
            self.outputList.SetItemData(nexidx, data_id)
        if cite:
            self.outputList.SetStringItem(nexidx, 1, cite)
        if href:
            self.outputList.SetStringItem(nexidx, 2, href)
        self.outputList.currentItem = nexidx
        self.outputList.EnsureVisible(nexidx) # scroll to here
        return nexidx

    def onPasteButton(self, evt):
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()
            do = wx.TextDataObject()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                self.urlField.SetValue(do.GetText())

    def onAbout(self, evt):
        info = wx.AboutDialogInfo()
        info.AddDeveloper('Raif Sarcich')
        info.SetVersion('1.5-1')
        info.SetCopyright('(c) 2010 Raif Sarcich et. al.')
        info.SetLicence('''This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.''')
        info.SetDescription('A program to download pdf documents from public websites, and catalogue them in BibTeX format')
        info.SetName('Pieberry (...for your library)')
        _icon = wx.EmptyIcon()
        if PY2EXE:
            _icon.CopyFromBitmap(wx.Bitmap('pie_48.png'))
        else:
            _icon.CopyFromBitmap(wx.Bitmap(os.path.join(GetAppdir(), 'pie_48.png')))
        info.SetIcon(_icon)
        wx.AboutBox(info)

    def onMouseEnterList(self, evt):
        self.mouseOverList = True

    def onMouseExitList(self, evt):
        self.mouseOverList = False
        if self.tipwindow and sys.platform == 'linux2': #irritating non x-platform behaviour 
            self.tipwindow.Destroy()
            self.tipwindow = None

    def onPrefetchTag(self, last_iter):
        if 2 > (last_iter - self.url_text_last_changed) > 1:
            if self.urlField.GetValidator().Validate():
                prefetcher = piePrefetchThread(self, self.urlField.GetValue())
            print 'trigger fetch?'

    def onPrefetchResult(self, evt):
        self.tagField.ChangeValue(evt.tag)
        
    def onMouseUpdateList(self):
        '''work out where the mouse is in the outputList, update
        tooltip accordingly'''
        # three-way switch....
        xy = wx.GetMousePosition()
        mlp = self.mouse_last_pos
        self.mouse_last_pos = xy
        # print xy, mlp, mlp == xy
        # do nothing where we're suppressing tip window
        if self.suppress_tipwindow:
            return
        # do nothing if the mouse isn't over the list
        if not self.mouseOverList:
            return
        ol_xy = self.outputList.ScreenToClient(xy)
        it_idx, flags = self.outputList.HitTest(ol_xy)
        # if there's nothing there, kill any windows
        if it_idx == wx.NOT_FOUND: 
            if self.tipwindow: 
                self.tipwindow.Destroy()
                self.tipwindow = None
            self.mouseoveritem = it_idx
            return
        # if the mouse is static but there's already a tipwindow, keep it
        if mlp == xy and self.tipwindow:
            return
        # if the mouse is moving and there's a tipwindow, kill it
        if mlp != xy and self.tipwindow:
            self.tipwindow.Destroy()
            self.tipwindow = None
            self.mouseoveritem = it_idx
            return
        # if the mouse is static, and there's no tipwindow, create one
        if mlp == xy and not self.tipwindow: 
            self.mouseoveritem = it_idx
            bibidx = self.outputList.GetItemData(it_idx)
            if self.allData.has_key(bibidx) and not (ol_xy == self.tipwindow_lastpos): # if there's data to display...
                bibdata = self.allData[bibidx]
                ttdata = "Author: %s\nTitle: %s\nPublication Date: %s %s\nHow published: %s" % (bibdata['author'], bibdata['title'], bibdata['month'], bibdata['year'], bibdata['howpublished'][:50])
                self.tipwindow = wx.TipWindow(self.outputList, ttdata, maxLength=300)
                self.tipwindow_lastpos = ol_xy
                if sys.platform == 'win32': # tipwindow behaviour is annoyingly non x-platform
                    wx.FutureCall(2000, self.tipwindow.Close)
                    return
            else: # if there's no data associated with this item, do nothing
                if self.tipwindow: self.tipwindow.Destroy()
                self.tipwindow = None
                return

    def onListRightClick(self, evt):
        '''pop up appropriate context menu'''
        self.suppress_tipwindow = True # we don't want tips while we're menu-ing
        if self.tipwindow:
            self.tipwindow.Destroy()
            self.tipwindow = None
        # record what was clicked
        if evt.GetIndex() == -1: return
        self.list_item_clicked = right_click_context = evt.GetIndex()
        ### 2. Launcher creates wxMenu. ###
        menu = wx.Menu()
        it_idx = self.outputList.GetItemData(self.list_item_clicked)
        if self.allData.has_key(it_idx):
            rcm_opendoc = wx.MenuItem(menu, 0, 'Open document')
            rcm_opendoc.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_MENU))
            menu.AppendItem(rcm_opendoc)
            wx.EVT_MENU(menu, 0, self.onMenuOpenDocument)
            rcm_openfol = wx.MenuItem(menu, 1, 'Open document\'s folder')
            rcm_openfol.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_MENU))
            menu.AppendItem(rcm_openfol)
            wx.EVT_MENU(menu, 1, self.onMenuOpenDocumentFolder)
            rcm_deletedoc = wx.MenuItem(menu, 2, 'Delete document from disk')
            rcm_deletedoc.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU))
            menu.AppendItem(rcm_deletedoc)
            wx.EVT_MENU(menu, 2, self.onDelete)
        if self.allData.has_key(it_idx) and not it_idx in self.savedDataKeys:
            menu.Append(3, 'Edit bibliography entry')
            wx.EVT_MENU(menu, 3, self.onMenuEditBibEntry)
            rcm_exclude = wx.MenuItem(menu, 4, 'Exclude from bibliography', kind=wx.ITEM_CHECK)
            menu.AppendItem(rcm_exclude)
            if self.allData[it_idx]['exclude'] == True:
                menu.Check(4, True)
            wx.EVT_MENU(menu, 4, self.onMenuToggleExclude)
        item = self.outputList.GetItem(self.list_item_clicked, 2)
        if len(item.GetText()) > 0:
            rcm_copyurl = wx.MenuItem(menu, 5, 'Copy Web Url to Clipboard')
            rcm_copyurl.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_MENU))
            menu.AppendItem(rcm_copyurl)
            self.Bind(wx.EVT_MENU, self.onMenuCopyUrl, rcm_copyurl)
        # menu.Append(5, 'Debug: item data')
        # wx.EVT_MENU(menu, 5, self.onMenuDebugData)
        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.outputList.PopupMenu( menu, evt.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak
        self.suppress_tipwindow = False

    def onMenuToggleExclude(self, evt):
        data_id = self.outputList.GetItemData(self.list_item_clicked)
        if self.allData[data_id]['exclude'] == True:
            self.allData[data_id]['exclude'] = False
            self.outputList.SetItemImage(self.list_item_clicked, self.msgtypes['success'])
        else:
            self.allData[data_id]['exclude'] = True
            self.outputList.SetItemImage(self.list_item_clicked, self.msgtypes['exclude'])
        

    def onListDoubleClick(self, evt):
        if evt.GetIndex() == -1: return
        self.list_item_clicked = evt.GetIndex()
        self.onMenuOpenDocument(1)

    def onMenuDebugData(self, evt):
        data_id = self.outputList.GetItemData(self.list_item_clicked)
        print 'list_item_clicked = %d' % self.list_item_clicked
        print 'list item data = %d' % data_id
        if self.allData.has_key(data_id):
            print self.allData[data_id]
        else:
            print 'No data associated with this item'

    def onMenuOpenDocument(self, evt):
        data_id = self.outputList.GetItemData(self.list_item_clicked)
        if self.allData.has_key(data_id):
            if sys.platform == 'linux2':
                subprocess.call(('xdg-open', self.allData[data_id]['ancillary_outfilename']))
            elif sys.platform == 'win32':
                os.startfile(self.allData[data_id]['ancillary_outfilename'])

    def onMenuOpenDocumentFolder(self, evt):
        data_id = self.outputList.GetItemData(self.list_item_clicked)
        if sys.platform == 'linux2':
            subprocess.call(('xdg-open', os.path.dirname(self.allData[data_id]['ancillary_outfilename'])))
        elif sys.platform == 'win32':
            os.startfile(os.path.dirname(self.allData[data_id]['ancillary_outfilename']))
        elif sys.platform == 'darwin':
            subprocess.call(('open', os.path.dirname(self.allData[data_id]['ancillary_outfilename'])))

    def onMenuCopyUrl(self, evt):
        '''copy the downloaded file's URL to the clipboard'''
        item = self.outputList.GetItem(self.list_item_clicked, 2)
        clipdata = wx.TextDataObject()
        clipdata.SetText(item.GetText())
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()

    def onMenuEditBibEntry(self, evt):
        idx = self.outputList.GetItemData(self.list_item_clicked)
        if idx in self.savedDataKeys:
            wx.MessageBox("This has already been saved.\nYou can use a bibliography manager like JabRef\n to maintain your library.", "Error")
            return
        if self.allData.has_key(idx):
            self.suppress_tipwindow = True
            dia = pieNewBibEditDialog(self.allData[idx], self)
            res = dia.ShowModal()
            if res == wx.ID_OK:
            #TODO data integrity/validity checking
                self.allData[idx] = dia.getData()
                self.outputList.SetItemText(self.list_item_clicked, 'Updated')
                self.outputList.SetItemImage(self.list_item_clicked, self.msgtypes['pass'])
                self.outputList.SetStringItem(self.list_item_clicked, 1, "%s (%s). %s" % (self.allData[idx]['author'].strip('{} '), self.allData[idx]['year'], self.allData[idx]['title']))
                # self.outputList.SetStringItem(self.list_item_clicked, 2, self.allData['ancillary_outfilename'])
            dia.Destroy()
            self.suppress_tipwindow = False
        else: print 'Tried to edit non-entry entry'

    def onAuthorValidate(self, evt=1):
        self.authorField.GetValidator().Validate()
        self.authorField.Refresh()

    def onTagValidate(self, evt=1):
        self.tagField.GetValidator().Validate()
        self.tagField.Refresh()

    def onUrlTextChanged(self, evt=1):
        self.url_text_last_changed = time.time()
        self.urlField.GetValidator().Validate()
        self.urlField.Refresh() 

    def onClose(self, evt=1):
        '''called when top level window closes'''
        print tuple(self.allData.keys())
        print tuple(self.savedDataKeys)
        if tuple(self.allData.keys()) != tuple(self.savedDataKeys): #check whether we've saved all this to the .bib file before exiting
            dia = wx.MessageDialog(self, 'You have unsaved bibliography data for downloaded files.\nSave these to your master bibliography file before exiting?', 'Unsaved items', style=wx.YES|wx.NO|wx.CANCEL)
            ans = dia.ShowModal()
            if ans == wx.ID_CANCEL: return
            if ans == wx.ID_YES: self.onSaveBibs()
        self.Destroy()

    def onScan(self, evt=1):
        self.sc_url = self.urlField.GetValue().strip()
        self.sc_tag = self.tagField.GetValue().strip()
        self.sc_auth = self.authorField.GetValue().strip()
        self.sc_tagbehav = self.use_choice_lookup[self.pfUseChoice.GetCurrentSelection()]
        self.sc_corpauth = self.corpAuthorCb.IsChecked()
        if not (self.urlField.GetValidator().Validate() and self.authorField.GetValidator().Validate() and self.tagField.GetValidator().Validate()):
            self.outputMsg(sys.maxint, 'warn', 'Invalid Input')
            return
        scrapedata = {
            'url': self.sc_url, 
            'tag': self.sc_tag, 
            'author': self.sc_auth
            }
        scrapecommands = {
            'tag_behaviour': self.sc_tagbehav
            }
        if not self.worker:
            self.scanButton.Disable()
            self.worker = pieWorkerThread(self, scrapedata, scrapecommands)

    def onStop(self, evt):
        if self.worker:
            print "Aborting..."
            self.worker.abort()

    def onSaveBibs(self, evt=1):
        '''Save main bibliography (post-editing)''' 
        print 'savebibs'
        savedata = ''
        saved_item_keys = []
        print self.allData
        try:
            bibwriter = pieBibtexWriter()
            for key, value in self.allData.items():
                if not key in self.savedDataKeys:
                    # ensure author is treated as correct type (corp/person)
                    bibentry = self.allData[key]
                    if not self.allData[key].has_key('corporate_author'):
                        if bibentry['author'] == self.sc_auth:
                            bibentry['corporate_author'] = self.corpAuthorCb.IsChecked()
                        else:
                            bibentry['corporate_author'] = False
                    bibwriter.addEntry(bibentry)
                    print 'adding entry %s' % bibentry['title']
                    saved_item_keys.append(key)
            bibwriter.write()

            # check off saved items in the list view
            for i in range(self.outputList.GetItemCount()):
                idat = self.outputList.GetItemData(i)
                if idat in saved_item_keys: 
                    if self.allData[idat]['exclude'] == False:
                        self.outputList.SetItemImage(i, self.msgtypes['tick'])
                        self.outputList.SetItemText(i, 'Added to bibliography')
                    else:
                        self.outputList.SetItemText(i, 'Not added to bibliography')
                        
            self.savedDataKeys = self.allData.keys()
            self.menu_savebibs.Enable(False)
            self.menu_discard.Enable(False)
            self.SetTitle(TITLE)
        except Exception:
            wx.MessageBox(traceback.format_exc())

    def onDiscard(self, evt=1):
        '''discard data intended for the bibliography'''
        dia = wx.MessageDialog(self, "Do you want to jettison the bibliography information Pieberry has collected?", "Discard bibliography information", style=wx.YES_NO|wx.ICON_QUESTION)
        ans = dia.ShowModal()
        if ans == wx.ID_YES:
            nonsaved_item_keys = []
            for key, value in self.allData.items():
                if not key in self.savedDataKeys:
                    nonsaved_item_keys.append(key)
            for i in range(self.outputList.GetItemCount()):
                idat = self.outputList.GetItemData(i)
                if idat in nonsaved_item_keys:
                    self.outputList.SetItemText(i, 'Not added to bibliography')
            self.savedDataKeys = self.allData.keys()
            self.menu_savebibs.Enable(False)
            self.menu_discard.Enable(False)
            self.SetTitle(TITLE)

    def onDelete(self, evt):
        idx = self.outputList.GetItemData(self.list_item_clicked)
        delfileinfo = self.allData[idx]
        dia = wx.MessageDialog(self, "Delete file %s" % delfileinfo['ancillary_outfilename'], "Delete file", style=wx.YES_NO|wx.ICON_EXCLAMATION)
        ans = dia.ShowModal()
        if ans == wx.ID_YES:
            try:
                os.remove(delfileinfo['ancillary_outfilename'])
                self.outputList.SetItemImage(self.list_item_clicked, self.msgtypes['fail'])
                self.outputList.SetItemText(self.list_item_clicked, 'Deleted')
                self.allData.pop(idx)
            except:
                traceback.print_exc()
                wx.MessageBox('Could not delete file', 'Error')

    def onResult(self, evt):
        if evt.data is None:
            print "Aborted!"
            self.outputMsg(sys.maxint, 'blank', 'Aborted')
        else:
            print 'Downloaded!'
            self.outputMsg(sys.maxint, 'blank', 'Done')
            self.allData.update(evt.data)
            self.lastDataKeys = evt.data.keys()
            savedata = ''
            if len(self.lastDataKeys) > 0: # don't bother if there's nothing new
                writer = pieBibtexWriter()
                for idx in self.lastDataKeys:
                    bibentry = self.allData[idx]
                    if bibentry['author'] == self.sc_auth:
                        bibentry['corporate_author'] = self.corpAuthorCb.IsChecked()
                    writer.addEntry(bibentry)
                writer.setLocation(os.path.join(config.get('PBoptions', 'workingdir'), self.sc_auth, self.sc_tag, '%s_bibliography.bib' % time.strftime('%Y%m%d-%H%M')))
                writer.write()
                self.menu_savebibs.Enable()
                self.menu_discard.Enable()
                self.SetTitle('%s (unsaved)' % TITLE)
        self.worker = None
        self.scanButton.Enable()

    def onUpdate(self, evt):
        print evt.msg
        self.outputMsg(sys.maxint, evt.msgtype, evt.msg, evt.cite, evt.href, evt.data_id, evt.updatelast)

    def onConfig(self, evt):
        self.suppress_tipwindow = True # tip windows get in the way
        cfd = pieNewConfigDialog(config, inipath, self)
        a = cfd.ShowModal()
        if a == wx.ID_OK:
            self._do_repop_authlist()
            self.menu_savebibs.SetItemLabel('&Save Bibliography Data [%s]\tCtrl-s' % os.path.basename(config.get('PBoptions', 'default_bibliography')))
        self.suppress_tipwindow = False

class pieNewConfigDialog(pieConfigDialog):
    def __init__(self, config, configfile, *args, **kwargs):
        pieConfigDialog.__init__(self, *args, **kwargs)
        self._config = config
        self._configfile = configfile
        self.workDirCtrl.SetValue(self._config.get('PBoptions', 'workingdir'))
        self.mainBibCtrl.SetValue(self._config.get('PBoptions', 'default_bibliography'))

    def onOk(self, evt):
        self._config.set('PBoptions', 'workingdir', self.workDirCtrl.GetValue())
        self._config.set('PBoptions', 'default_bibliography', self.mainBibCtrl.GetValue())
        self._config.write(open(self._configfile, 'w'))
        self.EndModal(wx.ID_OK)

    def onCancel(self, evt):
        self.EndModal(wx.ID_CANCEL)

    def onSelectRoot(self, evt):
        fd = wx.DirDialog(self, 'Choose root directory for library', os.getcwd(), style=wx.DD_DIR_MUST_EXIST)
        if fd.ShowModal() == wx.ID_OK:
            newdir = fd.GetPath()
            self.workDirCtrl.SetValue(newdir)
        fd.Close()
        
    def onSelectBib(self, evt):
        dn = os.path.dirname(self.mainBibCtrl.GetValue())
        fd = wx.FileDialog(self, 'Choose principal bibliography file', dn, wildcard="*.bib")
        if fd.ShowModal() == wx.ID_OK:
            newbib = fd.GetPath()
            self.mainBibCtrl.SetValue(newbib)
        fd.Close()
        
class pieNewBibEditDialog(pieBibEditDialog):
    def __init__(self, bibdata, *args, **kwargs):
        pieBibEditDialog.__init__(self, *args, **kwargs)
        self._bibdata = bibdata
        self.keyAutoCb.SetValue(True)
        self.keyCtrl.SetValue(autogen_bibtex_key(bibdata))
        self.keyCtrl.Enable(False)
        self.keyCtrl.Bind(wx.EVT_TEXT, self.onFieldValidate)
        self.keyAutoCb.Bind(wx.EVT_CHECKBOX, self.onKeygenToggle)
        self.authorIsCorporateCb.Set3StateValue(wx.CHK_UNDETERMINED)
        self.authorCtrl.SetValue(bibdata['author'])
        self.authorCtrl.Bind(wx.EVT_TEXT_ENTER, self.onOk)
        self.authorCtrl.Bind(wx.EVT_TEXT, self.onFieldValidate)
        self.authorSwapButton.Bind(wx.EVT_BUTTON, self.onAuthorSwap)
        self.authorAltCtrl.SetValue(bibdata['internal_author'])
        self.titleCtrl.SetValue(bibdata['title'])
        self.titleCtrl.Bind(wx.EVT_TEXT_ENTER, self.onOk)
        self.titleCtrl.Bind(wx.EVT_TEXT, self.onFieldValidate)
        self.titleSwapButton.Bind(wx.EVT_BUTTON, self.onTitleSwap)
        self.titleAltCtrl.SetValue(bibdata['internal_title'])
        self.howpublishedCtrl.SetValue(bibdata['howpublished'])
        self.howpublishedCtrl.Bind(wx.EVT_TEXT_ENTER, self.onOk)
        self.howpublishedCtrl.Bind(wx.EVT_TEXT, self.onFieldValidate)
        self.noteCtrl.Bind(wx.EVT_TEXT, self.onFieldValidate)
        self.annoteCtrl.SetValue(bibdata['annote'])
        self.annoteCtrl.Bind(wx.EVT_TEXT, self.onFieldValidate)
        t = wx.DateTimeFromTimeT(time.mktime(bibdata['ancillary_creationtime']))
        self.datePicker.SetValue(t)
        self.authorCtrl.SetFocus()

    def onKeygenToggle(self, evt):
        if self.keyAutoCb.IsChecked():
            self.keyCtrl.Enable(False)
        else:
            self.keyCtrl.Enable(True)
        
    def onOk(self, evt):
        for ctrl in (self.keyCtrl, self.authorCtrl, self.titleCtrl, self.howpublishedCtrl, self.annoteCtrl):
            if not ctrl.GetValidator().Validate():
                wx.MessageBox("One or more of these fields has problematic syntax for BibTeX - please remedy")
                return
        self._bibdata['author'] = self.authorCtrl.GetValue()
        self._bibdata['title'] = self.titleCtrl.GetValue()
        self._bibdata['howpublished'] = self.howpublishedCtrl.GetValue()
        self._bibdata['annote'] = self.annoteCtrl.GetValue()
        self._bibdata['note'] = self.noteCtrl.GetValue()
        newdate = wxdate2pydate(self.datePicker.GetValue())
        self._bibdata['year'] = unicode(newdate.year)
        self._bibdata['ancillary_creationtime'] = newdate.timetuple()
        self._bibdata['month'] = time.strftime('%B', self._bibdata['ancillary_creationtime'])
        if not self.keyAutoCb.IsChecked():
            self._bibdata['bibtex_key'] = self.keyCtrl.GetValue()
        corpcb = self.authorIsCorporateCb.Get3StateValue()
        if corpcb == wx.CHK_UNCHECKED:
            self._bibdata['corporate_author'] = False
        elif corpcb == wx.CHK_CHECKED:
            self._bibdata['corporate_author'] = True
        self.EndModal(wx.ID_OK)

    def onCancel(self, evt):
        self.EndModal(wx.ID_CANCEL)

    def getData(self):
        return self._bibdata
    
    def onTitleSwap(self, evt):
        t = self.titleCtrl.GetValue()
        self.titleCtrl.SetValue(self.titleAltCtrl.GetValue())
        self.titleAltCtrl.SetValue(t)

    def onAuthorSwap(self, evt):
        t = self.authorCtrl.GetValue()
        self.authorCtrl.SetValue(self.authorAltCtrl.GetValue())
        self.authorAltCtrl.SetValue(t)

    def onFieldValidate(self, evt):
        obj = evt.GetEventObject()
        obj.GetValidator().Validate()

# class RedirectText(object):
#     def __init__(self,aWxTextCtrl):
#         self.out=aWxTextCtrl
#     def write(self,string):
#         self.out.WriteText(string)

def main(argv):
    sys.stdout = open(os.path.join(sysdir, 'stdlog.txt'), 'w')
    sys.stderr = open(os.path.join(sysdir, 'errlog.txt'), 'w')
    app = wx.App(redirect=False)
    w = pieMainWindow()
    w.Show()
    # handle urls passed to pieberry from the command line
    if len(argv) > 1:
        regexp_long = re.compile("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?/*[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]'\\.}>\\),\\\"]")
        if regexp_long.match(argv[1]):
            w.urlField.SetValue(argv[1])
        elif argv[1] in ('-h', '--help', '/?', '/h'):
            usage()
            sys.exit(0)
        else:
            usage()
            dia = wx.MessageDialog(w, 'Argument passed to Pieberry was not a valid URL - Exiting', 'Error', style=wx.OK)
            dia.ShowModal()
            sys.exit(2)

    app.MainLoop()

def usage():
    print """usage: pieberrydm [URL]"""

if __name__ == '__main__':
    main(sys.argv)
