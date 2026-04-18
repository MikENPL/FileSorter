from pathlib import Path
import globals
class Category:
    def __init__(self, name, path, filetypes = None):
        self.name = name
        self.path = Path(path)
        self.filetypes = filetypes or []
    def AddFiletype(self, newFiletype):
        self.filetypes.append(newFiletype)
    def RemoveFiletype(self, targetFiletype):
        self.filetypes.remove(targetFiletype)
    def SetPath(self, newPath):
        self.path = Path(newPath)
    def MapFiletypes(self):
        output = {}
        for filetype in self.filetypes:
            output[filetype] = self.path
        return output
def AddCategory(newCategory):
    globals.categories.append(newCategory)
def RemoveCategory(targetCategory):
    globals.categories.remove(targetCategory)
def MapCategories():
    for category in globals.categories:
       globals.sortCategories.update(category.MapFiletypes())