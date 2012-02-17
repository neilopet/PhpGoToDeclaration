'''
@name    GoToDeclaration
@package sublime_plugin
@author  Neil Opet

This Sublime Text 2 plugin will search all open tabs for the 
method declaration of the selected function.

Supports PHP only.
'''

import os
import sublime
import sublime_plugin

def is_php( view ):
	syntax, _ = os.path.splitext(os.path.basename(view.settings().get('syntax')))
	return (syntax == "PHP")

class PhpGoToDeclaration(sublime_plugin.EventListener):  
    def on_load(self, view):  
    	if not is_php(view):
    		return None

class PhpGoToDeclarationCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view()
		if not is_php(view):
			return None
		pt   = view.sel()[0].begin()
		word = view.substr(view.word(pt))
		self.searchViews( self.window.views(), word )

	def searchViews(self, views, word):
		for view in views:
			if self.search(view, word):
				self.window.focus_view(view)
	
	def search(self, view, word):
		region = view.find("function(.*%s)" % word, 0, sublime.IGNORECASE)
		if not region:
			return False
		else:
			self.window.focus_view(view)
			view.sel().clear()
			view.sel().add(view.word(region))