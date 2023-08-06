# MiscUtils
# Webware for Python
# See Docs/index.html

__all__ = [
	'Configurable', 'DBPool', 'DataTable', 'DictForArgs', 'Error',
	'Funcs', 'MixIn', 'NamedValueAccess', 'PropertiesObject', 'unittest']

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

try:
	import mx.DateTime as mxDateTime
except ImportError:
	mxDateTime = None

try:
	import datetime as nativeDateTime
except ImportError: # fallback for Python < 2.3
	if mxDateTime is None:
		try:
			import BasicDateTime as nativeDateTime
		except ImportError:
			nativeDateTime = None

try:
	from types import StringTypes
except ImportError: # fallback for Python < 2.2
	from types import StringType, UnicodeType
	StringTypes = (StringType, UnicodeType)

try: # for Python < 2.3
	True, False
except NameError:
	True, False = 1, 0
	bool = lambda x: x and True or False


class AbstractError(NotImplementedError):
	"""Abstract method error.

	This exception is raised by abstract methods in abstract classes. It
	is a special case of NotImplementedError, that indicates that the
	implementation won't ever be provided at that location in the future
	-- instead the subclass should provide it.

	Typical usage:

		from MiscUtils import AbstractError

		class Foo:
			def bar(self):
				raise AbstractError, self.__class__

	Note that adding the self.__class__ makes the resulting exception
	*much* more useful.

	"""
	pass

# @@ 2002-11-10 ce: SubclassResponsibilityError is is now deprecated (post 0.7)
# @@ (will be removed after 1.0)
SubclassResponsibilityError = AbstractError


class NoDefault:
	"""Singleton for parameters with no default.

	This provides a singleton "thing" which can be used to initialize
	the "default=" arguments for different retrieval methods. For
	example:

		from MiscUtils import NoDefault
		def bar(self, name, default=NoDefault):
			if default is NoDefault:
				return self._bars[name]  # will raise exception for invalid key
			else:
				return self._bars.get(name, default)

	The value None does not suffice for "default=" because it does not
	indicate whether or not a value was passed.

	Consistently using this singleton is valuable due to subclassing
	situations:

		def bar(self, name, default=NoDefault):
			if someCondition:
				return self.specialBar(name)
			else:
				return SuperClass.bar(name, default)

	It's also useful if one method that uses "default=NoDefault" relies
	on another object and method to which it must pass the default.
	(This is similar to the subclassing situation.)

	"""
	pass

# @@ 2002-11-10 ce: Tombstone is now deprecated (post 0.7)
# @@ (will be removed after 1.0)
Tombstone = NoDefault


def InstallInWebKit(appServer):
	pass
