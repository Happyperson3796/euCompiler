from .filetype import fileType
from ..pdxscript import get, format, Pair, Collection, Jom
from .pull_file import Pulled
import os

class Merged(fileType):
    def execute(data: Jom, base_file: str, subpath: str, reverse: bool):
        subpath = subpath.removeprefix("/").removesuffix("/").split("/")

        if not os.path.exists(base_file): #Create if not found
            with open(base_file, "w", encoding="utf-8-sig") as file:
                t = ""
                for x in subpath:
                    t += x+"={"
                for x in subpath:
                    t += "}"
                file.write(t)

        with open(base_file, "r", encoding="utf-8-sig") as file:
            base = get(file.read())
            subbase = base.get(subpath[0])
            for p in subpath[1:]:
                subbase = subbase.get(p)

        suboverride = data[-1].get(subpath[0])
        for p in subpath[1:]:
            suboverride = suboverride.get(p)

        subbase.merge(suboverride, reverse)

        with open(base_file, "w", encoding="utf-8-sig") as file:
            file.write(format(base))

    def run(self):
        head, tail = os.path.split(self.path)

        with open(self.path, "r", encoding="utf-8-sig") as file:
            raw = get(file.read())

        for data in raw:
            base_file = data.key_data().unquote().strip()
            subpath = data.value().get("path").unquote().strip()
            reverse = data.value().get("reverse", "no").bool()
            pull = data.value().get("pull", "").unquote().strip()

            if pull != "": Pulled.execute(head, pull+"/"+base_file, base_file)

            Merged.execute(data, head+"/"+base_file, subpath, reverse)
            


    def clean(self):
        head, tail = os.path.split(self.path)

        with open(self.path, "r", encoding="utf-8-sig") as file: #TODO: Proper data removal, not just file deletion.
            raw = get(file.read())

        for data in raw:
            base_file = data.key_data().unquote().strip()

            try:
                os.remove(head+"/"+base_file)
            except: pass
