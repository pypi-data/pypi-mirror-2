from mercurial.cmdutil import findrepo
from mercurial import hg
from mercurial.ui import ui
import os

def get_repo(path=None):
    if path is None:
        path = os.getcwd()

    repo_root = findrepo(path)
    repo = hg.repository(ui(), path=repo_root)
    return repo

