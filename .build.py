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

GLOBFILE=sys.argv[1] if len(sys.argv)>1 else "**/**/main*.py"
OUTPATH=Path(r"\\wsl.localhost\Ubuntu-22.04\home\xsr\repo\nlct\simu")

files=glob.glob(GLOBFILE)
for file in files:
    pybin=Path(sys.orig_argv[0])
    pyscript=Path(file)
    print("pipenv run python",pyscript)
    run(["pipenv","run","python",pyscript.absolute()],env=PIPENV_ENV,cwd=pyscript.parent)
    for pdf in glob.glob("*.pdf",root_dir=pyscript.parent):
        filename="_".join(list(pyscript.parts)[0:2]+[pdf])
        shutil.copy(pyscript.parent.joinpath(pdf),OUTPATH.joinpath(filename))
        shutil.move(pyscript.parent.joinpath(pdf),PDF_OUT.joinpath(filename))