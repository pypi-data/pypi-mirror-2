import os
import copy
import imputil
import subprocess
import platform
import pkg_resources
import weakref

from iniparse import ConfigParser

from collective.buildout.cluster.states import STARTED, STOPPED, NOT_INSTALLED
from collective.buildout.cluster.states import STOPPING, STARTING, UNKNOWN
from collective.buildout.cluster.states import AUTOMATIC_START, MANUAL_START

class Base(object):

    service = 'Zope'

    def __init__(self, config, cluster):
        self.cluster = weakref.ref(cluster)
        self.config = config

    def __getitem__(self, name):
        return self.config[name]

    def items(self):
        return self.config.items()

    def setDefaults(self, config):
        for key, value in config.items():
            if not key in self.config:
                self.config[key] = value

    def exists(self):
        return self.config.get('location', None) is not None

    def getInstanceName(self):
        return self.config['name']

    def getInstanceHome(self):
        return self.config['location']
    
    def getBinDir(self):
        return self.config['bin-directory']

    def getVarDir(self):
        var_dir = self.config.get('var')
        if var_dir is not None:
            return var_dir
        return os.path.join(os.path.dirname(self.getBinDir()), 'var')

    def getPidFilename(self):
        pid_filename = self.config.get('pid-file')
        if pid_filename is not None:
            return pid_filename
        return os.path.join(self.getVarDir(), self.getInstanceName() + ".pid")
    
    def getInstanceCtl(self):
        return os.path.join(self.config['bin-directory'], self.config['name'])

    def setPort(self, port_name, value):
        cluster = self.cluster()
        if cluster is None:
            raise ValueError('Weak reference to cluster is gone!')

        cfg = ConfigParser()
        cfg.read(cluster.config_file)

        name = self.getInstanceName()
        if not cfg.has_section(name):
            raise ValueError('A section named %r does not exist!' % name)

        # Update or remove the given port name under the section
        # matching this cluster entry.
        port_name = '%s-address' % port_name
        if value is None:
            cfg.remove_option(name, port_name)
            if port_name in self.config:
                del self.config[port_name]
        else:
            cfg.set(name, port_name, value)
            self.config[port_name] = value

        fp = open(cluster.config_file, 'wb')
        try:
            cfg.write(fp)
        finally:
            fp.close()

    def getPort(self, name):
        pname = "%s-address" % name
        res = self.config.get(pname)
        if res is None:
            raise ValueError, "Unknown port"
        return res

    def _runCmd(self, cmd):
        ctl = self.getInstanceCtl()
        cmd = '%s %s' % (ctl, cmd)

        # The current python has probably set some
        # environment variables that may interfere
        # with calling our own python
        env = copy.deepcopy(os.environ)
        if 'PYTHONPATH' in os.environ:
            del env['PYTHONPATH']
        if 'PYTHONEXECUTABLE' in os.environ:
            del env['PYTHONEXECUTABLE']
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             shell=True, env=env)
        out, err = p.communicate()
        print "status: %s, output: %s, error: %s" % (p.returncode, out, err)
        return out
    
    def start(self):
        return self._runCmd('start')
    
    def stop(self):
        return self._runCmd('stop')

    def getStatus(self):
        output = self._runCmd('status')
        if output.find('program running') >= 0:
            return STARTED
        else:
            return STOPPED

    def isRunning(self):
        return self.getStatus() == STARTED


if platform.platform().find("Windows") < 0:
    class ClusterBase(Base): 
        pass
