from twisted.internet import protocol, reactor
from twisted.web import xmlrpc, server
from twisted.application import service, internet
import os, signal
import cPickle
from task import Task
from pwd import getpwnam
import smtplib  
import ConfigParser, os
import socket

def notify (user, fromaddr, toaddrs, msg):
    ## fromaddr = 'fromuser@gmail.com'  
    ## toaddrs  = 'touser@gmail.com'  
    ## msg = 'There was a terrible error that occured and I wanted you to know!'  

    config = ConfigParser.SafeConfigParser()
    config_file = os.path.expanduser('~%s/.queue.cfg'%user)
    print 'notify: config_file:', config_file
    config.read (config_file)
    
    # Credentials (if needed)  
    username = config.get ('default', 'username')
    password = config.get ('default', 'password')
    server = config.get ('default', 'server')
    port = config.getint ('default', 'port')
    #print '%s:%d' % (server, port)
    # The actual mail send  
    server = smtplib.SMTP('%s:%d' % (server, port))
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, toaddrs, msg)  
    server.quit()  

class MyPP(protocol.ProcessProtocol):
    def __init__ (self, task):
        self.task = task
    ## def processExited(self, reason):
    ##     print "processExited, status %d" % (reason.value.exitCode,)
    def processEnded(self, reason):
        print "processEnded, task %s, status %s, exit %s, signal %s" % (self.task, reason.value.status, reason.value.exitCode, reason.value.signal)
        if self.task.notify:
            notify (self.task.user, self.task.user, self.task.notify, "processEnded, host %s, task %s, status %s, exit %s, signal %s" % (socket.gethostname(), self.task, reason.value.status, reason.value.exitCode, reason.value.signal))
        active_tasks.remove(self.task)
        schedule()
        
active_tasks = []
queued_tasks = []
stopped_tasks = []

def __detect_ncpus():
    """Detects the number of effective CPUs in the system"""
    #for Linux, Unix and MacOS
    if hasattr(os, "sysconf"):
        if "SC_NPROCESSORS_ONLN" in os.sysconf_names:
            #Linux and Unix
            ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
            if isinstance(ncpus, int) and ncpus > 0:
                return ncpus
        else:
            #MacOS X
            return int(os.popen2("sysctl -n hw.ncpu")[1].read())
    #for Windows
    if "NUMBER_OF_PROCESSORS" in os.environ:
        ncpus = int(os.environ["NUMBER_OF_PROCESSORS"])
        if ncpus > 0:
            return ncpus
    #return the default value
    return 1

n_cpu = __detect_ncpus()
print 'n_cpu:', n_cpu

def schedule ():
    active_cores = len (active_tasks)
    busy_cores = active_cores
    free = n_cpu - busy_cores
    print 'schedule enter:', 'active:', active_cores, 'busy:', busy_cores, 'free:', free
    if free > 0.5 and len(queued_tasks) != 0:
        new_task = queued_tasks.pop(0)
        active_tasks.append(new_task)
        if new_task.pid:
            os.kill (new_task.pid, signal.SIGCONT)
            print 'continued:', new_task
        else:
            args = new_task.args
            pp = MyPP(new_task)
            running_as_root = os.getuid() == 0
            stuff = getpwnam (new_task.user)
            if running_as_root:
                uid, gid = stuff[2], stuff[3]
            else:
                uid = gid = None
            path=new_task.path
            child_stdout_name = new_task.log_stdout or '/dev/null'
            child_stderr_name = new_task.log_stderr or '/dev/null'

            with open ('/dev/null', 'r') as child_stdin:
                with open (child_stdout_name, 'w') as child_stdout:
                    with open (child_stderr_name, 'w') as child_stderr:
                        if running_as_root:
                            if child_stdout_name:
                                os.fchown (child_stdout.fileno(), uid, gid)
                            if child_stderr_name:
                                os.fchown (child_stderr.fileno(), uid, gid)
                        print 'env:', new_task.env
                        r = reactor.spawnProcess(pp, args[0], args, env=new_task.env, path=path, uid=uid, gid=gid, childFDs={0:child_stdin.fileno(), 1:child_stdout.fileno(), 2:child_stderr.fileno()})

            new_task.pid = r.pid
            print 'started:', new_task, 'path:', path, 'uid:', uid, 'gid:', gid
    print 'schedule exit: active:', active_tasks, 'queued:', queued_tasks, 'stopped:', stopped_tasks

class Spawner(xmlrpc.XMLRPC):
    """An example object to be published."""

    def __init__ (self):
        xmlrpc.XMLRPC.__init__ (self, allowNone=True)
        self.task_num = 0

    def xmlrpc_queue(self, args, user, path, env, log_stdout, log_stderr, email):
        env = cPickle.loads (env)
        print 'queue:', args, user, env, log_stdout, log_stderr
        queued_tasks.append (Task (args, user, self.task_num, path, env, log_stdout, log_stderr, email))
        self.task_num += 1
        schedule()
        return self.task_num-1
        
    def xmlrpc_kill(self, task_num, sig):
        print 'kill:', task_num, sig
        task = filter (lambda t: t.num == task_num, queued_tasks)
        if task:
            queued_tasks.remove (task[0])
            return True
        else:
            task = filter (lambda t: t.num == task_num, active_tasks)
            if len (task) == 0:
                raise xmlrpc.Fault (task_num, 'task not found')
            os.kill (task[0].pid, sig)
            return True

    def xmlrpc_suspend(self, task_num):
        task = filter (lambda t: t.num == task_num, active_tasks)
        assert (task != [])
        print 'suspend:', task[0]
        os.kill (task[0].pid, signal.SIGSTOP)
        active_tasks.remove (task[0])
        stopped_tasks.append (task[0])
        schedule()
        return True
    
    def xmlrpc_go(self, task_num):
        task = filter (lambda t: t.num == task_num, stopped_tasks)
        assert (task != [])
        print 'continue:', task[0]
        stopped_tasks.remove (task[0])
        queued_tasks.insert (0, task[0])
        schedule()
        return True
    
    def xmlrpc_terminate (self):
        print 'terminate'
        os.kill (0, signal.SIGTERM)
        return True
    
    def xmlrpc_get_tasks(self):
        print 'get_tasks:', str ((active_tasks, queued_tasks, stopped_tasks))
        return cPickle.dumps ((active_tasks, queued_tasks, stopped_tasks))
    
