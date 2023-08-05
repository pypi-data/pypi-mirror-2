"""USAGE:

freelancer [token_file]

TOKEN FILE

From within the shell, oauth.save({'file':'full/path/to/token/file'}) can be
used after oauth.getToken() to save your token to a file. Once it's save it
can be passed to freelancer and then loaded with oauth.load(), or just loaded
with oauth.load({'file':'full/path/to/token/file'})

COMMAND HELP

Within the shell, please use the help function of each module to get information
about available commands.

    Modules:
    admin -- contains the administrative commands for interactive shell
    api -- gives direct access to the freelancer.com API
    mock -- gives mock access to the freelancer.com API
    oauth -- contains the Oauth related commands for interactive shell

EXAMPLE

When using the shell with no token file available, you should run
oauth.getToken() first if you plan on using the api module.

freelancer>> oauth.getToken()
...
freelancer>> oauth.save({'file':'/full/path/to/token/file/freelancer.token'})
freelancer>> api.Profile.getAccountDetails()

After saving the token file, you can load it for use from within the shell.

freelancer>> oauth.({'file':'/full/path/to/token/file/freelancer.token'})
freelancer>> api.Profile.getAccountDetails()

If you don't want to make actual API calls, you can alternatively use the mock
module and not the oauth and api modules

freelancer>> mock.Profile.getAccountDetails()

Calling any module's help() function will print out its help text

freelancer>> oauth.help()

Use the admin.exit() method to leave the shell

freelancer>> admin.exit()"""

from freelancer.api import Freelancer
from freelancer.oauth import get_authorize_url, get_access_token
from freelancer.client import FreelancerClient
from exceptions import Exception

import sys
import readline

CONSUMER = ('b8720f555b3dd8ac538fd86ab67c9d4267373af5', '798dec89ac683b271e4a7aae56d41d9b7e019913')
SANDBOX = 'api.sandbox.freelancer.com'
SANDBOX_APP = 'http://www.sandbox.freelancer.com/users/api-token/auth.php'

class IncompatibleShell(Exception):
    pass

class InvalidCommand(Exception):
    pass

class FreelancerShell(object):

    def __init__(self, default_prompt='freelancer>>>', options={}):
        self.default_prompt = default_prompt
        self.options = options

    def msg(self, msg):
        print >>sys.stderr, msg

    def prompt(self, prompt='freelancer>>>'):
        return raw_input('%s ' % prompt)

    def exit(self, type=0):
        raise SystemExit(type)

class Command(object):
    """Within the shell, please use the help function (i.e., admin.help()) of each
module to get information about available commands.

    Modules:
    admin -- contains the administrative commands for interactive shell
    api -- gives direct access to the freelancer.com API
    mock -- gives mock access to the freelancer.com API
    oauth -- contains the Oauth related commands for interactive shell
    """
    def __init__(self, chain, shell):
        if not hasattr(shell, 'msg') or not hasattr(shell, 'prompt'):
            raise IncompatibleShell('Incompatible shell class passed to command')
        self.shell = shell
        
        self.chain, self.args = self.parse_cmd_from_list(chain)

    def do(self):
        if len(self.chain) < 2:
            return BadCommand(self.chain, self.shell).do()
        
        try:
            getattr(self, self.chain[1])(**self.args)
            return self.shell
        except AttributeError:
            return BadCommand(self.chain, self.shell).do()

    def help(self):
        pass
    
    def parse_cmd_from_list(self, chain):
        if len(chain) > 3:
            return((),())
        
        last = chain.pop()
        start_args = last.find('(')
        end_args = last.find(')')

        if start_args in [-1,0] or end_args in [-1,0,1]:
            return (chain,{})

        chain.append(last[0:start_args])

        try:
            if start_args + 1 == end_args:
                args = {}
            else:
                args = eval(last[start_args+1:end_args],{"__builtins__":None},{})
        except NameError:
            return ((),{})
        except SyntaxError:
            return ((), {})

        if not isinstance(args, dict):
            return ((),{})
        
        return (chain, args)

class BadCommand(Command):
    def __init__(self, chain, shell):
        if not hasattr(shell, 'msg') or not hasattr(shell, 'prompt'):
            raise IncompatibleShell('Incompatible shell class passed to command')
        self.shell = shell

    def do(self):
        msg = 'Invalid command. Use admin.help(), oauth.help(), api.help(), or\nmock.help() for more.'
        self.shell.msg(msg)

        return self.shell

class EmptyCommand(Command):
    def __init__(self, chain, shell):
        self.shell = shell

    def do(self):
        return self.shell

