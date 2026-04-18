import wx
import globals, save, category, sort
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="File Sorter", size=(600,400))
        self.borderSize = 10
        self.categoriesListIndex = 0
        self.sourcesListIndex = 0
        self.Bind(wx.EVT_CLOSE, self.CloseProgram)
        self.mainPanel = wx.Panel(self)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sortButton = wx.Button(self.mainPanel, label="Sort")
        self.sortButton.Bind(wx.EVT_BUTTON, self.BeginSort)
        self.notebook = wx.Notebook(self.mainPanel)
        self.mainSizer.Add(self.notebook, 1, wx.EXPAND)
        self.mainSizer.Add(self.sortButton, 0, wx.EXPAND)
        self.mainPanel.SetSizer(self.mainSizer)
        self.categoryPanel = wx.Panel(self.notebook)
        self.sourcePanel = wx.Panel(self.notebook)
        #Left category panel
        self.leftCategoryPanel = wx.Panel(self.categoryPanel)
        self.leftCategorySizer = wx.BoxSizer(wx.VERTICAL)

        self.addCategoryButton = wx.Button(self.leftCategoryPanel, label="Add") 
        self.removeCategoryButton = wx.Button(self.leftCategoryPanel, label="Remove")
        self.addCategoryButton.Bind(wx.EVT_BUTTON, self.AddCategory)
        self.removeCategoryButton.Bind(wx.EVT_BUTTON, self.RemoveCategory)

        self.categoryNameFieldLabel = wx.StaticText(self.leftCategoryPanel, label="Name")
        self.categoryNameField = wx.TextCtrl(self.leftCategoryPanel)
        self.categoryNameField.Bind(wx.EVT_TEXT, self.CategoryNameFieldChanged)

        self.pathFieldLabel = wx.StaticText(self.leftCategoryPanel, label="Path")
        self.pathField = wx.TextCtrl(self.leftCategoryPanel, style= wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        self.pathField.Disable()
        self.choosePathButton = wx.Button(self.leftCategoryPanel, label="Choose path")
        self.choosePathButton.Bind(wx.EVT_BUTTON, self.ChoosePath)

        self.filetypesFieldLabel = wx.StaticText(self.leftCategoryPanel, label="Filetypes")
        self.filetypesField = wx.TextCtrl(self.leftCategoryPanel, style= wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        self.filetypesField.Bind(wx.EVT_TEXT, self.CategoryFiletypesFieldChanged)

        self.leftCategorySizer.Add(self.addCategoryButton, 0, wx.LEFT | wx.TOP | wx.EXPAND, self.borderSize)
        self.leftCategorySizer.Add(self.removeCategoryButton, 0, wx.LEFT | wx.BOTTOM | wx.EXPAND, self.borderSize)

        self.leftCategorySizer.Add(self.categoryNameFieldLabel, 0, wx.LEFT, self.borderSize)
        self.leftCategorySizer.Add(self.categoryNameField, 0, wx.LEFT | wx.BOTTOM, self.borderSize)
        
        self.leftCategorySizer.Add(self.pathFieldLabel, 0, wx.LEFT, self.borderSize)
        self.leftCategorySizer.Add(self.pathField, 0, wx.LEFT, self.borderSize)
        self.leftCategorySizer.Add(self.choosePathButton, 0, wx.LEFT | wx.BOTTOM, self.borderSize)

        self.leftCategorySizer.Add(self.filetypesFieldLabel, 0, wx.LEFT, self.borderSize)
        self.leftCategorySizer.Add(self.filetypesField, 0, wx.LEFT, self.borderSize)
        self.leftCategoryPanel.SetSizer(self.leftCategorySizer)
        #Right category panel
        self.rightCategoryPanel = wx.Panel(self.categoryPanel)
        self.rightCategorySizer = wx.BoxSizer(wx.VERTICAL)
        self.categoriesList = wx.ListBox(self.rightCategoryPanel)
        self.rightCategorySizer.Add(self.categoriesList, 1, wx.ALL | wx.EXPAND, self.borderSize)
        self.rightCategoryPanel.SetSizer(self.rightCategorySizer)

        self.categoriesList.Bind(wx.EVT_LISTBOX, self.CategorySelected)
        #Category panel
        self.categorySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.categorySizer.Add(self.leftCategoryPanel, 0, wx.EXPAND)
        self.categorySizer.Add(self.rightCategoryPanel, 1, wx.EXPAND)
        self.categoryPanel.SetSizer(self.categorySizer)

        #Left source panel
        self.leftSourcePanel = wx.Panel(self.sourcePanel)
        self.leftSourceSizer = wx.BoxSizer(wx.VERTICAL)

        self.addSourceButton = wx.Button(self.leftSourcePanel, label="Add") 
        self.removeSourceButton = wx.Button(self.leftSourcePanel, label="Remove")
        self.addSourceButton.Bind(wx.EVT_BUTTON, self.AddSource)
        self.removeSourceButton.Bind(wx.EVT_BUTTON, self.RemoveSource)

        self.leftSourceSizer.Add(self.addSourceButton, 0, wx.LEFT | wx.TOP | wx.EXPAND, self.borderSize)
        self.leftSourceSizer.Add(self.removeSourceButton, 0, wx.LEFT | wx.EXPAND, self.borderSize)
        self.leftSourcePanel.SetSizer(self.leftSourceSizer)
        #Right source panel
        self.rightSourcePanel = wx.Panel(self.sourcePanel)
        self.rightSourceSizer = wx.BoxSizer(wx.VERTICAL)
        self.sourcesList = wx.ListBox(self.rightSourcePanel)
        self.sourcesList.Bind(wx.EVT_LISTBOX, self.SourceSelected)
        self.rightSourceSizer.Add(self.sourcesList, 1, wx.ALL | wx.EXPAND, self.borderSize)
        self.rightSourcePanel.SetSizer(self.rightSourceSizer)
        #Source panel
        self.sourceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sourceSizer.Add(self.leftSourcePanel, 0, wx.EXPAND)
        self.sourceSizer.Add(self.rightSourcePanel, 1, wx.EXPAND)
        self.sourcePanel.SetSizer(self.sourceSizer)
        #Add tabs
        self.notebook.AddPage(self.categoryPanel, "Categories")
        self.notebook.AddPage(self.sourcePanel, "Source")
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.NotebookChanged)

        self.UpdateCategories()
        self.UpdateSources()
        self.DisableEdits()
    
    def AddCategory(self, event):
        globals.categories.append(category.Category("New category", "."))
        self.EnableEdits()
        self.UpdateCategories()
    
    def RemoveCategory(self, event):
        globals.categories.pop(self.categoriesListIndex).name
        self.DisableEdits()
        self.UpdateCategories()

    def ChoosePath(self, event):
        dialog = wx.DirDialog(None, "Choose destination directory", style= wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dialog.ShowModal()
        path = dialog.GetPath()
        if path == "":
            return
        globals.categories[self.categoriesListIndex].SetPath(path)
        self.pathField.ChangeValue(path)
        self.UpdateCategories()

    def CategoryNameFieldChanged(self, event):
        globals.categories[self.categoriesListIndex].name = self.categoryNameField.Value
        self.UpdateCategories()

    def CategoryFiletypesFieldChanged(self, event):
        filetypes = []
        for filetype in self.filetypesField.GetValue().split():
            filetypes.append(filetype)
        globals.categories[self.categoriesListIndex].filetypes[:] = filetypes
        self.UpdateCategories()

    def CategorySelected(self, event):
        self.categoriesListIndex = self.categoriesList.GetSelection()
        category = globals.categories[self.categoriesListIndex]
        self.categoryNameField.ChangeValue(category.name)
        self.pathField.ChangeValue(str(category.path))
        self.filetypesField.ChangeValue(" ".join(category.filetypes))
        self.EnableEdits()

    def UpdateCategories(self):
        self.categoriesList.Clear()
        for category in globals.categories:
            self.categoriesList.Insert(category.name,self.categoriesList.GetCount())

    def DisableEdits(self):
        self.filetypesField.Disable()
        self.categoryNameField.Disable()
        self.choosePathButton.Disable()
        self.removeCategoryButton.Disable()
        self.removeSourceButton.Disable()

    def EnableEdits(self):
        self.filetypesField.Enable()
        self.categoryNameField.Enable()
        self.choosePathButton.Enable()
        self.removeCategoryButton.Enable()
        self.removeSourceButton.Enable()
    
    def UpdateSources(self):
        self.sourcesList.Clear()
        for source in globals.sourceDirectories:
            self.sourcesList.Insert(source, self.sourcesList.GetCount())
    def AddSource(self, event):
        dialog = wx.DirDialog(None, "Choose source directory", style= wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dialog.ShowModal()
        path = dialog.GetPath()
        if path == "":
            return
        globals.sourceDirectories.append(path)
        self.UpdateSources()
    def RemoveSource(self, event):
        globals.sourceDirectories.pop(self.sourcesListIndex)
        self.DisableEdits()
        self.UpdateSources()

    def SourceSelected(self, event):
        self.sourcesListIndex = self.sourcesList.GetSelection()
        self.EnableEdits()

    def NotebookChanged(self, event):
        self.categoriesListIndex = 0
        self.sourcesListIndex = 0

    def BeginSort(self, event):
        category.MapCategories()
        sort.Sort()
    def CloseProgram(self, event):
        save.SaveCategories()
        save.SaveSources()
        event.Skip()