#!/usr/bin/env python
"""PyAlaCarte is a simple programmer's editor."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: PyAlaCarte.py 26212 2004-03-15 13:42:37Z PKO $"
__revision__ = "$Revision: 26212 $"[11:-2]

import wx
import wx_py as py

import os
import sys

class App(wx.App):
    """PyAlaCarte standalone application."""

    def __init__(self, filename=None):
        self.filename = filename
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        wx.InitAllImageHandlers()
        self.frame = py.editor.EditorFrame(filename=self.filename)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main(filename=None):
    if not filename and len(sys.argv) > 1:
        filename = sys.argv[1]
    if filename:
        filename = os.path.realpath(filename)
    app = App(filename)
    app.MainLoop()

if __name__ == '__main__':
    main()
