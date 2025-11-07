from .objects import append_file, flag, merge_file, pull_file, epython, event
from .objects.filetype import fileType
import os

def clean_suffix(path):
    return str(path).replace("\\","/").replace("//","/").removesuffix("/").removesuffix("/").removeprefix("/").removeprefix("/").strip()

def endswith(path: str, suffix: str):
    return path.endswith(suffix) or path.endswith(suffix+"_temp")

def get(path: str):
    if endswith(path, ".pull"):
        return pull_file.Pulled(path)
    elif endswith(path, ".merge"):
        return merge_file.Merged(path)
    elif endswith(path, ".append"):
        return append_file.Appended(path)
    elif endswith(path, ".flag.tga"):
        return flag.Flag(path)
    elif endswith(path, ".event"):
        return event.Event(path)
    #elif endswith(path, ".focus.dds"):
    #    return focus_icon.FocusIcon(path)
    elif endswith(path, ".epy"):
        return epython.ePython(path)
    else:
        return fileType(path)
    
def order():
    return [
        pull_file.Pulled,
        merge_file.Merged,
        append_file.Appended,
        flag.Flag,
        event.Event,
        #focus_icon.FocusIcon,
        epython.ePython,
        fileType
    ]

def should_run(path: str):
    file = get(path)
    if type(file) == fileType:
        return False
    
    head, tail = os.path.split(path)
    
    if len(file.required_dir()) > 0: #Directory Requirements (Ex: must be in /countries/)
        cont = False
        for d in file.required_dir():
            if clean_suffix(head).endswith(clean_suffix(d)):
                cont = True
                break
        if not cont:
            file.required_dir_error()
            return False
        
    if len(file.blocked_dir()) > 0: #Blocked Directories (Ex: must not be in /history/countries/)
        for d in file.blocked_dir():
            if clean_suffix(head).endswith(clean_suffix(d)):
                file.blocked_dir_error()
                return False

    return True