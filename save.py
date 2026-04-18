import csv
from category import Category
import globals

def SaveCategories():
    with open("categories.csv", "w", newline="") as file:
        writer = csv.writer(file)
        data = []
        for category in globals.categories:
            data.append([category.name, category.path, " ".join(category.filetypes)])
        writer.writerows(data)
def ReadCategories():
    with open("categories.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            readCategory = Category(row[0],row[1])
            for filetype in row[2].split():
                readCategory.AddFiletype(filetype)
            globals.categories.append(readCategory)
def SaveSources():
    with open("sources.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows([[source] for source in globals.sourceDirectories])
            
def ReadSources():
     with open("sources.csv", "a+", newline="") as file:
        file.seek(0)
        reader = csv.reader(file)
        globals.sourceDirectories[:] = [row[0] for row in reader]