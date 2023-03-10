import os, tarfile, shutil, requests
import urllib.request
from functools import partial

from PyQt5.QtWidgets import QApplication, QFileDialog

from libmesact import firmware

def downloadFirmware(parent):
	board = parent.boardCB.currentData()
	if board:
		libpath = os.path.join(os.path.expanduser('~'), '.local/lib/libmesact')
		if not os.path.exists(libpath):
			os.makedirs(libpath)
		firmware_url = f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz'
		filename = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}.tar.xz')
		directory = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}')
		if os.path.isdir(directory):
			msg = (f'{board} firmware directory exists\n'
				'Delete it and download fresh?')
			if parent.questionMsg(msg, 'Firmware'):
				shutil.rmtree(directory)
			else:
				return
		download(parent, firmware_url, filename)
		with tarfile.open(filename) as f:
			f.extractall(libpath)
		# update firmware tab
		firmware.load(parent)
	else:
		parent.infoMsgOk('Select a Mesa Board\nto download firmware', 'Board')

def downloadAmd64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} amd64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_amd64.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_amd64.deb'
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		parent.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArmhDeb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} armhf Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_armhf.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_armhf.deb'
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		parent.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArm64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} arm64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_arm64.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_arm64.deb'
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		parent.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def download(parent, down_url, save_loc):
	def Handle_Progress(blocknum, blocksize, totalsize):
		## calculate the progress
		readed_data = blocknum * blocksize
		if totalsize > 0:
			download_percentage = readed_data * 100 / totalsize
			parent.progressBar.setValue(int(download_percentage))
			QApplication.processEvents()
	urllib.request.urlretrieve(down_url, save_loc, Handle_Progress)
	parent.progressBar.setValue(100)
	parent.statusbar.showMessage('Download Complete')
	parent.timer.start(5000)

def clearProgressBar(parent):
	parent.progressBar.setValue(0)
	parent.statusbar.clearMessage()
	parent.timer.stop()


