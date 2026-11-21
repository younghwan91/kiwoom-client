"""``python -m kiwoom_client`` — same as the ``kiwoom`` command."""

import sys

from kiwoom_client.cli import main

sys.exit(main())
