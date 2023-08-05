from mr.developer import common
import os
import re
import subprocess

logger = common.logger

RE_ROOT = re.compile(r'(:pserver:)([a-zA-Z0-9]*)(@.*)')


class CVSError(common.WCError):
    pass

def build_cvs_command(command, name, url, tag='', cvs_root=''):
    """
    Create CVS commands.
    
    Examples::
    
        >>> build_cvs_command('checkout', 'package.name', 'python/package.name')
        ['cvs', 'checkout', '-P', '-f', '-d', 'package.name', 'python/package.name']
        >>> build_cvs_command('update', 'package.name', 'python/package.name')
        ['cvs', 'update', '-P', '-f', '-d', 'package.name']
        >>> build_cvs_command('checkout', 'package.name', 'python/package.name', tag='package_name_0-1-0')
        ['cvs', 'checkout', '-P', '-r', 'package_name_0-1-0', '-d', 'package.name', 'python/package.name']
        >>> build_cvs_command('update', 'package.name', 'python/package.name', tag='package_name_0-1-0')
        ['cvs', 'update', '-P', '-r', 'package_name_0-1-0', '-d', 'package.name']
        >>> build_cvs_command('checkout', 'package.name', 'python/package.name', cvs_root=':pserver:user@127.0.0.1:/repos')
        ['cvs', '-d', ':pserver:user@127.0.0.1:/repos', 'checkout', '-P', '-f', '-d', 'package.name', 'python/package.name']
        
    """
    cmd = ['cvs']
    if cvs_root:
        cmd.extend(['-d', cvs_root])
    cmd.extend([command, '-P'])
    if tag:
        cmd.extend(['-r', tag])
    else:
        cmd.append('-f')
    cmd.extend(['-d', name])
    if command == 'checkout':
        cmd.append(url)
    
    return cmd
        

class CVSWorkingCopy(common.BaseWorkingCopy):
    def cvs_command(self, source, command, **kwargs):
        name = source['name']
        path = source['path']
        url = source['url']
        tag = source.get('tag')
        cvs_root = source.get('cvs_root')
        
        self.output((logger.info, 'Running %s %r from CVS.' % (command, name)))
        cmd = build_cvs_command(command, name, url, tag, cvs_root)

        ## because CVS can not work on absolute paths, we must execute cvs commands
        ## in parent directory of destination
        old_cwd = os.getcwd()
        os.chdir(os.path.dirname(path))

        try:
            cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = cmd.communicate()
        finally:
            os.chdir(old_cwd)
            
        if cmd.returncode != 0:
            raise CVSError('CVS %s for %r failed.\n%s' % (command, name, stderr))
        if kwargs.get('verbose', False):
            return stdout

    def checkout(self, source, **kwargs):
        name = source['name']
        path = source['path']
        update = self.should_update(source, **kwargs)
        if os.path.exists(path):
            if update:
                self.update(source, **kwargs)
            elif self.matches(source):
                self.output((logger.info, 'Skipped checkout of existing package %r.' % name))
            else:
                raise CVSError(
                    'Source URL for existing package %r differs. '
                    'Expected %r.' % (name, source['url']))
        else:
            return self.cvs_command(source, 'checkout', **kwargs)

    def matches(self, source):
	def normalize_root(text):
	    """
	    Removes username from CVS Root path.
	    """
	    return RE_ROOT.sub(r'\1\3', text)

	name = source['name']
        path = source['path']
        
        repo_file = os.path.join(path, 'CVS', 'Repository')
        if not os.path.exists(repo_file):
            raise CVSError('Can not find CVS/Repository file in %s.' % path)
        repo = open(repo_file).read().strip()        
        
        cvs_root = source.get('cvs_root')
        if cvs_root:
            root_file = os.path.join(path, 'CVS', 'Root')
            root = open(root_file).read().strip()            
            if normalize_root(cvs_root) != normalize_root(root):
                return False
        
        return (source['url'] == repo)

    def status(self, source, **kwargs):
        name = source['name']
        path = source['path']
        
	## packages before checkout is clean
	if not os.path.exists(path):
	    return 'clean'

        ## because CVS can not work on absolute paths, we must execute cvs commands
        ## in parent directory of destination
        old_cwd = os.getcwd()
        os.chdir(path)
        try:
            cmd = subprocess.Popen(
                ['cvs', '-q', '-n', 'update'], cwd=path, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = cmd.communicate()
        finally:
            os.chdir(old_cwd)
        
        status = 'clean'
        for line in stdout.split('\n'):
	    if not line or line.endswith('.egg-info'):
		continue
            if line[0] == 'C':
                ## there is file with conflict
                status = 'conflict'
                break
            if line[0] in ('M', '?', 'A', 'R'):
                ## some files are localy modified
                status = 'modified'
                
        if kwargs.get('verbose', False):
            return status, stdout
        else:
            return status

    def update(self, source, **kwargs):
        name = source['name']
        path = source['path']
        if not self.matches(source):
            raise CVSError(
                "Can't update package %r, because its URL doesn't match." %
                name)
        if self.status(source) != 'clean' and not kwargs.get('force', False):
            raise CVSError(
                "Can't update package %r, because it's dirty." % name)
        return self.cvs_command(source, 'update', **kwargs)

common.workingcopytypes['cvs'] = CVSWorkingCopy
