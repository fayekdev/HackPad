import subprocess 
import os
from pathlib import Path


class ProgramAction:

    def execute(self, action):

        if "data" in action:
            path = action["data"].get("path", "")
            args = action["data"].get("args", "")
        else:
            path = action.get("path", "")
            args = action.get("args", "")

        if not path:
            return

        path = os.path.expandvars(path)
        path = os.path.expanduser(path)

        try:
            if args:

                subprocess.Popen(
                    [path] + args.split(),
                    shell=False
                )
            else:

                if Path(path).is_dir():
                    os.startfile(path)

                elif Path(path).exists():
                    os.startfile(path)

                else:
                    subprocess.Popen(
                        path, 
                        shell=True
                    )
        except Exception as e:
            print("ProgramAction Error:", e)