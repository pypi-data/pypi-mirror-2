import os,tempfile,shutil,logging
log = logging.getLogger( __name__ )

class MockProc( object ):
    """Provides basic path-overriding process mocks for nose (or similar) test frameworks

    You would normally use a MockProc where you have code which uses subprocess
    to call an external program which would have negative effects were it to
    actually be called within your test framework.

    Limitations:

        Only works on PATH-looked-up executables, so e.g. /etc/init.d/* executables
        will *not* be overridden.

        Will not give you any notice if the mocking/faking fails.

        Default script template doesn't look at arguments or do "expect"-style
        parsing of input, so it just always produces the specified results.

        Not thread-safe.
    """
    def __init__( self, bindir=None ):
        self.scripts = {}
        self.bindir = bindir
    def __enter__( self ):
        """Write scripts to bindir (possibly creating it) and set PATH to use it"""
        if not self.bindir:
            self.bindir = tempfile.mkdtemp()
        bindir = self.bindir
        try:
            if not os.path.isdir( bindir ):
                os.makedirs( bindir )
        except (IOError,OSError,TypeError), err:
            log.warn( 'Could not create bin directory for mocks: %s', bindir )
            raise RuntimeError( """Unable to create test binary directory: %s"""%( bindir, ))
        os.environ['PATH'] = self.bindir + os.pathsep + os.environ.get( 'PATH', '' )
        for scripts in self.scripts.values():
            if scripts:
                self.write_script( scripts[-1] )
    enter = __enter__
    def __exit__( self ):
        """Delete bindir and remove from PATH"""
        if self.bindir:
            os.environ['PATH'] = os.environ.get( 'PATH', '' ).replace( os.pathsep + self.bindir, '' )
            for scripts in self.scripts.values():
                if scripts:
                    self.delete_script( scripts[-1] )
            shutil.rmtree( self.bindir, ignore_errors=True )
    exit = __exit__
    def write_script( self, description ):
        if not description.get('script'):
            description['script'] = self.script_template % description
        description['filename'] = filename = os.path.join( self.bindir, description['executable'] )
        fh = open( filename, 'w' )
        fh.write( description['script'] )
        fh.close()
        os.chmod( filename,0755 )
        return filename
    def delete_script( self, description ):
        try:
            filename = os.path.join( self.bindir, description['executable'] )
            os.remove( filename )
        except (OSError,IOError,TypeError), err:
            return False
        else:
            return True

    def append(
        self,
        executable,
        returncode = 0,
        stdout = None,
        stderr = None,
        script = None,
    ):
        """Add a new script to the bin-dir, 'pushes' the script into the stack..."""
        if not executable:
            raise ValueError( """Null executable not allowed""" )
        if os.path.basename( executable ) != executable:
            raise ValueError( """Only base-name executables can be overridden""" )
        description = {
            'executable': executable,
            'returncode': returncode,
            'stdout': stdout,
            'stderr': stderr,
            'script': script,
        }
        self.scripts.setdefault(executable,[] ).append( description )
        if self.bindir:
            self.write_script( description )
        return description
    def remove( self, executable ):
        """Pop the current executable from our set of scripts
        """
        try:
            scripts = self.scripts[executable]
            script = scripts.pop()
        except (KeyError,IndexError), err:
            return None
        else:
            if not scripts:
                if self.bindir:
                    self.delete_script( executable )
                del self.scripts[executable]
            else:
                if self.bindir:
                    self.write_script( scripts[-1] )
            return script

    script_template = """#! /usr/bin/env python

# mocked implementation of %(executable)s

import os,sys
stdout = %(stdout)r
stderr = %(stderr)r
if stdout:
    sys.stdout.write( stdout )
if stderr:
    sys.stderr.write( stderr )
sys.exit( %(returncode)s )
"""
