"""\
Permissions related to a user's username
"""

def is_valid_user(marble):
    if not marble.bag.has_key('ticket'):
        marble.bag.enter('ticket')
    if not marble.bag.environ.get('REMOTE_USER'):
        return 'not_authenticated'
    return True

