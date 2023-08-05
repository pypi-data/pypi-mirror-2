import os

def refresh(repo=None):
    """Calls on Sphinx to turn our .rst files into pretty HTML"""

    from mercurial.match import match
    from mercurial.ui import ui
    from sphinx.cmdline import main as sphinxify
    from hgblog.utils import get_repo

    if repo is None:
        repo = get_repo()

    # find all .rst files that Mercurial is currently tracking
    m = match(repo.root, repo.getcwd(), ('*.rst',))
    files_to_consider = repo[None].walk(m)

    # tell Sphinx to HTML-ize the .rst files we found
    args = [
        '-bdirhtml',
        '-d%s' % os.path.join(repo.root, 'build', 'doctrees'),
        os.path.join(repo.root, 'source'),
        os.path.join(repo.root, 'build', 'html'),
    ] + files_to_consider
    sphinxify(args)

