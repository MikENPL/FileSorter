from pathlib import Path
import wx
import globals, save, category, gui

if __name__ == "__main__":
    save.ReadCategories()
    save.ReadSources()
    app = wx.App()
    frame = gui.MyFrame()
    frame.Show()
    app.MainLoop()