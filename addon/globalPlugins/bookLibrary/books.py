# -*- coding: utf-8 -*-
# books.py

#for compatibility with python3
try:
	import cPickle as pickle
except ImportError:
	import pickle

#.decode("mbcs")

import os, sys
import wx, gui
from logHandler import log

CURRENT_DIR= os.path.dirname(__file__).decode("mbcs") if sys.version_info.major == 2 else os.path.dirname(__file__)

SAVING_DIR= os.path.join(os.path.expanduser('~'), 'bookLibrary-addonFiles')

class Book(object):
	myBooks={}
	filename= ""

	def __init__(self, name, author, about, size, url, url2):
		super(Book, self).__init__()
		self.key= (name, author)
		self.name= name
		self.author= author
		self.about= about
		self.size= size
		self.url= url
		self.url2= url2

	@classmethod
	def add_book(cls, name, author, about, size, url, url2):
		book= cls(name, author, about, size, url, url2)
		cls.myBooks[book.key]= {"about": book.about, "size": book.size, "url": book.url, "url2": book.url2}
		#cls.save_to_file()

	@classmethod
	def remove_book(cls, bookKey):
		'''removing a book with the help of the book key.'''
		del cls.myBooks[bookKey]
		if not cls.myBooks:
			cls.save_to_file()

	@classmethod
	def remove_allBooks(cls):
		if not cls.myBooks:
			return
		cls.myBooks.clear()
		cls.save_to_file()

	# save data
	@classmethod
	def save_to_file(cls):
		try:
			with open(os.path.join(SAVING_DIR, cls.filename), 'wb') as f:
				pickle.dump(cls.myBooks, f, protocol=2)
			cls.myBooks= {}
		except Exception as e:
			log.info("Error",exc_info=1)
			return

	#retreave data
	@classmethod
	def retreave_from_file(cls):
		if cls.myBooks: return
		#else:
		try:
			with open(os.path.join(SAVING_DIR, cls.filename), 'rb') as f:
				d= pickle.load(f)
				cls.myBooks= d
		except EOFError:
			cls.myBooks= {}
			return
		except Exception as e:
			gui.messageBox("Unable to load data", "Error", wx.OK|wx.ICON_ERROR)
			log.info("Error", exc_info=1)
			return

	@classmethod
	def getBookByKey(cls, key):
		book= cls(key[0], key[1], cls.myBooks[key]['about'], cls.myBooks[key]['size'], cls.myBooks[key]['url'], cls.myBooks[key]['url2'])
		return book

	@classmethod
	def getBookByUrl(cls, url):
		key= [key for key in cls.myBooks if cls.myBooks[key]['url']== url]
		if key:
			book= cls.getBookByKey(key[0])
			return book

	@classmethod
	def getBookByUrl2(cls, url):
		key= [key for key in cls.myBooks if cls.myBooks[key]['url2']== url]
		if key:
			book= cls.getBookByKey(key[0])
			return book
