# Settings common to all environments (development|staging|production)

# Application settings
APP_NAME = "MSState Library ETD System"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username

# Password hashing settings
USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ['argon2']  # argon2 for password hashing
# I would suggest settings these to the maximum that you can.
USER_PASSLIB_CRYPTCONTEXT_KEYWORDS = dict(argon2__rounds=5, argon2__memory_cost=8192, argon2__max_threads=-1)
# rounds - This corresponds linearly to the amount of time hashing will take.
# memory_cost - Defines the memory usage in kibibytes. This corresponds linearly to the amount of memory hashing will take.
# max_threads - Maximum number of threads that will be used. -1 means unlimited; otherwise hashing will use `min(parallelism, max_threads)` threads.

# Flask-User routing settings
USER_AFTER_LOGIN_ENDPOINT = "main.index"
USER_AFTER_LOGOUT_ENDPOINT = "main.signed_out"
USER_AFTER_EDIT_USER_PROFILE_ENDPOINT = 'main.profile'
