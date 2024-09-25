#!/usr/bin/env python3
import os
import ipdb
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoORMBug.settings")
django.setup()
if __name__ == "__main__":
    from demo.models import demonstrate_bug

    try:
        demonstrate_bug()
    except Exception:
        ipdb.post_mortem()
