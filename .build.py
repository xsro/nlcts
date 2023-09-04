import glob
import shutil
from pathlib import Path
from subprocess import run
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='script to run all simulation and save figures')
parser.add_argument("--glob",type=str,default="**/**/*.py",help="glob pattern to find main.py")
parser.add_argument("--outpath",type=str,default=r"\\wsl.localhost\Ubuntu-22.04\home\xsr\repo\nlct\simu",help="path to copy all figures to")
parser.add_argument("--no-copy",action="store_true",help="do not copy figures to outpath")
parser.add_argument("--no-run",action="store_true",help="do not run simulation")
args = parser.parse_args()

#获得传入的参数
print(args)

PIPENV_ENV = os.environ.copy()
PIPENV_ENV["PIPENV_VERBOSITY"]="-1"

PDF_OUT=Path(__file__).parent.joinpath("out")
PDF_OUT.mkdir(exist_ok=True)

GLOBFILE=args.glob
OUTPATH=Path(args.outpath)

files=glob.glob(GLOBFILE)
for file in files:
    pybin=Path(sys.orig_argv[0])
    pyscript=Path(file)
    if args.no_run:
        print("skip",pyscript)
        continue
    else:
        print("pipenv run python",pyscript)
        run(["pipenv","run","python",pyscript.absolute()],env=PIPENV_ENV,cwd=pyscript.parent)
    for pdf in glob.glob("*.pdf",root_dir=pyscript.parent):
        filename="_".join(list(pyscript.parts)[0:2]+[pdf])
        if not args.no_copy:
            print("\tcopying",pdf)
            shutil.copy(pyscript.parent.joinpath(pdf),OUTPATH.joinpath(filename))
            shutil.copy(pyscript.parent.joinpath(pdf),PDF_OUT.joinpath(filename))