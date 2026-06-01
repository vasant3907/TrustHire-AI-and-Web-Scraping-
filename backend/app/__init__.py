import platform
import sys

if sys.platform.startswith("win"):
    platform.machine = lambda: "AMD64"
