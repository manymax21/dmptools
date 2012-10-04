import sublime

def getSymbols():
	view = sublime.View
	symbols = view.get_symbols

	return symbols