class ExitCommand(EmptyCommand):

    def do(self):
        AdminCommand(['admin', 'exit()'], self.shell).exit()

class AdminCommand(Command):
    """
    Contains the administrative commands for the freelancer interactive shell

    Available methods within the shell:
    * admin.exit() -- exit the shell
    * admin.help() -- print this help text
    * admin.reset() -- resets shell options back to default
    """

    def exit(self):
        self.shell.msg('Exitting freelancer shell...')
        self.shell.exit()

    def help(self):
        self.shell.msg(AdminCommand.__doc__)

    def reset(self):
        self.shell.options = DEFAULT_OPTIONS

class OauthCommand(Command):
    """
    Contains the Oauth related commands for the freelancer interactive shell

    Available methods within the shell:
    * oauth.setConsumer() -- set the consumer key and secret, parameters passed
      as a valid Python dictionary
        consumer_key -- consumer key
        consumer_secret -- consumer secret
    * oauth.setToken() -- set the token key and secret, parameters passed
      as a valid Python dictionary
        token -- your token
        token_secret -- your secret
    * oauth.getToken() -- fetch new access tokens, interactive prompts
    * oauth.save() -- save current token to file parameters passed
      as a valid Python dictionary
        file -- full path and filename of token file to be created
    * oauth.load() -- load token from file, parameters passed
      as a valid Python dictionary
        file -- full path and filename of token file to be opened
    * oauth.help() -- print this help text
    """
    def setConsumer(self, **kwargs):
        if not kwargs.get('consumer_key', False) or not kwargs.get('consumer_secret', False):
            msg = "Unable to set consumer key and secret. See oauth.help() for more."
            self.shell.msg(msg)
        else:
            self.shell.options['consumer'] = (kwargs.get('consumer_key', False), kwargs.get('consumer_secret', False))
    
        return self.shell

    def setToken(self, **kwargs):
        if not kwargs.get('token', False) or not kwargs.get('token_secret', False):
            msg = "Unable to set token key and secret. See oauth.help() for more."
            self.shell.msg(msg)
        else:
            self.shell.options['token'] = (kwargs.get('token', False), kwargs.get('token_secret', False))

        return self.shell

    def getToken(self):
        self.shell.msg("Visit this url to authorize this application: %s" % get_authorize_url(self.shell.options['consumer'], 'oob', SANDBOX_APP, domain=SANDBOX))
        self.shell.msg('')

        oauth_token = self.shell.prompt('What is your oauth token? ')
        verifier = self.shell.prompt('What is your verifier? ')
        try:
            self.shell.options['token'] = get_access_token(self.shell.options['consumer'], oauth_token, verifier, domain=SANDBOX)
        except ValueError:
            msg = 'Unable to retrieve access tokens. Try again.'
            self.shell.msg(msg)
            return self.shell

        self.shell.msg('')
        self.shell.msg("You can now use these access tokens to access the API:")
        self.shell.msg("     oauth_token: %s" % self.shell.options['token'][0])
        self.shell.msg("     oauth_token_secret: %s" % self.shell.options['token'][1])
        self.shell.msg('')
        self.shell.msg('To save this token for use with oauth.load(), save it with oauth.save()')

        return self.shell

    def save(self, **kwargs):
        if not kwargs.get('file', False) and not self.shell.options['token_file']:
            msg = "Unable to save token to file, missing file to save to.\nSee oauth.help() for more."
            self.shell.msg(msg)
            return self.shell

        try:
            file = open(kwargs.get('file', self.shell.options['token_file']), 'w')
            print >> file, self.shell.options['token'][0]
            print >> file, self.shell.options['token'][1]
            file.close()
            self.shell.msg('Token successfully saved to %s' % (kwargs.get('file', self.shell.options['token_file'])))
        except KeyError:
            msg = 'Unable to save token to file. You need a token first'
            self.shell.msg(msg)
        except:
            msg = "Unable to save token to file."
            self.shell.msg(msg)
            
        return self.shell
            
    def load(self, **kwargs):
        if not kwargs.get('file', False) and not self.shell.options['token_file']:
            msg = "Unable to load token from file, missing file to load from.\nSee oauth.help() for more."
            self.shell.msg(msg)
            return self.shell

        try:
            file = open(kwargs.get('file', self.shell.options['token_file']))
            self.shell.options['token'] = (file.readline().strip(), file.readline().strip())
            self.shell.msg('Token successfully loaded from %s' % (kwargs.get('file', self.shell.options['token_file'])))
        except:
            msg = "Unable to load token from file."
            self.shell.msg(msg)

        return self.shell

    def help(self):
        self.shell.msg(OauthCommand.__doc__)

