bp.preferences is based on the Preference package available on PyPI (http://pypi.python.org/pypi/Preferences).

It overwrites the ``load_files`` method to change the behaviour of loading preferences from different files. On initialization preferences are always loaded in this order:

-   package_location/file_name.cfg  (contains default preferences)
-   /etc/file_name
-   ~/.file_name
-   current_working_direcory/file_name

Additionaly some methods are added to make conversion of preference values to Python types easier:

def _toString(self, value):
    Converts a string enclosed with single or double quotes to a Python string without quotes. This is needed e.g. to support preference values with leading/trailing whitespace characters.

