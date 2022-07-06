from gs_wik.settings.base import *

try:
    from gs_wik.settings.local import *

    live = False

except ImportError:

    live = True

if live:
    from gs_wik.settings.production import *
