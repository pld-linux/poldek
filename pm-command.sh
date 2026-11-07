#!/bin/sh
# wrapper to add pre-install.d and post-install.d support for pm command in poldek

/bin/run-parts /etc/poldek/pre-install.d

/bin/rpm "$@"
rc=$?

/bin/run-parts /etc/poldek/post-install.d

exit $rc
