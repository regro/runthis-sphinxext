$PROJECT = $GITHUB_REPO = 'runthis-server'
$GITHUB_ORG = 'regro'

$ACTIVITIES = [
    'authors',
    'version_bump',
    'changelog',
    'tag',
    'push_tag',
    'ghrelease',
    'pypi',
    #'conda_forge',
]

$AUTHORS_FILENAME = 'AUTHORS.md'
$VERSION_BUMP_PATTERNS = [
    ('runthis/server/__init__.py', r'__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', r'version\s*=.*,', "version='$VERSION',")
]
$CHANGELOG_FILENAME = 'CHANGELOG.md'
$CHANGELOG_TEMPLATE = 'TEMPLATE.md'
$CHANGELOG_PATTERN = "<!-- current developments -->"
$CHANGELOG_HEADER = """
<!-- current developments -->

## v$VERSION
"""
$PYPI_SIGN = False
