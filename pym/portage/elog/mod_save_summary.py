# elog/mod_save_summary.py - elog dispatch module
# Copyright 2006-2007 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Id$

import codecs
import time
from portage import os
from portage.data import portage_uid, portage_gid
from portage.localization import _
from portage.util import ensure_dirs, apply_permissions
from portage.const import EPREFIX

def process(mysettings, key, logentries, fulltext):
	if mysettings["PORT_LOGDIR"] != "":
		elogdir = os.path.join(mysettings["PORT_LOGDIR"], "elog")
	else:
		elogdir = os.path.join(EPREFIX, "var", "log", "portage", "elog")
	ensure_dirs(elogdir, uid=portage_uid, gid=portage_gid, mode=02770)

	# TODO: Locking
	elogfilename = elogdir+"/summary.log"
	elogfile = codecs.open(elogfilename, mode='a',
		encoding='utf_8', errors='replace')
	apply_permissions(elogfilename, mode=060, mask=0)
	elogfile.write(_(">>> Messages generated by process %(pid)d on %(time)s for package %(pkg)s:\n\n") %
			{"pid": os.getpid(), "time": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(time.time())), "pkg": key})
	elogfile.write(fulltext)
	elogfile.write("\n")
	elogfile.close()

	return elogfilename
