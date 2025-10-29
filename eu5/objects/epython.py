from .filetype import fileType
import os
import json
import subprocess
import sys

python_allowed = False

def run_function(filepath, func_name, *args):
    file_dir = os.path.dirname(os.path.abspath(filepath))
    args_json = json.dumps(args)

    code = f"""
import json
ns = {{}}
exec(open(r'{filepath}').read(), ns)
result = ns['{func_name}'](*json.loads(r'''{args_json}'''))
print(json.dumps(result))
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=file_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return json.loads(result.stdout.strip())

class ePython(fileType):
    def run(self):
        if not python_allowed:
            print("\nPython execution is disabled! Set run_unsafe to true in the build config.")
            return
        
        run_function(self.path, "run")

    def clean(self):
        if not python_allowed:
            print("\nPython execution is disabled! Set run_unsafe to true in the build config.")
            return

        run_function(self.path, "clean")
