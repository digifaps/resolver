#!/bin/bash
# postrm script for resolver
#
# see: dh_installdeb(1)

set -e

# summary of how this script can be called:
#        * <postrm> `remove'
#        * <postrm> `purge'
#        * <old-postrm> `upgrade' <new-version>
#        * <new-postrm> `failed-upgrade' <old-version>
#        * <new-postrm> `abort-install'
#        * <new-postrm> `abort-install' <old-version>
#        * <new-postrm> `abort-upgrade' <old-version>
#        * <disappearer's-postrm> `disappear' <overwriter>
#          <overwriter-version>
# for details, see http://www.debian.org/doc/debian-policy/ or
# the debian-policy package


case "$1" in
    remove|upgrade|failed-upgrade|abort-install|abort-upgrade|disappear)
        deluser --system resolver
        deluser --group --system resolver
    ;;

    purge)
        deluser --system resolver
        deluser --group --only-if-empty resolver
        rm -rf /etc/resolver
        rm /etc/apache2/sites-enabled/resolver.conf
        rm /etc/apache2/sites-available/resolver.conf
        rm /etc/supervisor/conf.d/resolver.conf
    ;;

    *)
        echo "postrm called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac

# dh_installdeb will replace this with shell code automatically
# generated by other debhelper scripts.

#DEBHELPER#

exit 0