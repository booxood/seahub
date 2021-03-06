"""
Tools for i18n.
"""
from fabric.api import local, task
from fabric.colors import red, green

@task
def push():
    """Update source language, and upload to Transifex.
    """
    local('django-admin.py makemessages -l en -e py,html -i "thirdpart*"')

    # some version of makemessages will produce "%%" in the string, replace that
    # to "%".
    _inplace_change('locale/en/LC_MESSAGES/django.po', '%%', '%')

    local('tx push -s')

@task
def pull():
    """Update local po files with Transifex.
    """
    local('tx pull')

@task(default=True)
def compile():
    """Compile po files.
    """
    local('django-admin.py compilemessages')

########## utility functions
def _inplace_change(filename, old_string, new_string):
    s = open(filename).read()
    if old_string in s:
        print(green('Changing "{old_string}" to "{new_string}" in "{filename}"'.format(**locals())))
        s = s.replace(old_string, new_string)
        f = open(filename, 'w')
        f.write(s)
        f.flush()
        f.close()

def _debug(msg):
    print(red('Running: {msg}'.format(**locals())))
