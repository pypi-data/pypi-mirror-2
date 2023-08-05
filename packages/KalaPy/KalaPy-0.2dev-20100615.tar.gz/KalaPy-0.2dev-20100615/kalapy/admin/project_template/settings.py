# Settings for ${name} project

# Name of the project
PROJECT_NAME = "${name}"

# Version of the project
PROJECT_VERSION = "1.0"

# Database backend engine
# Possible value can be either sqlite3, postgresql, bigtable
DATABASE_ENGINE = "sqlite3"

# Database name
# For sqlite3 use path to the sqlite3 database file
# For bigtable keep empty
DATABASE_NAME = "test_${name}.sqlite"

# Database user (must have rights to create database tables)
# Keep empty for sqlite3 and bigtable
DATABASE_USER = ""

# Database password
# Keep empty for sqlite3 and bigtable
DATABASE_PASSWORD = ""

# Database host
# Keep empty for sqlite3 and bigtable
DATABASE_HOST = ""

# Database port
# Keep empty for sqlite3 and bigtable
DATABASE_PORT = ""

# Database specific options
DATABASE_OPTIONS = {
}

# Enable/Disable internationalization support
USE_I18N = True

# Default locale
DEFAULT_LOCALE = 'en_US'

# Default timezone, UTC recommended
DEFAULT_TIMEZONE = 'UTC'

# List of Middleware classes
MIDDLEWARE_CLASSES = (
    'kalapy.contrib.sessions.SessionMiddleware',
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
)

# Application options (subdomain, submount etc).
#
# For example::
#
# PACKAGE_OPTIONS = {
#     'wiki': dict(subdomain='wiki'),
#     'blog': dict(subdomain='blog'),
#     'foo': dict(submount='/foo'),
# }
#
PACKAGE_OPTIONS = {
}

# Deployment server name (e.g. example.com)
SERVERNAME = 'localhost:8080'

