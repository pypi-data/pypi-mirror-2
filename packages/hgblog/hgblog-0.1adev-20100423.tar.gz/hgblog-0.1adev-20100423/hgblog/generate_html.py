from mercurial.match import match
from sphinx.cmdline import main as sphinxify

def htmlize_articles(ui, repo, **kwargs):
    """Calls on Sphinx to turn our .rst files into pretty HTML"""

    # find all .rst files that Mercurial is currently tracking
    m = match(repo.root, repo.getcwd(), ('*.rst',), default='relglob')
    files_to_consider = repo[None].walk(m)

    # tell Sphinx to HTML-ize the .rst files we found
    args = [
        '-bdirhtml',
        '-dbuild/doctrees',
        'source',
        'build/html',
    ] + files_to_consider
    sphinxify(args)

