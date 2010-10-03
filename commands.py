# I18N extraction
# Usage : put this in $(play.path)/framework/pym/play/commands/i18n_extract.py
# Then run "play help" to check the task is well recognized, and "play i18n-extract" to fill up your messages files with
# the i18n strings found in your code (Java + views, files and directories starting with a dot are excluded)

import sys
import os
import re
import time
import locale

from play.utils import *

COMMANDS = ['i18n-extract']

HELP = {
	'i18n-extract': "Extracts I18N strings from classes and templates",
}

def execute(**kargs):
	app = kargs.get("app")
	app.check()
	
	i18nStrings = dict()
	
	print "~ Extracting i18n strings from Java files [Messages.get(\"...\")] ..."
	javaFiles = []
	for root, subFolders, files in os.walk(os.path.join(app.path, "app")):
		for file in files:
			javaFile = os.path.join(root, file)
			if isValidFile(javaFile, r"[^\.].*.java"):
				javaFiles.append(javaFile)
	javaI18nStrings = dict()
	for file in javaFiles:
		f = open(file)
		java = f.read()
		f.close()
		for match in re.finditer(r"Messages.get\(\"(.*?)\"\)", java):
			i18nString = match.group(1)
			javaI18nStrings[i18nString] = True
			i18nStrings[i18nString] = True
	print "~ Found %i i18n string(s) in %i Java file(s)..." % (len(javaI18nStrings), len(javaFiles))
	
	print "~ Extracting i18n strings from templates [&{'...'...}] ..."
	tplFiles = []
	for root, subFolders, files in os.walk(os.path.join(os.path.join(app.path, "app"), "views")):
		for file in files:
			tplFile = os.path.join(root, file)
			if isValidFile(tplFile, r"[^\.].*"):
				tplFiles.append(tplFile)
	tplI18nStrings = dict()
	for file in tplFiles:
		f = open(file)
		tpl = f.read()
		f.close()
		for match in re.finditer(r"&\{([\"'])(.*?)\1", tpl):
			i18nString = match.group(2)
			tplI18nStrings[i18nString] = True
			i18nStrings[i18nString] = True
	print "~ Found %i i18n string(s) in %i view file(s)..." % (len(tplI18nStrings), len(tplFiles))
	
	i18nStrings = i18nStrings.keys()
	print "~ Found %i i18n string(s) in your application, now let's fill up your messages files !" % len(i18nStrings)
	
	langs = app.readConf("application.langs").split(",")
	messagesFiles = [os.path.join("conf", "messages")]
	for lang in langs:
		messagesFiles.append(os.path.join("conf", "messages." + lang.strip()))
	for messagesFile in messagesFiles:
		strings = readMessagesFile(messagesFile)
		stringsToAdd = []
		for string in i18nStrings:
			if string not in strings:
				stringsToAdd.append(string)
		appendToMessagesFile(messagesFile, stringsToAdd)
		print "~ %s : %i string(s) added" % (messagesFile, len(stringsToAdd))

def isValidFile(path, fileNameRegex):
	base = os.path.basename(path)
	if not re.match(fileNameRegex, base):
		return False
	parts = os.path.split(os.path.dirname(path))
	for part in parts:
		if part[0] == '.':
			return False
	return True

def readMessagesFile(path):
	entries = dict()
	if os.path.exists(path):
		f = file(path)
		for line in f:
			linedef = line.strip()
			if len(linedef) == 0:
				continue
			if linedef[0] in ('!', '#'):
				continue
			if linedef.find('=') == -1:
				continue
			entries[linedef.split('=')[0].rstrip()] = linedef.split('=')[1].lstrip()
		f.close()
	return entries

def appendToMessagesFile(path, strings):
	if len(strings) > 0:
		text = "\n\n# Next %i lines were automatically added by i18n-extract on %s\n" % (len(strings), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		for string in strings:
			text += "%s = %s\n" % (string, "")
		f = open(path, "a")
		f.write(text)
		f.close()
