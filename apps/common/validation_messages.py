"""
Validation messages used in project
"""
CHAR_LIMIT_SIZE = {
    'first_name_max': 50,
    'last_name_max': 50,
    'max_username': 50,
    'min_username': 6,
    'pass_min': 6,
    'pass_max': 15,
}

VALIDATION = {
    'first_name': {
        "blank": "FIRST_NAME_BLANK",
        "invalid": "FIRST_NAME_INVALID",
        "min_length": "FIRST_NAME_MIN_LENGTH",
        "max_length": "FIRST_NAME_MAX_LENGTH",
        "required": "FIRST_NAME_REQUIRED"
    },
    'last_name': {
        "blank": "LAST_NAME_BLANK",
        "invalid": "LAST_NAME_INVALID",
        "min_length": "LAST_NAME_MIN_LENGTH",
        "max_length": "LAST_NAME_MAX_LENGTH",
        "required": "LAST_NAME_REQUIRED"
    },
    'username': {
        "blank": "USERNAME_BLANK",
        "invalid": "USERNAME_INVALID",
        "min_length": "USERNAME_MIN_LENGTH",
        "max_length": "USERNAME_MAX_LENGTH",
        "required": "USERNAME_REQUIRED"
    },
    'email': {
        "blank": "EMAIL_BLANK",
        "invalid": "EMAIL_INVALID",
        "min_length": "EMAIL_MIN_LENGTH",
        "max_length": "EMAIL_MAX_LENGTH",
        "required": "EMAIL_REQUIRED"
    },
    'password': {
        "blank": "PASSWORD_BLANK",
        "min_length": "PASSWORD_MAX_LENGTH",
        "max_length": "PASSWORD_MAX_LENGTH",
        "pattern": "PASSWORD_PATTERN",
        "required": "PASSWORD_REQUIRED"
    },
    'email_verification_otp': {
        "blank": "VERIFICATION_OTP_BLANK",
        "min_length": "VERIFICATION_OTP_MIN_LENGTH",
        "max_length": "VERIFICATION_OTP_MAX_LENGTH",
        "required": "VERIFICATION_OTP_REQUIRED"
    },
}

ERROR_MESSAGE = {
    'email': {
        'exists': 'EMAIL_ALREADY_EXISTS',
        'invalid': 'EMAIL_INVALID',
        'not_verified': 'EMAIL_NOT_VERIFIED',
    },
    'password': {
        'invalid': 'INVALID_PASSWORD',
    },
    'user': {
        'inactive': 'ACCOUNT_DEACTIVATED'
    },
    'verification_otp': {
        'invalid': 'EMAIL_VERIFICATION_OTP_INVALID',
        'verified': 'EMAIL_ALREADY_VERIFIED'
    }
}
