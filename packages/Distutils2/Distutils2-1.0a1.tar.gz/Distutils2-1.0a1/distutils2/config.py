"""distutils.pypirc

Provides the PyPIRCCommand class, the base class for the command classes
that uses .pypirc in the distutils.command package.
"""
import os
from ConfigParser import ConfigParser

from distutils2.cmd import Command

DEFAULT_PYPIRC = """\
[distutils]
index-servers =
    pypi

[pypi]
username:%s
password:%s
"""

class PyPIRCCommand(Command):
    """Base command that knows how to handle the .pypirc file
    """
    DEFAULT_REPOSITORY = 'http://pypi.python.org/pypi'
    DEFAULT_REALM = 'pypi'
    repository = None
    realm = None

    user_options = [
        ('repository=', 'r',
         "url of repository [default: %s]" % \
            DEFAULT_REPOSITORY),
        ('show-response', None,
         'display full response text from server')]

    boolean_options = ['show-response']

    def _get_rc_file(self):
        """Returns rc file path."""
        return os.path.join(os.path.expanduser('~'), '.pypirc')

    def _store_pypirc(self, username, password):
        """Creates a default .pypirc file."""
        rc = self._get_rc_file()
        f = open(rc, 'w')
        try:
            f.write(DEFAULT_PYPIRC % (username, password))
        finally:
            f.close()
        try:
            os.chmod(rc, 0600)
        except OSError:
            # should do something better here
            pass

    def _read_pypirc(self):
        """Reads the .pypirc file."""
        rc = self._get_rc_file()
        if os.path.exists(rc):
            self.announce('Using PyPI login from %s' % rc)
            repository = self.repository or self.DEFAULT_REPOSITORY
            config = ConfigParser()
            config.read(rc)
            sections = config.sections()
            if 'distutils' in sections:
                # let's get the list of servers
                index_servers = config.get('distutils', 'index-servers')
                _servers = [server.strip() for server in
                            index_servers.split('\n')
                            if server.strip() != '']
                if _servers == []:
                    # nothing set, let's try to get the default pypi
                    if 'pypi' in sections:
                        _servers = ['pypi']
                    else:
                        # the file is not properly defined, returning
                        # an empty dict
                        return {}
                for server in _servers:
                    current = {'server': server}
                    current['username'] = config.get(server, 'username')

                    # optional params
                    for key, default in (('repository',
                                          self.DEFAULT_REPOSITORY),
                                         ('realm', self.DEFAULT_REALM),
                                         ('password', None)):
                        if config.has_option(server, key):
                            current[key] = config.get(server, key)
                        else:
                            current[key] = default
                    if (current['server'] == repository or
                        current['repository'] == repository):
                        return current
            elif 'server-login' in sections:
                # old format
                server = 'server-login'
                if config.has_option(server, 'repository'):
                    repository = config.get(server, 'repository')
                else:
                    repository = self.DEFAULT_REPOSITORY
                return {'username': config.get(server, 'username'),
                        'password': config.get(server, 'password'),
                        'repository': repository,
                        'server': server,
                        'realm': self.DEFAULT_REALM}

        return {}

    def _metadata_to_pypy_dict(self):
        meta = self.distribution.metadata
        data = {
            'metadata_version' : meta.version,
            'name': meta['Name'],
            'version': meta['Version'],
            'summary': meta['Summary'],
            'home_page': meta['Home-page'],
            'author': meta['Author'],
            'author_email': meta['Author-email'],
            'license': meta['License'],
            'description': meta['Description'],
            'keywords': meta['Keywords'],
            'platform': meta['Platform'],
            'classifier': meta['Classifier'],
            'download_url': meta['Download-URL'],
        }

        if meta.version == '1.2':
            data['requires_dist'] = meta['Requires-Dist']
            data['requires_python'] = meta['Requires-Python']
            data['requires_external'] = meta['Requires-External']
            data['provides_dist'] = meta['Provides-Dist']
            data['obsoletes_dist'] = meta['Obsoletes-Dist']
            data['project_url'] = [','.join(url) for url in
                                   meta['Project-URL']]

        elif meta.version == '1.1':
            data['provides'] = meta['Provides']
            data['requires'] = meta['Requires']
            data['obsoletes'] = meta['Obsoletes']

        return data

    def initialize_options(self):
        """Initialize options."""
        self.repository = None
        self.realm = None
        self.show_response = 0

    def finalize_options(self):
        """Finalizes options."""
        if self.repository is None:
            self.repository = self.DEFAULT_REPOSITORY
        if self.realm is None:
            self.realm = self.DEFAULT_REALM
