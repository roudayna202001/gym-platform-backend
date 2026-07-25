from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(*roles):
    """Décorateur : restreint une vue à une ou plusieurs valeurs de `role`."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator
