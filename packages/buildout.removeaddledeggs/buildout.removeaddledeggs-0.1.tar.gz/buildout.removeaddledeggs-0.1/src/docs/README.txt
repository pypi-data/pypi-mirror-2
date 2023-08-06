buildout.removeaddledeggs
=========================

Q: What is a buildout extension ?

A: http://pypi.python.org/pypi/zc.buildout#extensions


Installation
------------
Add "buildout.removeaddledeggs" to the ``extension``-section in your buildout, like ::

	[buildout]
	parts =
		...
		
	extensions =
		buildout.removeaddledeggs
		