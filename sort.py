from pathlib import Path
import globals

def Sort():
    for source in globals.sourceDirectories:
        path = Path(source)
        for file in path.iterdir():
            if not file.is_file(): continue
            if file.suffix not in globals.sortCategories: continue
            isFileMoved = False
            i = 0
            newFile = file
            while not isFileMoved:
                if i != 0:
                    newFile = file.with_name(file.stem + f"({i})" + file.suffix)
                try:
                    file.rename(globals.sortCategories[file.suffix]/newFile.name)
                    isFileMoved = True
                except FileExistsError:
                    i+=1