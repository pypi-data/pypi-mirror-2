# -*- coding: utf-8 -*-

import sip, os, sys
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

import setproctitle
import warnings
warnings.filterwarnings("ignore", ".*sha module is deprecated.*", DeprecationWarning)
warnings.filterwarnings("ignore", ".*md5 module is deprecated.*", DeprecationWarning)
warnings.filterwarnings("ignore", ".*This application uses RandomPool.*", DeprecationWarning)

from PyQt4.QtCore import QCoreApplication, QTranslator, QLocale, QSettings
from PyQt4.QtGui import QApplication, QSystemTrayIcon, QImage

from tunneldialog import TunnelDialog

app = None
aboutData = None

name = "IOSSHy"
description = "Desktop tool to quickly setup SSH tunnels and automatically execute commands that make use of them"
version = "1.4"
url = "http://github.com/mtorromeo/iosshy"

def main():
	global app, aboutData

	setproctitle.setproctitle("iosshy")

	try:
		from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
		from PyKDE4.kdeui import KUniqueApplication

		aboutData = KAboutData(
			name, #appName
			"", #catalogName
			ki18n(name), #programName
			version,
			ki18n(description), #shortDescription
			KAboutData.License_BSD, #licenseKey
			ki18n("© 2010 Massimiliano Torromeo"), #copyrightStatement
			ki18n(""), #text
			url #homePageAddress
		)
		aboutData.setBugAddress("http://github.com/mtorromeo/iosshy/issues")
		aboutData.addAuthor(
			ki18n("Massimiliano Torromeo"), #name
			ki18n("Main developer"), #task
			"massimiliano.torromeo@gmail.com" #email
		)
		aboutData.setProgramLogo(QImage(":icons/network-server.png"))

		KCmdLineArgs.init (sys.argv, aboutData)
		KUniqueApplication.addCmdLineOptions()

		if not KUniqueApplication.start():
			print "%s is already running" % name
			sys.exit(0)

		app = KUniqueApplication()
	except ImportError:
		app = QApplication(sys.argv)
		app.setOrganizationName("MTSoft")
		app.setApplicationName(name)


	if QSystemTrayIcon.isSystemTrayAvailable():
		translator = QTranslator()
		qmFile = "tunneller_%s.qm" % QLocale.system().name()
		if os.path.isfile(qmFile):
			translator.load(qmFile)
		app.installTranslator(translator)

		dialog = TunnelDialog()
		sys.exit(app.exec_())
	else:
		print "System tray not available. Exiting."
		sys.exit(1)

if __name__ == "__main__":
	main()
