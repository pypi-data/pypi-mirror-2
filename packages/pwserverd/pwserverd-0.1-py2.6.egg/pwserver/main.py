#
#  pwserverd
#

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, defer
from twisted.application import service, internet
from optparse import OptionParser

import pwtools
from config import config

pwgen = pwtools.PasswordGenerator()
pwcheck = pwtools.PasswordChecker()

# Protocol state machine
WAIT_COMMAND       = 0
READING_PARAMETERS = 1
BAD_REQUEST        = 2

class PasswordProtocol (LineReceiver):

    def __init__(self, *args, **kwargs):
        self.state = WAIT_COMMAND
    
    def connectionMade(self):
        self.factory.numProtocols += 1
        if self.factory.numProtocols > 100:
            self.transport.write("500 Too many connections, try later\r\n")
            self.transport.loseConnection()

    def connectionLost(self, reason):
        self.factory.numProtocols -= 1

    def doGenerate(self, params):
        """Process a GENERATE command."""
        password = pwgen.generate(randomBits=int(params.get('randombits', '47')),
                                  maxLength=params.get('maxlength', None))
        self.transport.write('200 OK\r\n')
        self.transport.write('Password: %s\r\n\r\n' % password)

    def doCheck(self, password, params):
        """Process a CHECK command."""
        old_password = params.get('oldpassword', None)
        username = params.get('username', None)
        if old_password is not None:
            del params['oldpassword']
        if username is not None:
            del params['username']
            
        result = pwcheck.checkPassword(password,
                                       old_password=old_password,
                                       username=username,
                                       personal=params)
        if not result:
            self.transport.write('200 OK\r\n')
            self.transport.write('Status: Secure\r\n\r\n')
        else:
            self.transport.write('200 OK\r\n')
            self.transport.write('Status: Insecure\r\nReason: Password is %s\r\n\r\n' % result)

    def doCommand(self, cmd, args, parameters):
        if cmd == "GENERATE":
            self.doGenerate(parameters)
        elif cmd == "CHECK":
            self.doCheck(args[1], parameters)
        elif cmd == "SHUTDOWN":
            self.transport.write("200 OK\r\n\r\n")
            reactor.stop()
        elif cmd == "CLOSE":
            self.transport.write("200 OK\r\n\r\n")
            self.transport.loseConnection()
        else:
            self.transport.write("400 Bad Request\r\n\r\n")

    def lineReceived(self, line):
        """Called when we received a line of text from the client.  This
        function is responsible for parsing commands and reading parameter
        data for the command."""

        if config.get('main', 'debug') == 'true':
            print "$ %s" % line

        if self.state == WAIT_COMMAND:
            self.args = line.split(' ', 1)
            if len(self.args) < 1:
                return
        
            self.cmd = self.args[0].upper()
            self.state = READING_PARAMETERS
            self.params = {}
            self.previousParam = None
        elif self.state == READING_PARAMETERS:
            line = line.strip()
            if not line:
                self.doCommand (self.cmd, self.args, self.params)
                self.state = WAIT_COMMAND
                self.params = {}
                self.previousParam = None
            else:
                param, value = [s.strip() for s in line.split(':', 1)]
                if not param:
                    if not self.previousParam:
                        self.state = BAD_REQUEST
                    else:
                        self.params[self.previousParam] = '\r\n'.join([
                            self.params[self.previousParam], value])
                else:
                    param = param.lower()
                    self.params[param] = value
                    self.previousParam = param
        elif self.state == BAD_REQUEST:
            line = line.strip()
            if not line:
                self.transport.write("400 Bad Request\r\n\r\n")
                self.state = WAIT_COMMAND
                self.params = {}
                self.previousParam = None

class PasswordProtocolFactory (Factory):

    protocol = PasswordProtocol

    def __init__(self):
        self.numProtocols = 0

def main():
    print 'pwserverd starting'

    # Parse the arguments
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config_file",
                      default="/etc/pwserverd.cfg",
                      help="use the specified configuration file")

    (options, args) = parser.parse_args()

    # Read the configuration file
    config.read([options.config_file])

    # Set things up
    factory = PasswordProtocolFactory ()

    listeners = [l.strip() for l in config.get('main', 'listeners').split(',')]

    for listener in listeners:
        ltype = config.get(listener, 'type').strip().upper()
        if ltype == 'TCP':
            port = config.getint(listener, 'port')
            interface = '127.0.0.1'
            if config.has_option(listener, 'interface'):
                interface = config.get(listener, 'interface')
            print 'listening on interface %s port %s' % (interface, port)
            reactor.listenTCP(port, factory, interface=interface)
        elif ltype == 'UNIX':
            mode = 0644
            if config.has_option(listener, 'mode'):
                mode = int(config.get(listener, 'mode'), 0)
            socket = config.get(listener, 'socket')
            wantpid = True
            if config.has_option(listener, 'wantPID'):
                wantpid = config.getboolean(listener, 'wantPID')
            
            print 'listening on socket %s' % socket
            reactor.listenUNIX(socket, factory, mode=mode, wantPID=wantpid)
        else:
            print 'unknown listener type %s for listener %s' % (ltype, listener)

    reactor.run()
