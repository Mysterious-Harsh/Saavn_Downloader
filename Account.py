import os
import pygubu
from bs4 import BeautifulSoup
import requests

from scripts.helper import argManager, setProxy, scan_url

from scripts.saavnaccount import Account
from tkinter import messagebox
PROJECT_PATH = os.path.dirname( __file__ )
PROJECT_UI = os.path.join( PROJECT_PATH, "UI", "account.ui" )


class Accountform:

	def __init__( self, mainwindow ):
		self.builder = builder = pygubu.Builder()
		builder.add_resource_path( PROJECT_PATH )
		builder.add_from_file( PROJECT_UI )
		self.mainwindow = mainwindow
		self.account_F = builder.get_object( 'account_F' )
		builder.connect_callbacks( self )
		self.email_E = self.builder.get_object( "email_E" )
		self.password_E = self.builder.get_object( "password_E" )
		self.progressbar = self.builder.get_object( "progressbar" )
		self.filename_MTV = self.builder.tkvariables[ 'filename_MTV' ]
		self.email_E.focus_set()

	def login( self ):
		try:
			self.disable()
			self.account_F.update()
			album_name = "songs"
			proxies, headers = setProxy()
			self.account = Account(
			    proxies=proxies,
			    headers=headers,
			    email=self.email_E.get(),
			    password=self.password_E.get(),
			    progressbar=[ self.progressbar, self.account_F, self.filename_MTV ]
			    )
		except:
			self.enable()
			self.account_F.update()
			messagebox.showerror( 'Error', "Check your Email and Password" )

	def logout( self ):
		self.enable()
		self.progressbar[ 'value' ] = 0
		self.filename_MTV.set( "" )
		self.account_F.update()

	def download_playlists( self ):
		self.login()
		self.account.start_download_playlist()
		self.logout()

	def download_albums( self ):
		self.login()
		self.account.start_download_album()
		self.logout()

	def download_podcasts( self ):
		self.login()
		self.account.start_download_podcast()
		self.logout()

	def back( self ):
		self.account_F.destroy()
		pass

	def run( self ):
		self.mainwindow.mainloop()

	def disable( self ):
		for child in self.account_F.winfo_children():
			print( child )
			if str( child ) not in [
			    ".!labelframe2.!progressbar", ".!labelframe2.!label", ".!labelframe2.!message",
			    ".!labelframe2.!message2", ".!labelframe2.!message3"
			    ]:
				child.config( state="disabled" )

	def enable( self ):
		for child in self.account_F.winfo_children():
			if str( child ) not in [
			    ".!labelframe2.!progressbar", ".!labelframe2.!label", ".!labelframe2.!message",
			    ".!labelframe2.!message2", ".!labelframe2.!message3"
			    ]:
				child.config( state="enabled" )


if __name__ == '__main__':
	import tkinter as tk
	root = tk.Tk()
	app = Account( root )
	app.run()
