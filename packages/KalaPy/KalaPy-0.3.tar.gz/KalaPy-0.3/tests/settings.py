# Settings for tests project

# Name of the project
PROJECT_NAME = "tests"

# Version of the project
PROJECT_VERSION = "1.0"

# Database backend engine
# Possible value can be either sqlite3, postgresql, gae
DATABASE_ENGINE = "postgresql"

# Database name
# For sqlite3 use path to the sqlite3 database file
# For gae keep empty
DATABASE_NAME = "test_kalapy"

# Database user (must have rights to create database tables)
# Keep empty for sqlite3 and gae
DATABASE_USER = ""

# Database password
# Keep empty for sqlite3 and gae
DATABASE_PASSWORD = ""

# Database host
# Keep empty for sqlite3 and gae
DATABASE_HOST = ""

# Database port
# Keep empty for sqlite3 and gae
DATABASE_PORT = ""

# Database specific options
DATABASE_OPTIONS = {
}

# Enable/Disable internationalization support
USE_I18N = True

# List of Middleware classes
MIDDLEWARE_CLASSES = (
    'kalapy.contrib.sessions.SessionMiddleware',
    'core.middleware.TestMiddleware',
)

# Session storage engine (memory, memcached or database)
SESSION_ENGINE = "memory"

# Session cookie options
SESSION_COOKIE = {
    'name': 'session_id',
    'age': 60 * 60 * 24 * 7 * 2,
    'domain': None,
    'path': '/'
}

# List of installed packages
INSTALLED_PACKAGES = (
    'kalapy.contrib.sessions',
    'core',
    'foo',
    'bar',
)

# Package options (submount etc).
#
# For example::
#
# PACKAGE_OPTIONS = {
#     'wiki': {'submount': '/wiki'},
#     'blog': {'submount': '/blog'},
# }
#
PACKAGE_OPTIONS = {
    'foo': {'submount': '/foo'},
    'bar': {'submount': '/bar'},
}

