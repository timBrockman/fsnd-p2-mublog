"""some basic validation checks"""

import re

# signup CONSTANTS
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{8,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

# blog entry CONSTANTS
TITLE_RE = re.compile(r"^[ a-zA-Z0-9_-]{3,20}$")

