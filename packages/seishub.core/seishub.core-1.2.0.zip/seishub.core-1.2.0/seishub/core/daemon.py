"""
The SeisHub Daemon: platform-independent interface.
"""
from seishub.core.env import Environment
from seishub.core.services.manhole import ManholeService
from seishub.core.services.sftp import SFTPService
from seishub.core.services.ssh import SSHService
from seishub.core.services.web import WebService
from twisted.application import service
from twisted.python import usage
from twisted.scripts.twistd import _SomeApplicationRunner, ServerOptions
import sys


__all__ = ['run', 'createApplication']


def createApplication(path, log_file=None, create=False):
    # create application
    application = service.Application("SeisHub")
    # setup our Environment
    env = Environment(path, application=application, log_file=log_file,
                      create=create)
    # add services
    WebService(env)
    SSHService(env)
    ManholeService(env)
    SFTPService(env)
    #HeartbeatService(env)
    return application


class SeisHubApplicationRunner(_SomeApplicationRunner):
    """
    """
    def __init__(self, config, log_file):
        _SomeApplicationRunner.__init__(self, config)
        self.log_file = log_file
        self.config = config

    def createOrGetApplication(self):
        return createApplication(self.config.get('rundir'), self.log_file)


def run():
    # parse daemon configuration
    config = ServerOptions()
    try:
        config.parseOptions()
    except usage.error, ue:
        print config
        print "%s: %s" % (sys.argv[0], ue)
        return
    # debug modus
    if config['nodaemon']:
        log_file = None
    else:
        log_file = 'seishub.log'
    # start Twisted event loop
    SeisHubApplicationRunner(config, log_file).run()


if __name__ == '__main__':
    run()
