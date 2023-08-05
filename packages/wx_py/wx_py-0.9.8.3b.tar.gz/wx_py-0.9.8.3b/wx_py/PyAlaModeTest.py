#!/usr/bin/env python
"""PyAlaModeTest is a programmer's editor."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: PyAlaModeTest.py 26212 2004-03-15 13:42:37Z PKO $"
__revision__ = "$Revision: 26212 $"[11:-2]

import wx
import wx_py as py

import os
import sys

class App(wx.App):
    """PyAlaModeTest standalone application."""

    def __init__(self, filename=None):
        self.filename = filename
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        wx.InitAllImageHandlers()
        self.frame = py.editor.EditorShellNotebookFrame(filename=self.filename)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main(filename=None):
    app = App(filename)
    app.MainLoop()

if __name__ == '__main__':
    filename = None
    if len(sys.argv) > 1:
        filename = os.path.realpath(sys.argv[1])
    main(filename)
