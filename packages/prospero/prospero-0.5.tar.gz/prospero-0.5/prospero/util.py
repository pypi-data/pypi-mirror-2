# Copyright 2009-2010 numero, theothernumber.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Created on 17/04/2010

@author: numero
'''
from utils.encoding import smart_str
import hashlib, random, os, sys, signal, time

if os.name == 'nt':
    import Console
    import msvcrt
else:
    import termios
    import select
    
def get_hexdigest(salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    
    return hashlib.sha1(salt + raw_password).hexdigest()

def create_password(raw_password):
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]

    return salt + "$" + get_hexdigest(salt, raw_password)

def create_http_digest(username, realm, raw_password):
    
    return hashlib.md5(username + ":" + realm + ":" + raw_password).hexdigest()

def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    try:
        salt, hsh = enc_password.split('$')
        return hsh == get_hexdigest(salt, raw_password)
    except ValueError as e:
        return None
    
class Watcher:
    """this class solves two problems with multithreaded
    programs in Python, (1) a signal might be delivered
    to any thread (which is just a malfeature) and (2) if
    the thread that gets the signal is waiting, the signal
    is ignored (which is a bug).

    The watcher is a concurrent process (not thread) that
    waits for a signal and the process that contains the
    threads.  See Appendix A of The Little Book of Semaphores.
    http://greenteapress.com/semaphores/

    I have only tested this on Linux.  I would expect it to
    work on the Macintosh and not work on Windows.
    """
    
    def __init__(self):
        """ Creates a child thread, which returns.  The parent
            thread waits for a KeyboardInterrupt and then kills
            the child thread.
        """
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            #print "Waiting..."
            os.wait()
        except KeyboardInterrupt:
            # I put the capital B in KeyBoardInterrupt so I can
            # tell when the Watcher gets the SIGINT
            #print 'KeyBoardInterrupt'
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError: pass

class WindowsConsole:
    def __init__(self):
        self.console = Console.getconsole()

    def clear(self):
        self.console.page()

    def write(self, str):
        self.console.write(str)

    def sleep_and_input(self, seconds):
        time.sleep(seconds)
        if msvcrt.kbhit():
            return msvcrt.getch()
        return None

class UnixConsole:
    def __init__(self):
        self.fd = sys.stdin
        sys.exitfunc = self._onexit

    def _onexit(self):
        #termios.tcsetattr(self.fd.fileno(), termios.TCSADRAIN, self.old)
        pass

    def clear(self):
        sys.stdout.write('\033[2J\033[0;0H')
        sys.stdout.flush()

    def write(self, str):
        sys.stdout.write(str)
        sys.stdout.flush()

    def sleep_and_input(self, seconds):
        read,_,_ = select.select([self.fd.fileno()], [], [], seconds)
        if len(read) > 0:
            return self.fd.read(1)
        return None