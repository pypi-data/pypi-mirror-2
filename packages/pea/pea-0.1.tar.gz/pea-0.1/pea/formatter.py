import os
import sys
import nose
import functools
import termstyle

failure = 'FAILED'
error = 'ERROR'
success = 'passed'
skip = 'skipped'
line_length = 77

class PeaFormatter(nose.plugins.Plugin):
	name = 'pea'
	score = 500
	instance = None
	_newtest = False
	stream = None
	
	def __init__(self, *args):
		self.enabled = False
		type(self).instance = self

	def setOutputStream(self, stream):
		type(self).stream = stream

	def configure(self, options, conf):
		self.enabled = options.verbosity >= 2
		if not self.enabled: return
		color = getattr(options, 'color', True)
		force_color = getattr(options, 'force_color', False)
		if color:
			try:
				(termstyle.enable if force_color else termstyle.auto)()
			except TypeError: # happens when stdout is closed
				pass
		else:
			termstyle.disable()

	def beforeTest(self, test):
		type(self)._newtest = True
	
	def afterTest(self, test):
		if self.enabled and self._newtest is False:
			print >> self.stream, ""

	@classmethod
	def with_formatting(cls, prefix, func):
		def prn(s):
			if cls.instance and cls.instance.enabled:
				if cls._newtest:
					print >> cls.stream, ""
					cls._newtest = False
				print >> cls.stream, s

		@functools.wraps(func)
		def nice_repr(obj):
			return obj if isinstance(obj, str) else repr(obj)

		def _run(*a, **kw):
			name = func.__name__.replace('_', ' ')
			def desc(color):
				desc = color("    %s %s" % (prefix, name))
				if a:
					desc += ' ' + color(termstyle.bold(' '.join(map(nice_repr,a))))
				if kw:
					desc += ' ' + ' '.join([color("%s=%s") % (k, termstyle.bold(repr(v))) for k,v in kw.items()])
				return desc
			try:
				ret = func(*a, **kw)
				prn(desc(termstyle.green))
				return ret
			except:
				prn(desc(termstyle.red))
				raise
		return _run

