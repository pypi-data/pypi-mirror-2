'''
__changelog__ -- contains the project changelog in object form.
'''

from bwversion import Version, ChangeLog

CHANGELOG = ChangeLog(
    Version('0.1', 'Initial pre-release at PyOhio'),
    Version('0.2.5',
        'Added throwables',
        'Added changelog file',
        'Modified version to be more shell friendly',
        'Made __version__ more pydoc compatible',
        ),
    Version('0.2.6',
        'Added throw() and catch() as simple functions',
        ),
    Version('0.3',
        'Added type conversion support for members',
        'Added default and built values for members',
        'Added required members',
        'Added TC global',
        )
)

if __name__ == '__main__':
    print CHANGELOG

