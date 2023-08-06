=====================
cp.recipe.cmd package
=====================

.. contents::

What is cp.recipe.cmd ?
=======================

This recipe is used to run one or more command lines.

I stole this from iw.recipe.cmd (http://pypi.python.org/pypi/iw.recipe.cmd/0.1)

It works differently tho, when it comes to executing shell commands.  iw.recipe.cmd would push each command out separately in it's own shell.  Here I push them out to a shell script, and then run the shell script.  This way things like CD and other things that require state within the shell work great.

Also, I changed the way it works in the config file.
we have 2 options in the command.

[commandexample]
recipe = cp.recipe.cmd
install_cmds =
   echo "install commands go here"
	cd /tmp
	echo `pwd`
	echo 'see, I exist in one shell instance.'
update_cmds =
	echo "update commands go here"
	

On install, install_cmds will be turned into a shell script, and then ran.
on update, update_cmds will be turned into a shell script and then ran.  If you want update_cmds to be the same you can do something like this:
update_cmds = ${commandexample:install_cmd}

(where commandexample is the name of your part)

python code execution is unchanged in this version, and below are the original docs.


We need a config file::

  >>> cfg = """
  ... [buildout]
  ... parts = cmds
  ...
  ... [cmds]
  ... recipe = iw.recipe.cmd
  ... on_install=true
  ... cmds= %s
  ... """

  >>> test_file = join(sample_buildout, 'test.txt')
  >>> cmds = 'touch %s' % test_file
  >>> write(sample_buildout, 'buildout.cfg', cfg % cmds)

Ok, so now we can touch a file for testing::

  >>> print system(buildout)
  Installing cmds.

  >>> 'test.txt' in os.listdir(sample_buildout)
  True

And remove it::

  >>> test_file = join(sample_buildout, 'test.txt')
  >>> cmds = 'rm -f %s' % test_file
  >>> write(sample_buildout, 'buildout.cfg', cfg % cmds)

  >>> print system(buildout)
  Uninstalling cmds.
  Installing cmds.

  >>> 'test.txt' in os.listdir(sample_buildout)
  False

We can run more than one commands::

  >>> cmds = '''
  ... touch %s
  ... rm -f %s
  ... ''' % (test_file, test_file)

  >>> test_file = join(sample_buildout, 'test.txt')
  >>> cmds = 'rm -f %s' % test_file
  >>> write(sample_buildout, 'buildout.cfg', cfg % cmds)

  >>> print system(buildout)
  Updating cmds.

  >>> 'test.txt' in os.listdir(sample_buildout)
  False

We can also run some python code::

  >>> cfg = """
  ... [buildout]
  ... parts = py py2
  ...
  ... [py]
  ... recipe = iw.recipe.cmd:py
  ... on_install=true
  ... cmds= 
  ...   >>> sample_buildout = buildout.get('directory', '.')
  ...   >>> print os.listdir(sample_buildout)
  ...   >>> shutil.rmtree(os.path.join(sample_buildout, "bin"))
  ...   >>> print os.listdir(sample_buildout)
  ... [py2]
  ... recipe = iw.recipe.cmd:py
  ... on_install=true
  ... cmds=
  ...   >>> def myfunc(value):
  ...   ...     return value and True or False
  ...   >>> v = 20
  ...   >>> print myfunc(v)
  ... """

  >>> write(sample_buildout, 'buildout.cfg', cfg)

Ok, so now we run it::

  >>> print system(buildout)
  Uninstalling cmds.
  Installing py.
  ['.installed.cfg', 'bin', 'buildout.cfg', 'develop-eggs', 'eggs', 'parts']
  ['.installed.cfg', 'buildout.cfg', 'develop-eggs', 'eggs', 'parts']
  Installing py2.
  True


