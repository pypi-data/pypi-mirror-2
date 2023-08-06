from blazeweb.globals import settings, user
from blazeweb.routing import current_url

def after_login_url():
    if settings.components.auth.after_login_url:
        if callable(settings.components.auth.after_login_url):
            return settings.components.auth.after_login_url()
        else:
            return settings.components.auth.after_login_url
    return '/'

def load_session_user(user_obj):
    user.id = user_obj.id
    user.login_id = user_obj.login_id
    user.display_name = user_obj.name_or_login
    user.is_super_user = bool(user_obj.super_user)
    user.reset_required = user_obj.reset_required
    user.is_authenticated = True

    # now permissions
    for row in user_obj.permission_map:
        if row['resulting_approval'] or user_obj.super_user:
            user.add_perm(row['permission_name'])
