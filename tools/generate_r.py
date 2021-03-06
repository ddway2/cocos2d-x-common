#!/usr/bin/python

#Run like:
#generate.py ./Resources/ ../gen

import sys
import os
import collections

SCRIPT_PATH=os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_PATH)

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

if( len(sys.argv) < 3 ):
	print ("Please pass path were to scan for resources")
	print ("EXAMPLE: generate.py ./Resources/ ../gen")
	exit (1)

R = [
	{'name':'Sprite','types':['png','jpg'], 'files':set()}
	,{'name':'Plist','types':['plist'], 'files':set()}
	,{'name':'Json','types':['json'], 'files':set()}
	,{'name':'Font','types':['ttf','fnt'], 'files':set()}
	,{'name':'TMX','types':['tmx'], 'files':set()}
]

scannedPath = os.path.normpath(sys.argv[1])
genPath = os.path.normpath(sys.argv[2])
print ('Scanning path: ', scannedPath)
scaledFolders = ["ldpi","mdpi","xxxhdpi","xxhdpi","xhdpi","hdpi"]

def isScalledFolder(path):
	return path.split('/')[1] in scaledFolders

def addFile(rType,path,fileName):
	print("Add %s to %s" % (os.path.join(path,fileName),rType['name']))
	folders = os.path.split(path)
	rType['files'].add(os.path.join(path,fileName))

def filterForType(rType,path,files):
	print("Filtring for %s -> %s" % (rType['name'],rType['types']))
	for fileName in files:
		for fileType in rType['types']:
			if fileName.endswith(fileType):
				addFile(rType,path,fileName)

def filterForR(path,files):
	for rType in R:
		filterForType(rType,path,files)

for root,dirs,files in os.walk(scannedPath):
	print("\n\nScanning: %s" % (root))
	root = root.replace(scannedPath,"",1)
	if len(root) == 0:
		root = "/"
	print("\n\nScanning: %s" % (root))
	if isScalledFolder(root):
		print("Got scallable path %s" % (root))
		root = ''.join(root.split('/',2)[2:])
		print("Got scallable path %s" % (root))
		filterForR(root,files)
	else:
		root = root[1:]
		filterForR(root,files)



print("#######################################################")
print("#######################################################")
print("#######################################################")
print("R structure:")
for rType in R:
	print(rType)


print("Generating gen")

rFileContentH = """/**********************************************************
	This file is autogenerated please do not modify it!
	Also don't include this in your revision system
**********************************************************/
#ifndef __R__
#define __R__
namespace R
{
"""
rFileContentCpp = """/**********************************************************
	This file is autogenerated please do not modify it!
	Also don't include this in your revision system
**********************************************************/
#include "R.h"
namespace R
{
"""

indention = 1

def normalizeVariableName(text):
	return os.path.split(text)[1].split('.')[0]

def printNamespace(name,namespace,indention):
	global rFileContentH
	global rFileContentCpp
	print("Namespace: %s" % name)

	if len(name) > 0:
		stringNamespace = ""
		stringNamespace += "\t"*indention + "namespace " + name + "\n"
		stringNamespace += "\t"*indention + "{\n"
		rFileContentH += stringNamespace
		rFileContentCpp += stringNamespace

		indention += 1
	if 'files' in namespace:
		for fileName in namespace['files']:
			print("\tFile: %s" % fileName)
			rFileContentH += "\t"*indention
			rFileContentCpp += "\t"*indention
			#extern const char* const BACKGROUND_GAME_PNG
			rFileContentH += "extern const char* const "
			rFileContentH += normalizeVariableName(fileName) + ";\n"
			#const char* const BACKGROUND_GAME_PNG = "game/background_game.png";
			rFileContentCpp += "const char* const "
			rFileContentCpp += normalizeVariableName(fileName)
			rFileContentCpp += ' = "' + fileName + '";\n'

	for nestedName,nestedNamespace in namespace.items():
		if nestedName == 'files':
			continue
		printNamespace(nestedName,nestedNamespace,indention)

	if len(name) > 0:
		indention -= 1
		rFileContentH += "\t"*indention + "}//" + name + "\n"
		rFileContentCpp += "\t"*indention + "}//" + name + "\n"

for rType in R:
	rFileContentH += "\t"*indention
	rFileContentH += "namespace " + rType['name'] + "\n"
	rFileContentH += "\t"*indention + "{\n"

	rFileContentCpp += "\t"*indention
	rFileContentCpp += "namespace " + rType['name'] + "\n"
	rFileContentCpp += "\t"*indention + "{\n"
	indention += 1
	# namespace
	namespaces = {}
	for fileName in rType['files']:
		pathAndFileName = os.path.split(fileName)

		previous = namespaces
		for namespace in pathAndFileName[0].split('/'):
			if namespace not in previous:
				previous[namespace] = {}
			previous = previous[namespace]
		if 'files' not in previous:
			previous['files'] = []
		previous['files'].append(fileName)

	for name,namespace in namespaces.items():
		printNamespace(name,namespace,indention)
	# namespace
	indention -= 1
	rFileContentH += "\t"*indention + "}\n"
	rFileContentCpp += "\t"*indention + "}\n"

indention -= 1
rFileContentH += "\t"*indention + "}\n"
rFileContentCpp += "\t"*indention + "}\n"

rFileContentH += "#endif\n"

if not os.path.exists(genPath):
	os.makedirs(genPath)

fileCpp = open(os.path.join(genPath, "R.cpp"), 'w')
fileH = open(os.path.join(genPath, "R.h"), 'w')

fileH.write(rFileContentH)
fileCpp.write(rFileContentCpp)
