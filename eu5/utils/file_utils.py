from ..pdxscript import get, format, Pair, Collection, Jom
import os

class Locfile():
    def __init__(self, filename: str, lang: str = "english"):
        self.lang = lang

        if ".yml" not in filename: filename += "_l_"+self.lang+".yml"
        filepath = ""+filename

        self.filepath = filepath

    def add(self, key: str, val: str):
        loc = "\n "+key+": \""+val+"\""

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8-sig") as file:
                file.write("l_"+self.lang+":")
        else:
            with open(self.filepath, "r", encoding="utf-8-sig") as file:
                lines = file.read()
                for x in lines.split("\n"):
                    if x.strip() == loc.strip(): return
        
        with open(self.filepath, "a", encoding="utf-8-sig") as file:
            file.write(loc)

    def remove(self, key: str, val: str):
        loc = "\n "+key+": \""+val+"\""

        if not os.path.exists(self.filepath):
            return
        else:
            with open(self.filepath, "r", encoding="utf-8-sig") as file:
                lines = file.read()

            with open(self.filepath, "w", encoding="utf-8-sig") as file:
                text = []
                for x in lines.split("\n"):
                    if x.strip() != loc.strip():
                        text.append(x)
                file.write("\n".join(text))

class Jomfile():
    def __init__(self, filename: str):
        self.filepath = filepath

    def add(self, data: Jom):

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8-sig") as file:
                file.write(data.format())
        else:
            with open(self.filepath, "r", encoding="utf-8-sig") as file:
                lines = file.read()
                for x in lines.split("\n"):
                    if x.strip() == loc.strip(): return
        
        with open(self.filepath, "a", encoding="utf-8-sig") as file:
            file.write(loc)

    def remove(self, key: str, val: str):
        loc = "\n "+key+": \""+val+"\""

        if not os.path.exists(self.filepath):
            return
        else:
            with open(self.filepath, "r", encoding="utf-8-sig") as file:
                lines = file.read()

            with open(self.filepath, "w", encoding="utf-8-sig") as file:
                text = []
                for x in lines.split("\n"):
                    if x.strip() != loc.strip():
                        text.append(x)
                file.write("\n".join(text))