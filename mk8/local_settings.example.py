"""
Django local settings for mk8 project.
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'some key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SERVE_MEDIA = False

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

from django_auth_ldap.config import LDAPSearch
import ldap
AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"
AUTH_LDAP_BIND_DN = "CN=user,DC=example,DC=com"
AUTH_LDAP_BIND_PASSWORD = "password"
AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=example,DC=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

