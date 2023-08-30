import glob
import shutil
from pathlib import Path
from subprocess import run
import sys
import os

PIPENV_ENV = os.environ.copy()
PIPENV_ENV["PIPENV_VERBOSITY"]="-1"

PDF_OUT=Path(__file__).parent.joinpath("out")
PDF_OUT.mkdir(exist_ok=True)

files=glob.glob('**/**/main*.py')
for file in files:
    pybin=Path(sys.orig_argv[0])
    pyscript=Path(file)
    print("pipenv run python",pyscript)
    run(["pipenv","run","python",pyscript.absolute()],env=PIPENV_ENV,cwd=pyscript.parent)
    for pdf in glob.glob("*.pdf",root_dir=pyscript.parent):
        filename="_".join(list(pyscript.parts)[0:2]+[pdf])
        shutil.move(pyscript.parent.joinpath(pdf),PDF_OUT.joinpath(filename))