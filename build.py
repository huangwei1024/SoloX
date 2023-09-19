# -*- coding: utf-8 -*-

import os
import re
import json
import shutil
import hashlib
import argparse
import datetime
import py_compile
import subprocess

import paramiko

from solox import __version__

def build(debug, console):
	# gen version
	now = datetime.datetime.now()
	versionDate = now.strftime("%Y%m%d.%H.%M")
	versionProduct = now.strftime("%Y.%m%d.%H.%M")

	pyfiglet = subprocess.check_output('pip show pyfiglet')
	match = re.search(r"Location: ([^\n]+)", pyfiglet.decode())
	if not match:
		raise Exception("check pyfiglet location")
	pyfiglet = os.path.join(match.group(1), 'pyfiglet')
	print(pyfiglet)

	command = [
		'pyinstaller',
		'-D',
		'--name=SoloX',
		'--noconfirm',

		'--paths=./;./solox/',

		'--add-data="./solox/public/;./public/"',
		'--add-data="./solox/static/;./static/"',
		'--add-data="./solox/templates/;./templates/"',
		'--add-data="%s;./pyfiglet/"' % pyfiglet,

		'--hidden-import=numpy',
		'--hidden-import=pyfiglet',
		'--hidden-import=pyfiglet.fonts',
		'--hidden-import=engineio.async_drivers.threading',

		'solox/debug.py'
	]
	if debug:
		command += [
			'-d',
			'--log-level=DEBUG'
		]
	if not console:
		command += ['-w']

	# compile app/defines.py python3
	# versionFile = 'app/defines.py'
	# if os.path.exists('app/__pycache__'):
	# 	shutil.rmtree('app/__pycache__')
	# with open(versionFile, 'r') as fp:
	# 	data = fp.read()
	# with open(versionFile, 'w') as fp:
	# 	old = data
	# 	data = re.sub(r"VERSION = [^\n]+", "VERSION = '%s'" % versionDate, data)
	# 	fp.write(data)
	# 	if old == data:
	# 		raise Exception("version not be update")
	# py_compile.compile(versionFile, doraise=True)

	command = ' '.join(command)
	print('\n\n')
	print('-'*10)
	print(command)
	print('-'*10)

	os.system(command)

	# rename
	# exeName = "SoloX_%s.exe" % (versionDate)
	# shutil.move('debug.exe', exeName)

	# export publish_version.json
	# with open(exeName, 'rb') as fp:
	# 	m = hashlib.md5()
	# 	m.update(fp.read())
	# 	md5 = m.hexdigest()

	# versionD = {
	# 	"version": versionDate,
	# 	"url": "http://192.168.1.98:9788/SoloX/%s" % exeName,
	# 	"md5": md5,
	# }
	# with open('publish_version.json', 'w') as fp:
	# 	json.dump(versionD, fp, indent=4, sort_keys=True)

	exeName = None
	return versionDate, exeName


def publish(versionDate, exeName):
	if not os.path.exists('publish_version.json'):
		raise Exception("publish_version.json not exists")

	with open('publish_version.json', 'r') as fp:
		versionD = json.load(fp)
		localMD5 = versionD['md5']
		print('local:', versionD)

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('192.168.1.98', port=22, username='root', key_filename='tjgame_f3322_net', disabled_algorithms=dict(pubkeys=['rsa-sha2-256', 'rsa-sha2-512']))

	if os.path.exists('remote_version.json'):
		os.remove('remote_version.json')

	sftp = client.open_sftp()
	sftp.get("/var/www/html/SoloX/version.json", "remote_version.json")

	with open("remote_version.json", "r") as f:
		remoteVersionD = json.load(f)
		print('remote:', remoteVersionD)

	if remoteVersionD['version'] == versionDate:
		print('version was the same, skip publish')
		return

	remotePath = "/var/www/html/SoloX/%s" % exeName
	sftp.put(exeName, remotePath)
	sftp.put("publish_version.json", "/var/www/html/SoloX/version.json")

	# verify remote exe
	stdin, stdout, stderr = client.exec_command("md5sum " + remotePath)
	output = stdout.read().decode().strip()
	print("ssh:", output)

	remoteMD5 = output.split()[0]
	if localMD5 != remoteMD5:
		raise Exception("remote md5 error")

	sftp.close()
	client.close()

	print("publish", exeName, "->", remotePath, "ok")

def main(args):
	print(args)

	versionDate, exeName = build(args.debug, args.console)
	if False and args.publish:
		# versionDate, exeName = "20230901.18.18", "SoloX_20230901.18.18.exe"
		publish(versionDate, exeName)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='SoloX_build', description='SoloX build tool')
	parser.add_argument('--debug', dest='debug', action="store_true", default=False, help='trace debug')
	parser.add_argument('--console', dest='console', action="store_true", default=True, help='windows console')
	parser.add_argument('--publish', dest='publish', action="store_true", default=False, help='publish to 192.168.1.98')

	main(parser.parse_args())
