from ..pdxscript import get, format, Pair, Collection
from ..objects import filetype
import os

def entry_key_gfx(self: filetype, data: Collection, path: str):
    head, tail = os.path.split(self.path)
    for p in data.entries():
        key = p.key()
        if os.path.exists(head+"/"+key+".dds"):
            os.makedirs(path, exist_ok=True)
            try: os.remove(path+key+".dds")
            except: pass
            os.rename(head+"/"+key+".dds", path+key+".dds")
