#!/usr/bin/python
import sys
import os
import csv
import collections
import re
from urllib import urlretrieve
import urlparse
import sqlite3
import thread

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import glib
from pkg_resources import load_entry_point

class DeckenGUI:
	
	def __init__(self):
		self.builder = gtk.Builder()
		self.gladefile = os.path.join(os.path.dirname(__file__), 'maginbook2.glade')
		self.builder.add_from_file(self.gladefile)
		#self.wTree = gtk.glade.XML(self.gladefile)
		self.window = self.get_widget("windowMain")
		self.statusbar = self.get_widget("statusbar1")
		
		Plugin = load_entry_point('DeckenMagicPlugin','decken.cards_plugin','magic')
		self.path_image, self.path_application = initials('magic')
		self.plugin = Plugin()
		if not self.is_tables_created('magic'):
			self.plugin.create_tables(self.get_conexao())
			self.set_tables_created('magic')
			self.plugin.load_sets(self.get_conexao())
			
		self.cartas = self.plugin.all_cards(self.get_conexao())

		
		self.imagem = self.get_widget('imagem_carta')
		pixbuf = gtk.gdk.pixbuf_new_from_file(self.plugin.get_image_back())
		pixbuf = pixbuf.scale_simple(312,445,gtk.gdk.INTERP_BILINEAR)
		self.imagem.set_from_pixbuf(pixbuf)
		# selecao de cards
		self.cartas_combo = self.get_widget('listbox')
		
		self.scrolledlistbox = self.get_widget('scrolledlistbox')
		
		self.scrolled_detail = self.get_widget('scrolled_detail')
		self.scrolled_detail.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.text_detail = self.get_widget('text_detail')
		self.text_detail.set_wrap_mode(gtk.WRAP_WORD)
		
		# cria uma liststre com uma coluna para usar como modelo
		##self.liststore = gtk.ListStore(str, str, str)
		self.liststore = gtk.ListStore( *tuple( [ str ] * self.plugin.number_columns_invisibles) )
		self.cartas_combo.set_model(self.liststore)
		# cria os cellrenderers para renderizar os texto
		for i in range(self.plugin.number_columns):
			self.cartas_combo.append_column(
				gtk.TreeViewColumn(self.plugin.columns_names[ i ], gtk.CellRendererText(), text = i )
			)
		
		for i in self.cartas:
			self.liststore.append( self.plugin.value_columns_by_card(i))

		dic = {
			'on_windowMain_destroy' : self.delete_event,
			'on_listbox_row_activated' : self.playlist_select_row,
			'on_caixa_pesquisa_changed' : self.filtrar_por_nome,
			'help_about' : self.mostrar_sobre,
		}
		#self.wTree.signal_autoconnect(dic)
		self.builder.connect_signals(self)
		
	def playlist_select_row(self, treeview, path, column):
   		self.cardlist_selected = self.liststore.get_iter(path)
		column_values = []
		for column in range(self.plugin.number_columns_invisibles):
			value = self.liststore.get_value(self.cardlist_selected, column)
			column_values.append(value)
		run_in_background(self.get_card_image, (column_values,))
		#run_in_background(self.set_detail, (column_values,))
		self.set_detail(column_values)
		self.statusBarUpdate(self.descricao_carta)
		#self.get_card_image(column_values)
		
	def set_detail(self, column_values):
		cards = self.plugin.find_card(self.get_conexao(), column_values)
		card = cards[0]
		self.descricao_carta = self.plugin.description_card(card)
		textbuffer = self.text_detail.get_buffer()
		textbuffer.set_text(self.plugin.detail_card(card))
		
	def get_card_image(self, column_values):
		cards = self.plugin.find_card(self.get_conexao(), column_values)
		card = cards[0]
		caminho = self.plugin.find_or_create_path(self.path_image, card)
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(caminho)
		except glib.GError:
			self.plugin.download_image(card, caminho)
			pixbuf = gtk.gdk.pixbuf_new_from_file(caminho)
		pixbuf = pixbuf.scale_simple(312,445,gtk.gdk.INTERP_BILINEAR)
		self.imagem.set_from_pixbuf(pixbuf)
		
	def filtrar_por_nome(self, widget):
		card = widget.get_text()
		if len(card) > 0:
			print card
			self.liststore.clear()
			cards = self.plugin.find_by_name(self.get_conexao(), card)
			for i in cards:
				self.liststore.append( self.plugin.value_columns_by_card(i) )
		else:
			self.liststore.clear()
			lista = self.plugin.all_cards(self.get_conexao())
			for i in lista:
				self.liststore.append( self.plugin.value_columns_by_card(i) )
		
	def delete_event(self, widget):
		print 'Oinc tchau!'
		gtk.main_quit()
		return False	
		
	def mostrar_sobre(self, widget):
		widget.show()
		
	def get_conexao(self):
		conn = sqlite3.connect(os.path.join(self.path_application,'database.db'))
		return conn
		
	def is_tables_created(self, name_plugin):
		try:
			reader = csv.reader(open(os.path.join(self.path_application,'tables_created.csv')))
		except IOError:
			arq = open( os.path.join(self.path_application,'tables_created.csv'), 'w' )
			arq.close()
			return False
		for i in reader:
			if i[0] == name_plugin:
				return True
		return False
		
	def set_tables_created(self, name_plugin):
		reader = csv.reader(open(os.path.join(self.path_application,'tables_created.csv')))
		plugins = []
		for i in reader:
			plugins.append(i[0])
		writer = csv.writer(open(os.path.join(self.path_application,'tables_created.csv'), 'w'))
		plugins.append(name_plugin)
		for i in plugins:
			writer.writerow(i)
		self.plugin.load_sets(self.get_conexao())
		self.statusBarUpdate("Sets loaded.")
		run_in_background(self.update_sets, ())
		
	def update_sets(self):
		atualizacao =  self.plugin.update_sets(self.get_conexao())
		for mensagem in atualizacao:
			self.statusBarUpdate(mensagem)
			
	def update_set_plugin(self, widget):
		run_in_background(self.update_sets, ())

	def get_widget(self, widget_name):
		"""Simplifies getting objects from glade file.
		"""
		return self.builder.get_object(widget_name)
		
	def statusBarUpdate(self, message):
		context_id = self.statusbar.get_context_id(message)
		self.statusbar.push(context_id, message)
			
	def start(self):
		"""Really starts the application.
		"""
		self.window.show()
		#self.statusBarUpdate(_("Application started."))
		if sys.platform == 'win32':
		    gobject.threads_init()
		else:
		    gtk.gdk.threads_init()

		gtk.main()

					
def run_in_background(func, args):
    thread.start_new(func, args)	

def initials(plugin_name):
	directory_application = '.decken'
	if sys.platform == 'darwin':
		home = os.environ['HOME']
		directory_image = 'Pictures'
	elif sys.platform == 'linux2':
		home = os.environ['HOME']
		directory_image = 'Images'
	else: # windows?
		home = os.environ['USERPROFILE']
		directory_image = 'Images'
	path_image = os.path.join(home, directory_image, 'decken', plugin_name)
	path_application = os.path.join(home, directory_application)
	try:
		os.listdir( path_image )
	except OSError:
		os.makedirs( path_image)
	try:
		os.listdir( path_application )
	except OSError:
		os.makedirs( path_application)
	return path_image, path_application
	
