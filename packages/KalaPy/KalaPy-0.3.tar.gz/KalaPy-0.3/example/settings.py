# Settings for example project

# Name of the project
PROJECT_NAME = "example"

# Version of the project
PROJECT_VERSION = "1.0"

# Database backend engine
# Possible value can be either sqlite3, postgresql, mysql, gae
DATABASE_ENGINE = "sqlite3"

# Database name
# For sqlite3 use path to the sqlite3 database file
# For gae keep empty
DATABASE_NAME = "example.db"

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
)

# Session storage engine (memory, memcached or database)
SESSION_ENGINE = "memory"

# Session related options, for example memcached servers.
#
# For memcached engine, provide list of memcached servers.
# If DATABASE_ENGINE is set to 'gae' this option will be ignored.
SESSION_OPTIONS = {
    'memcached_servers': [],
}

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
    'main',
    'wiki',
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
    'wiki': {'submount': '/wiki'},
}