else:
    # pywintypes and pythoncom should come before other pywin32 modules
    # so our 'local' copy will be used instead of any possible 'system32' ones.
    import pywintypes
    import pythoncom

    import win32api
    import win32con
    import win32service
    import win32serviceutil

    state_map = {
        win32service.SERVICE_START_PENDING: STARTING,
        win32service.SERVICE_RUNNING:       STARTED,
        win32service.SERVICE_STOP_PENDING:  STOPPING,
        win32service.SERVICE_STOPPED:       STOPPED,
    }

    start_type_map = {
        win32service.SERVICE_AUTO_START: AUTOMATIC_START,
        win32service.SERVICE_DEMAND_START: MANUAL_START,
        }

    start_type_name = {
        "auto": win32service.SERVICE_AUTO_START,
        "manual": win32service.SERVICE_DEMAND_START,
        }

    class ClusterBase(Base):

        wait = 120

        def getServiceName(self):
            return '%s_%s' % (self.service, 
                              hash(self.getInstanceHome().lower()))

        def getServiceDisplayName(self):
            return '%s instance at %s' % (
                self.service, self.getInstanceHome())

        def isServiceInstalled(self):
            return self.getStatus() != NOT_INSTALLED

        def getStatus(self):
            sn = self.getServiceName()
            try:
                stat = win32serviceutil.QueryServiceStatus(sn)[1]
            except pywintypes.error, err:
                # service is not installed
                return NOT_INSTALLED
            return state_map.get(stat, UNKNOWN)

        def getStartType(self):
            if not self.isServiceInstalled():
                return MANUAL_START

            sn = self.getServiceName()
            hscm = win32service.OpenSCManager(None, None, win32con.GENERIC_READ)
            try:
                hs = win32service.OpenService(hscm, sn, win32con.GENERIC_READ)
                try:
                    cfg = win32service.QueryServiceConfig(hs)
                    return start_type_map.get(cfg[1], MANUAL_START)
                finally:
                    win32service.CloseServiceHandle(hs)
            finally:
                win32service.CloseServiceHandle(hscm)

        def start(self):
            status = self.getStatus()
            if status in (STARTED,):
                return

            sn = self.getServiceName()
            win32serviceutil.StartService(sn)

            if self.wait:
                win32serviceutil.WaitForServiceStatus(
                    sn, win32service.SERVICE_RUNNING, self.wait)

        def stop(self):
            status = self.getStatus()
            if status in (STOPPED,):
                return

            sn = self.getServiceName()
            win32serviceutil.StopService(sn)

            if self.wait:
                win32serviceutil.WaitForServiceStatus(
                    sn, win32service.SERVICE_STOPPED, self.wait)
        
        def getServiceClassString(self):
            # Try old location first.
            svc_base = self.service.lower() + "service"
            for svc_dir in (os.path.join(self.getInstanceHome(), "bin"),
                            os.path.join(self.cluster().path, "bin")):
                svc_filename = os.path.join(svc_dir, svc_base + ".py")
                if os.path.exists(svc_filename):
                    mod_base = os.path.splitext(svc_filename)[0]
                    return mod_base + ".InstanceService"

            # Fallback to the new location, in the nt_svcutils module.
            return pkg_resources.resource_filename(
                'nt_svcutils', 'service') + ".Service"
            
        def install(self, start_type="auto"):
            name = self.getServiceName()
            display_name = self.getServiceDisplayName()
            class_string = self.getServiceClassString()
            
            start_type = start_type_name[start_type]
            win32serviceutil.InstallService(class_string, name,
                                            display_name, start_type)
            self.SetKey("command", '"%s" fg' % self.getInstanceCtl())
            self.SetKey("pid_filename", self.getPidFilename())

        def remove(self):
            win32serviceutil.RemoveService(self.getServiceName())

        def OpenKey(self, keyname=None):
            keypath = ("System\\CurrentControlSet\\Services\\" + 
                       self.getServiceName())
            if keyname:
                keypath += ("\\" + keyname)
            return win32api.RegOpenKey(
                win32con.HKEY_LOCAL_MACHINE, keypath, 
                0, win32con.KEY_ALL_ACCESS)
    
        def SetKey(self, name, value, keyname="PythonClass"):
            key = self.OpenKey(keyname)
            try:
                win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, value)
            finally:
                win32api.RegCloseKey(key)


