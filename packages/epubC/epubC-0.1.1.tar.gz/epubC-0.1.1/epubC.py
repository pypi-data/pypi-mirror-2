##############################################################################
# File:            epubC.py
# Description:     Classes for editing an epub file.
# Authors:         Awad Mackie <firesock.serwalek@gmail.com>
# Date:            02-07-2010
# Copyright:       (c) 2010 firesock serwalek
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

##############################################################################/

"""
This modules provides classes to create a EPUB file from scratch given data.

See documentation on class Epub.
"""

import tempfile, shutil, os, zipfile, hashlib
#lxml imports
from lxml.builder import ElementMaker
from lxml import etree

class Epub(object):
	"""
	Class is used to create epub files, writing all necessary XML and contents pages.

	Example of use:
	import epubC
	
	ep = epubC.Epub("Title", "Author", "ID")
	
	As specifed, ID should be a unique identifier such as an ISBN. Attribs are set on the object
	for easy change.
	
	ep.add("content.html", "application/xhtml+xml", io.StringIO(html), "Chapter 1")

	Arcname is the internal name incase any other files reference it. html contents must be
	valid XHTML, so set media type accordingly. data is a stream out of an html string in memory,
	but can be data of any type, even binary.
	Title is the Chapter/Section name.
	
	ep.add("test.css", "text/css", io.StringIO(css))

	If the title is omitted or None, it assumes that it is not in the linear reading order
	and only adds it to the file.
	
	ep.write("test.epub")

	Creates the final file in name specified. No extensions are added, so specify full path.
	
	ep.close()

	Frees up temporary files made in the process. Call this unless you want your storage
	littered with files.

	Tested with Python v3.1 & 2.6 with lxml 2.2.6
	"""
	
	def _standard_setup(self):
		"""Internal function to create standard files at the beginning."""
		#Make internal directories
		self._meta = os.path.abspath(os.path.join(self._path, "META-INF"))
		self._oebps = os.path.abspath(os.path.join(self._path, "OEBPS"))
		os.mkdir(self._meta)
		os.mkdir(self._oebps)
		#Write mimetype
		with open(os.path.join(self._path, "mimetype"), "wt", encoding = "utf-8") as mimefile:
			mimefile.write("application/epub+zip")
		#Write meta container.xml - all readers start here.
		#Contents pretty much the same always but use lxml anyway
		E = ElementMaker(nsmap = {None: "urn:oasis:names:tc:opendocument:xmlns:container"})
		#to allow dashes, set attribs for rootfile by hand here
		rootfile_tag = E.rootfile()
		rootfile_tag.set("full-path", "OEBPS/content.opf")
		rootfile_tag.set("media-type", "application/oebps-package+xml")
		topelem = E.container(
			E.rootfiles(
				rootfile_tag
				),
			version="1.0"
			)
		tree = topelem.getroottree()
		#write into meta-inf in full representation
		tree.write(os.path.join(self._meta, "container.xml"), pretty_print = True,
				   xml_declaration = True, encoding = "utf-8")
	
	def __init__(self, title, author, uid, language="en-US"):
		"""Creates temporary space for epub file, and writes simple files.
		Call write() to create final output.

		Call close() to clear temporary space on the file system.

		Attributes are set on object using same names, e.g. title, author,
		uid and language and can be changed the same way"""
		self.title = title
		self.author = author
		self.uid = uid
		self.language = language
		#This holds everything the user adds in a list of tuples
		#(Filename in OEBPS, media-type, Title or None, id - Text)
		self._files = []
		self._path = os.path.abspath(tempfile.mkdtemp())
		#Create Element Factories for later use.
		#Content.opf creators
		#DCMI Main namespace - workaround for use in lxml
		dcmi = "http://purl.org/dc/elements/1.1/"
		self._DCMI = ElementMaker(namespace = dcmi)
		#OPF Main namespace with DCMI listed.
		self._OPF = ElementMaker(nsmap = {None: "http://www.idpf.org/2007/opf",
										  "dc": dcmi})
		#DAISY ns for the ncx file
		self._NCX = ElementMaker(nsmap = {None: "http://www.daisy.org/z3986/2005/ncx/"})
		self._standard_setup()

	def close(self):
		"""Clears filesystem of redundant files, obsoletes object.

		MAKE SURE TO CALL THIS ALWAYS."""
		shutil.rmtree(self._path)

	def _flush(self):
		"""Internal function that writes XML files into directory. Regenerates
		content-dependent data."""
		#To prevent adding these files to the manifest, as creating now, remove
		#if exist
		for file in ["content.opf", "toc.ncx"]:
			filen = os.path.join(self._oebps, file)
			if os.path.exists(filen):
				os.remove(filen)
		
		#Create DCMI namespace tags for use in OPF
		title_tag = self._DCMI.title(self.title)
		author_tag = self._DCMI.creator(self.author)
		uid_tag = self._DCMI.identifier(self.uid, id = "bookid")
		language_tag = self._DCMI.language(self.language)
		#Alias it to make it easiser
		O = self._OPF
		N = self._NCX

		#ncx is always present and written by this
		o_ncx = O.item(id = "ncx", href = "toc.ncx")
		o_ncx.set("media-type", "application/x-dtbncx+xml")
		#Manifest and spine for adding content
		manifest = O.manifest(o_ncx)
		spine = O.spine(toc="ncx")
		#navmap for ncx
		navmap = N.navMap()
		#Keep track of content added for ncx play order
		play_order = 1
		
		#iterate over added files.
		for filename, media, title, uid in self._files:
			item = O.item(id = uid, href = filename)
			item.set("media-type", media)
			manifest.append(item)
			#No title for content, its a resource.
			#Therefore, not in spine or ncx
			if title is None:
				continue
			spine.append(O.itemref(idref = uid))
			navmap.append(N.navPoint(
				N.navLabel(
					N.text(title),
					),
				N.content(src = filename),
				id = ("nav" + str(play_order)),
				playOrder = str(play_order)
				))
			play_order += 1
		
		#Generate full trees
		opf_topelem = O.package(
			O.metadata(
				title_tag,
				author_tag,
				uid_tag,
				language_tag
				),
			manifest,
			spine,
			version = "2.0"
			)
		opf_topelem.set("unique-identifier", "bookid")
		opf_tree = opf_topelem.getroottree()

		ncx_topelem = N.ncx(
			N.head(
				N.meta(name = "dtb:uid", content = self.uid),
				N.meta(name = "dtb:depth", content = "1"),
				N.meta(name = "dtb:totalPageCount", content = "0"),
				N.meta(name = "dtb:maxPageNumber", content = "0")
				),
			N.docTitle(
				N.text(self.title)
				),
			navmap,
			version = "2005-1"
			)
		ncx_tree = ncx_topelem.getroottree()
		
		opf_tree.write(os.path.join(self._oebps, "content.opf"), pretty_print = True,
					   xml_declaration = True, encoding = "utf-8")
		#NCX write, write doctype seperately - lxml doesn't seem to
		#Assume a xml declaration, then add.
		#lxml silliness - when I call tostring, and encoding str... I want my xml declaration
		#too please! - decode it given a known encoding
		ncx_text = etree.tostring(ncx_tree, pretty_print = True, xml_declaration = True,
								  encoding = "utf-8").decode("utf-8").splitlines(True)
		ncx_text.insert(1, "<!DOCTYPE ncx PUBLIC '-//NISO//DTD ncx 2005-1//EN' 'http://www.daisy.org/z3986/2005/ncx-2005-1.dtd'>\n")
		with open(os.path.join(self._oebps, "toc.ncx"), "wt", encoding = "utf-8") as ncx:
			for line in ncx_text:
				ncx.write(line)

	def write(self, file):
		"""Given an absolute filename, file, write as epub file.
		No extension is added, so provide full file and absolute path.

		Can be called as many times as necessary until close() is called.
		"""
		self._flush()
		
		#Final file output
		epub = zipfile.ZipFile(file, mode="w", compression=zipfile.ZIP_DEFLATED)

		#mimetype needs to be uncompressed and first.
		epub.write(os.path.join(self._path, "mimetype"), arcname = "mimetype",
				   compress_type=zipfile.ZIP_STORED)
		#then container.xml
		epub.write(os.path.join(self._meta, "container.xml"),
				   arcname = os.path.join("META-INF", "container.xml"))

		#Walk the directory chain, add everything in OEBPS
		top_len = len(self._path)
		for path, dirnames, filenames in os.walk(self._oebps):
			#Make archive directories relative to top, not absolute
			arc_dir = path[top_len:]
			for filen in filenames:
				epub.write(os.path.join(path, filen), arcname = os.path.join(arc_dir, filen))

		epub.close()

	def add(self, arcname, media_type, data, content_title = None):
		"""Main method to add contents to epub file.

		arcname is the epub internal name for a file.
		media_type is the MIME type for a file.
		data is a stream object that contains a file to be added.
		content_title is the title of this file. e.g. Chapter.
		- With no title it is treated as a resource not in the reading
		order.

		Will overwrite previous file with same arcname."""

		#Use md5 as ID, might be useful somewhere.
		md5 = hashlib.md5()
		with open(os.path.join(self._oebps, arcname), "wb") as arcfile:
			# A FALLACY! Read in block size, but y'know... this fails
			#for unicode strings... Why am I doing this again?
			block = data.read(md5.block_size)
			#Am I a string? Wrap a byte encode in here somewhere
			if isinstance(block, str):
				block = block.encode()
				data_read = lambda : data.read(md5.block_size).encode()
			else:
				data_read = lambda : data.read(md5.block_size)
			#Read file, update md5 and write
			while len(block) != 0:
				md5.update(block)
				arcfile.write(block)
				block = data_read()

		#Update filelist - id's need to start with a letter according
		#to epubcheck
		self._files.append((arcname, media_type, content_title, "h" + md5.hexdigest()))
