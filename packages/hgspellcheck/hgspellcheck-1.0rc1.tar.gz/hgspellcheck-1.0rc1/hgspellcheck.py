#!/usr/bin/python

import os

import enchant
from enchant.checker import SpellChecker
from mercurial import commands, extensions, util

def get_checker(ui):
	locale = ui.config('spellcheck', 'locale', 'en_US')
	pdictfile = ui.config('spellcheck', 'dictfile', '.dict-validwords')
	
	checker = SpellChecker(locale)
	
	if os.path.exists(pdictfile):
		for line in open(pdictfile):
			checker.add(line.strip())
			
	return checker

def hook(ui, repo, **kwargs):
	"""This hook fails if the commit message for the `node` parameter has spelling
	errors.
	"""
	
	if not 'node' in kwargs:
		raise util.Abort('You must use the spellcheck hook in a context that supplies a `node` parameter (e.g. pretxncommit)')
		
	checker = get_checker(ui)
	checker.set_text(repo[kwargs['node']].description())
	
	errors = 0
	
	for err in checker:
		errors += 1
		err.replace('>%s<' % err.word)
	
	if errors:	
		raise util.Abort('spelling error: %s' % checker.get_text())

def spellchecked(orig, ui, repo, *pats, **opts):
	locale = ui.config('spellcheck', 'locale', 'en_US')
	pdictfile = ui.config('spellcheck', 'dictfile', '.dict-validwords')
	
	msg = opts['message']
	
	checker = get_checker(ui)
	
	checker.set_text(msg)
	leftover = None
	
	for err in checker:
		w = err.word
		
		if w == leftover:
			continue

		suggestions = err.suggest()
		
		keys = ['&%s' % x for x in 'abcdef'.upper()][:len(suggestions)]
		ui.warn(checker.get_text().replace(w, '>%s<' % w), '\n\n')
		
		for letter, s in zip('abcdef'.upper(), suggestions):
			ui.write('  %s. %s\n' % (letter, checker.get_text().replace(w, '>%s<' % s)))
		
		ui.write('\n')	
		ui.write('  X. Custom replacement\n')
		ui.write('  Q. Cancel commit\n')
		ui.write('  +. Add "%s" to personal dictionary\n' % w)
		
		ri = ui.promptchoice('\n[%sxq+]:' % ''.join(k.replace('&', '').lower() for k in keys), keys + ['&X', '&Q', '&+'], 0)

		if ri == len(keys):
			checked = False
			while not checked:
				repl = ui.prompt('Replacement text [%s]:' % w, default=w)
				if repl == w:
					break
				checked = checker.check(repl)
				if not checked:
					ui.warn('  Spelling error in correction text!\n')
		elif ri > len(keys):
			if ri == len(keys) + 1:
				raise util.Abort('commit message failed spellcheck.')
			elif ri == len(keys) +2:
				repl = w
				checker.add(w)
				f = open(pdictfile, 'a')
				print >>f, w
				f.close()
		else:
			repl = suggestions[ri]
		
		if len(w) > len(repl):
			leftover = w[len(repl):]
			
		err.replace(repl)

	opts['message'] = checker.get_text()
	return orig(ui, repo, *pats, **opts)
	
def uisetup(ui):
	if not hasattr(extensions, 'wrapcommand'):
		return
	extensions.wrapcommand(commands.table, 'commit', spellchecked)
