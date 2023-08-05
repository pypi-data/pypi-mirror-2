import hildon
import ui
import gtk

class Decken800GUI(ui.DeckenGUI):
	
	def __init__(self):
		
		self.program = hildon.Program()
		self.program.__init__()
		
		self.window = hildon.Window()
		self.window.set_title("Decken")
		self.program.add_window(self.window)
		
		if self.window:
			self.window.connect('destroy', gtk.main_quit)
			
		# chamar init da superclasse
		super(B, self).__init__()
		
		# reparent the vbox1 from glade to self.window
		self.vbox1 = self.get_widget('vbox1')
		self.reparent_loc(self.vbox1, self.window)
		

		self.gtkWindow = self.get_widget('windowMain')
		self.gtkWindow.destroy()
		self.window.show_all()
		