#!/usr/bin/env python
"""Print a string suitable for use as a Django `SECRET_KEY` setting."""

import random


SECRET_KEY_LENGTH = 50
SECRET_KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


def secret_key():
    """Return a string of random characters suited to a Django `SECRET_KEY`."""
    return ''.join(
        [random.SystemRandom().choice(SECRET_KEY_CHARS)
         for _ in range(SECRET_KEY_LENGTH)])


if __name__ == "__main__":
    print(secret_key()),
