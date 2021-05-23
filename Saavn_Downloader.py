import os
import pygubu
from bs4 import BeautifulSoup
import requests

from scripts.helper import argManager, setProxy, scan_url
from scripts.content.playlist import Playlist
from scripts.content.album import Album
from scripts.content.artist import Artist
from scripts.content.song import Song
from scripts.saavnaccount import Account
# from scripts.content.podcast import Podcast
from tkinter import ttk, messagebox, PhotoImage
from Account import Accountform
PROJECT_PATH = os.path.dirname( __file__ )
PROJECT_UI = os.path.join( PROJECT_PATH, "UI", "saavn_downloader.ui" )


class SaavnDownloader:

	def __init__( self ):
		self.builder = builder = pygubu.Builder()
		builder.add_resource_path( PROJECT_PATH )
		builder.add_from_file( PROJECT_UI )
		self.mainwindow = builder.get_object( 'mainwindow' )
		self.mainwindow.tk.call( "wm", "iconphoto", self.mainwindow._w, PhotoImage( file="images/logo.png" ) )
		self.saavn_F = builder.get_object( 'saavn_F' )
		builder.connect_callbacks( self )
		self.config()
		self.get_widget_object()
		self.url_E.focus_set()

	def get_widget_object( self ):
		self.url_E = self.builder.get_object( "url_E" )
		self.progressbar = self.builder.get_object( "progressbar" )
		self.filename_MTV = self.builder.tkvariables[ 'filename_MTV' ]
		print( self.progressbar )

	def config( self ):
		self.s_w = self.mainwindow.winfo_screenwidth()
		self.s_h = self.mainwindow.winfo_screenheight()
		self.wow = 540
		self.how = 360
		x_c = ( ( self.s_w / 2 ) - ( self.wow / 2 ) )
		y_c = ( ( self.s_h / 2 ) - ( self.how / 2 ) )
		self.mainwindow.geometry( "%dx%d+%d+%d" % ( self.wow, self.how, x_c, y_c ) )
		self.style = ttk.Style( self.mainwindow )
		# print( self.style.theme_names() )
		# self.style.theme_use( "winnative" )
		self.style.configure(
		    "TLabelframe",
		    background="#ffffff",
		    highlightthickness=5,
		    highlightcolor='#000000',
		    relief="flat",
		    highlightbackground="#000000"
		    )
		# self.style.map( "TLabelframe", background=[ ( 'active', 'red' ) ] )ttk.Separator
		self.style.configure( "TSeparator", background="#000000" )

		self.style.configure(
		    "TLabelframe.Label",
		    background="#141414",
		    foreground="#ffffff",
		    font=( 'Arial', 14, 'bold' ),
		    width=self.wow,
		    anchor="center",
		    relief="flat"
		    )
		self.style.configure(
		    "Treeview",
		    fieldbackground="#ffffff",
		    background="#ffffff",
		    foreground="#000000",
		    font=( "Arial", 12, "bold" ),
		    borderwidth=5,
		    relief="flat"
		    )
		self.style.configure( "Treeview.Heading", font=( "Arial", 14, "bold" ) )

		self.style.configure(
		    "TButton",
		    background="#000000",
		    foreground="#000000",
		    font=( "Arial", 12, "bold" ),
		    relief="flat",
		    highlightthickness=5,
		    padding=5,
		    highlightcolor="blue",
		    bordercolor="#000000",
		    takefocus=True,
		    width=12
		    )
		# self.style.map( "TButton", background=[ ( 'active', 'blue' ) ] )
		self.style.configure(
		    "TLabel",
		    padding=2,
		    font=( "Arial", 12, "bold" ),
		    relief="flat",
		    width=10,
		    takefocus=False,
		    borderwidth=3,
		    cursor="arrow",
		    anchor="center"
		    )

		self.style.configure( "TEntry", fieldbackground="#99ddff" )

	def run( self ):
		self.mainwindow.mainloop()

	def read_urls( self, filepath ):
		urls = []
		with open( filepath, "r" ) as fh:
			for line in fh:
				url = line.strip()
				if url:
					urls.append( url )
		return urls

	def validate_url( self ):
		import re
		regex = re.compile(
		    r'^(?:http|ftp)s?://'  # http:// or https://
		    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
		    r'localhost|'  #localhost...
		    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
		    r'(?::\d+)?'  # optional port
		    r'(?:/?|[/?]\S+)$',
		    re.IGNORECASE
		    )

		print( re.match( regex, self.url_E.get() ) is not None )  # True
		# print(re.match(regex, "example.com") is not None)            # False

	def download( self, event=None ):
		# self.validate_url()
		try:
			self.disable()
			self.saavn_F.update()
			self.progressbar[ 'value' ] = 0
			self.saavn_F.update()

			progressbar = [ self.progressbar, self.saavn_F, self.filename_MTV ]
			args = argManager()

			album_name = "songs"
			proxies, headers = setProxy()
			if os.path.isfile( self.url_E.get() ):
				args.file = self.url_E.get()
			else:
				args.url = self.url_E.get()

			if args.url is None and args.file is None:
				dl_urls = [ self.url_E.get().strip() ]
			elif args.url is None and args.file:
				dl_urls = self.read_urls( self.url_E.get() )
			else:
				dl_urls = [ args.url ]

			for dl_url in dl_urls:
				dl_type = scan_url( url=dl_url )
				print( dl_type )
				if dl_type == 'playlist':
					playlist = Playlist( proxies, headers, progressbar, dl_url )
					playlist.start_download()
				elif dl_type == 'album':
					album = Album( proxies, headers, progressbar, dl_url )
					album.start_download()
				elif dl_type == 'artist':
					artist = Artist( proxies, headers, args, progressbar, dl_url )
					artist.start_download()
				elif dl_type == 'song':
					song = Song( proxies, headers, progressbar, dl_url )
					song.start_download()
				else:
					messagebox.showerror( 'Invalid', "Invalid URL !" )
				# elif dl_type == 'podcast':

				# 	podcast = Podcast( progressbar, proxies, headers )
				# 	show_json = podcast.getPodcast( dl_url )
				# 	podcast.dowloadPodcasts( show_json )
			self.enable()
			self.saavn_F.update()
			self.progressbar[ 'value' ] = 0
			self.filename_MTV.set( "" )
			self.saavn_F.update()
			print( 'DONE\n' )

		except Exception as e:
			messagebox.showerror( 'Error', e )
		finally:
			self.enable()
			self.progressbar[ 'value' ] = 0
			self.filename_MTV.set( "" )
			self.saavn_F.update()

	def disable( self ):
		for child in self.saavn_F.winfo_children():
			print( child )
			if str( child ) not in [
			    ".!labelframe.!progressbar", ".!labelframe.!label", ".!labelframe.!message", ".!labelframe.!message2",
			    ".!labelframe.!message3"
			    ]:
				child.config( state="disabled" )

	def enable( self ):
		for child in self.saavn_F.winfo_children():
			if str( child ) not in [
			    ".!labelframe.!progressbar", ".!labelframe.!label", ".!labelframe.!message", ".!labelframe.!message2",
			    ".!labelframe.!message3"
			    ]:
				child.config( state="enabled" )

	def account( self ):
		ac = Accountform( self.mainwindow )

	def exit( self ):
		self.mainwindow.destroy()


if __name__ == '__main__':
	app = SaavnDownloader()
	app.run()
