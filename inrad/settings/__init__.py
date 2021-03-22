import os

if "DJANGO_SETTINGS" in os.environ:
    if os.environ["DJANGO_SETTINGS"] == "dev":
        try:
            from .local import *
        except ImportError as e:
            from .default import *
else:
    from .prod import *
