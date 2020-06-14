import os

ZAPPA_COMMANDS_REQUIRE_LIB_FILES = ("deploy", "package", "update")
SO_FILENAMES = [
    "_cffi_backend.cpython-38-x86_64-linux-gnu.so",
    ".libs_cffi_backend",
]
PROJECT_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(PROJECT_DIR, "lib")


def activate_shared_object(filename):
    """
    Move the shared object file to the top-level
    """
    os.rename(os.path.join(LIB_DIR, filename), os.path.join(PROJECT_DIR, filename))


def deactivate_shared_object(filename):
    """
    Move the shared object file back to lib/
    """
    os.rename(os.path.join(PROJECT_DIR, filename), os.path.join(LIB_DIR, filename))


def after_settings(zappa_cli):
    """
    Activate shared object files so that they will be included in the zip package
    """
    if zappa_cli.command in ZAPPA_COMMANDS_REQUIRE_LIB_FILES:
        for filename in SO_FILENAMES:
            activate_shared_object(filename)


def after_zip(zappa_cli):
    """
    Deactivate shared object files so that they won't be used during development
    """
    if zappa_cli.command in ZAPPA_COMMANDS_REQUIRE_LIB_FILES:
        for filename in SO_FILENAMES:
            deactivate_shared_object(filename)
