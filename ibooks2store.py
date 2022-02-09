#!/usr/bin/env python3
import zipfile
import plistlib
import getopt
import sys
import os
from shutil import copyfile

plistPath=""
inputDir=""
outputDir=""


def usage():
	print("-v|--version")
	print("-h|--help")
	print("-i|--inputdir")
	print("-o|--outputdir")
	print("-p|--plistfile")


def walk_dir(topdir, curdir, context, filefun, dirfun, topdown = True):
	for root, dirs, files in os.walk(curdir, topdown):
		for name in files:
			fullpath = os.path.join(root, name);
			filefun(context, fullpath, os.path.relpath(fullpath, topdir))
		for name in dirs:
			fullpath = os.path.join(root, name);
			dirfun(context, fullpath, os.path.relpath(fullpath, topdir))

def epubfile_add(zipFile, path, pathsave):
	print("add file: ", path)
	zipFile.write(path, pathsave, zipfile.ZIP_DEFLATED)

def epubdir_add(zipFile, path, pathsave):
	print("add dir: ", path)
	zipFile.write(path, pathsave, zipfile.ZIP_DEFLATED)

def create_epub(bookName,inPath,outPath):
	bookPath = os.path.join(outPath, bookName + '.epub');
	try: 
		zipFile = zipfile.ZipFile(bookPath, 'w')
		walk_dir(inPath, inPath, zipFile, epubfile_add, epubdir_add, False)
	except BaseException:
		print("error!")
	else:
		zipFile.close()

def main(argv):
	global plistPath,inputDir,outputDir
	opts,args = getopt.getopt(sys.argv[1:],'-h-i:-o:-p:-v',['help','inputdir=','outputdir=','plistfile=''version'])
	for opt_name,opt_value in opts:
		if opt_name in ('-h','--help'):
			print("[*] Help info")
			usage()
			exit()
		if opt_name in ('-v','--version'):
			print("[*] Version is 0.01 ")
			exit()
		if opt_name in ('-p','--plistfile'):
			plistPath = os.path.abspath(opt_value)
			print("[*] plistPath is ",plistPath)
		if opt_name in ('-i','--inputdir'):
			inputDir = os.path.abspath(opt_value)
			print("[*] inputDir is ",inputDir)
		if opt_name in ('-o','--outputdir'):
			outputDir = os.path.abspath(opt_value)
			print("[*] outputDir is ",outputDir)

	if plistPath == "" or outputDir == "":
		usage()
		exit()

	fp = open(plistPath, 'rb')
	pl = plistlib.load(fp)
	fp.close()

	for book in pl['Books']:
		bookName = book['itemName']
		if not book['genre'] is None:
			bookGenre = book['genre']
		else:
			bookGenre = 'Unknown'
		outDir = outputDir + os.path.sep + bookGenre
		outPath = outDir + os.path.sep + os.path.basename(book['path'])
		if inputDir != "" :
			inPath = inputDir + os.path.sep + os.path.basename(book['path'])
		else:
			inPath = book['path']
		bookType = book['BKBookType']

		if not os.path.exists(outDir):
			os.mkdir(outDir)
		if bookType == 'pdf':
			print ("%s : %s ==> %s" %(book['BKBookType'],inPath,outPath))
			copyfile(inPath, outPath)
		elif bookType == 'epub':
			print ("%s : %s ==> %s" %(book['BKBookType'],inPath,os.path.join(outDir, bookName + '.epub')))			
			create_epub(bookName,inPath,outDir)

main(sys.argv)
