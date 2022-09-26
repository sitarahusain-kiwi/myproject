"""
Constants used in application
"""
API_TITLE = 'Myproject API Document'
API_VERSION = 'v1'
API_DESCRIPTION = 'Test API for Authentication and Subscription'
API_VERSION_URL = 'api/' + API_VERSION + '/'

REGEX_VALID = {
    "password": "^[A-Za-z0-9~'`!@#$%^&*()_+,.-]*$",
    "email": '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
}

NUMBER = {
    'one': 1,
    'two': 2
}
# Define Email From address & Text
EMAIL_FROM_ADDRESS = "rockstar.backend@gmail.com"
EMAIL_FROM_TEXT = "Python <" + EMAIL_FROM_ADDRESS + ">"
