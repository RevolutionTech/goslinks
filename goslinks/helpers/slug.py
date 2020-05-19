import re

CLEANED_SLUG_INVALID_CHAR_RE = re.compile(r"[^a-z0-9]")


def clean_to_slug(dirty_slug):
    return re.sub(CLEANED_SLUG_INVALID_CHAR_RE, "", dirty_slug.lower())
