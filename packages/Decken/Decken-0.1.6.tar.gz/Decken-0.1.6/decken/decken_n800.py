
from app.config import *

import sys
import os
import csv
import collections
import re
from urllib import urlretrieve
import urlparse
import sqlite3
sys.path.append(APP_ABS_PATH)

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import hildon

colecoes_diferentes = {
	'soa' : 'ala',
	'2010' : 'm10'
}

class MaginBookGUI():
	
	def __init__(self, cartas):
		
		self.program = hildon.Program()
		self.program.__init__()
		
		self.window = hildon.Window()
		self.window.set_title("Mamaemogin")
		self.program.add_window(self.window)
		
		if self.window:
			self.window.connect('destroy', gtk.main_quit)
			
		self.cartas = cartas
		self.gladefile = os.path.join(APP_ABS_PATH, 'projeto.glade')
		self.wTree = gtk.glade.XML(self.gladefile)
		
		# reparent the vbox1 from glade to self.window
		self.vbox1 = self.wTree.get_widget('vbox1')
		self.reparent_loc(self.vbox1, self.window)
		
		self.imagem = self.wTree.get_widget('imagem_carta')
		self.cardlist = self.wTree.get_widget('listbox')
		self.scrolledlistbox = self.wTree.get_widget('scrolledlistbox')
		self.cardlist_model = gtk.ListStore(gobject.TYPE_STRING)
		self.cardlist.set_model(self.cardlist_model)
		self.cardlist_renderer = gtk.CellRendererText()
		self.cardlist_column = gtk.TreeViewColumn("Card", self.cardlist_renderer, text=0)
		self.cardlist.append_column(self.cardlist_column)
		
		lista = self.cartas.keys()
		lista.sort()
		for i in lista:
			self.cardlist_model.set(self.cardlist_model.append(), 0, i)
		self.cardlist_selected = self.cardlist_model.get_iter_root()

		dic = {
			'on_windowMain_destroy' : self.delete_event,
			'on_listbox_row_activated' : self.playlist_select_row,
			'on_caixa_pesquisa_changed' : self.filtrar_por_nome,
		}
		self.wTree.signal_autoconnect(dic)
		self.gtkWindow = self.wTree.get_widget('windowMain')
		self.gtkWindow.destroy()
		self.window.show_all()
		
	def playlist_select_row(self, treeview, path, column):
   		self.cardlist_selected = self.cardlist_model.get_iter(path)
		card = self.cardlist_model.get_value(self.cardlist_selected, 0)
		self.get_card_image(card)
		
	def get_card_image(self, card):
		#nome, sigla, numero, tipo, mana, raridade, texto)
		colecao = self.cartas[card][1]
		carta = self.cartas[card][2]
		print self.cartas[card]
		self.descricao_carta = "%s - %s" % (self.cartas[card][0], colecao)
		if colecao not in os.listdir('setimages'):
			os.mkdir(os.path.join('setimages',colecao))
		caminho = "setimages/%s/%s.jpg" % (colecao, carta)
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(caminho)
		except:
			if colecao in colecoes_diferentes.keys():
				colecao = colecoes_diferentes[colecao]
			url = "http://magiccards.info/scans/en/%s/%s.jpg" % (colecao, carta)
			parsed = list(urlparse.urlparse(url))
			print 'Baixando ', parsed
			urlretrieve(urlparse.urlunparse(parsed), caminho)
			pixbuf = gtk.gdk.pixbuf_new_from_file(caminho)
		pixbuf = pixbuf.scale_simple(250,300,gtk.gdk.INTERP_BILINEAR)
		self.imagem.set_from_pixbuf(pixbuf)
		
	def filtrar_por_nome(self, widget):
		card = widget.get_text()
		if len(card) > 0:
			print card
			self.cardlist_model.clear()
			lista = self.cartas.keys()
			lista.sort()
			for i in lista:
				if re.match(card.upper(),i.upper()):
					self.cardlist_model.set(self.cardlist_model.append(), 0, i)
		else:
			lista = self.cartas.keys()
			lista.sort()
			for i in lista:
				self.cardlist_model.set(self.cardlist_model.append(), 0, i)
		

	def delete_event(self, widget):
		print 'Oinc tchau!'
		gtk.main_quit()
		return False		

def cartas():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute("select * from card")
	#ColecaoRegister = collections.namedtuple('ColecaoRegister','nome, sigla, numero, tipo, mana, raridade, texto')
	lista = {}
	for carta in c.fetchall():
		#nome, sigla, numero, tipo, mana, raridade, texto)
		lista[ carta[nome] ] = carta
	return lista

if __name__ == '__main__':
       pd = MaginBookGUI(cartas())

       if sys.platform == 'win32':
           gobject.threads_init()
       else:
           gtk.gdk.threads_init()

       gtk.main()