class ApiCommand(Command):
    """
    Gives direct access to the freelancer.com API. Methods are directly bound
    to freelancer.com. All API call parameters need to be passed as a valid
    Python dictionary.

    Examples:

    # To search all PHP projects on Freelancer and return the latest 3
    api.Project.searchProjects({'count':3, 'searchjobtypecsv':'PHP'})

    # Return a user's profile details
    api.Profile.getAccountDetails()

    For all available methods, visit http://developer.freelancer.com/API
    """

    def do(self):
        if len(self.chain) < 2:
            return BadCommand(self.chain, self.shell).do()

        if self.chain[1] == 'help':
            self.help()
            return self.shell

        if not self.shell.options['token']:
            msg = 'No Oauth token available. Use oauth.getToken() or oauth.load()\nfirst. See oauth.help() for more.'
            self.shell.msg(msg)
            return self.shell

        try:
            client = FreelancerClient(self.shell.options['consumer'], self.shell.options['token'])
        except ValueError:
            self.shell.msg('Unable to initalized client, bad tokens.')
            return self.shell
        
        freelancer = Freelancer(client, SANDBOX)

        for link in self.chain[1:]:
            freelancer = getattr(freelancer, link)

        self.shell.msg("\nMaking request to %s://%s/%s.%s\n" % (freelancer.protocol, freelancer.domain, freelancer.uri, freelancer.format))

        resp = freelancer(self.args)
        self.shell.msg("%s\n" % resp)

        return self.shell

    def help(self):
        self.shell.msg(ApiCommand.__doc__)

class MockCommand(Command):
    """
    Gives mock access to the freelancer.com API to allow exploring the API
    without making actual API calls. Methods are directly bound
    to freelancer.com. All API call parameters need to be passed as a valid
    Python dictionary.

    Examples:

    # To search all PHP projects on Freelancer and return the latest 3
    mock.Project.searchProjects({'count':3, 'searchjobtypecsv':'PHP'})

    # Return a user's profile details
    mock.Profile.getAccountDetails()

    For all available methods, visit http://developer.freelancer.com/API
    """

    def do(self):
        if len(self.chain) < 2:
            return BadCommand(self.chain, self.shell).do()

        if self.chain[1] == 'help':
            self.help()
            return self.shell

        client = FreelancerClient(self.shell.options['consumer'])
        freelancer = Freelancer(client, SANDBOX)

        for link in self.chain[1:]:
            freelancer = getattr(freelancer, link)

        self.shell.msg("\nRequest to %s://%s/%s.%s\n" % (freelancer.protocol, freelancer.domain, freelancer.uri, freelancer.format))
        self.shell.msg('Call parameters (as a dict): %s\n' % self.args)

        return self.shell

    def help(self):
        self.shell.msg(MockCommand.__doc__)

COMMANDS = {
    'admin': AdminCommand,
    'oauth': OauthCommand,
    'api': ApiCommand,
    'mock': MockCommand,
    'exit': ExitCommand,
}

DEFAULT_OPTIONS = {
    'consumer': CONSUMER,
    'token': False,
    'token_file': ''
}

def cmd_to_action(cmd, shell):
    cmd = cmd.strip()

    if not len(cmd):
        cmd_chain = ()
        handler = EmptyCommand
    else:
        cmd = cmd.partition('(')
        cmd_chain = cmd[0].split('.', 3)
        cmd_chain.append(cmd_chain.pop() + cmd[1] + cmd[2])
        handler = COMMANDS.get(cmd_chain[0], BadCommand)

    action = handler(cmd_chain, shell)

    return action

def main(args=sys.argv[1:]):
    options = DEFAULT_OPTIONS

    try:
        options['token_file'] = args[0]
    except IndexError:
        options['token_file'] = ''

    shell = FreelancerShell('freelancer>>>', options)

    if 'help' in args or '-h' in args:
        shell.msg(__doc__)
        shell.exit()
    else:
        shell.msg(Command.__doc__)

    while 'you want to do this':
        try:
            cmd = shell.prompt()
            action = cmd_to_action(cmd, shell)
            shell = action.do()
        except InvalidCommand, e:
            shell.msg(e)
        except KeyboardInterrupt:
            shell.msg('\nKeyboard interrupt, exiting...')
            shell.exit()
        except EOFError:
            shell.msg('\nExiting...')
            shell.exit()

if __name__ == "__main__":
    main();