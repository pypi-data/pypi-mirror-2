import os
from ConfigParser import RawConfigParser
import urllib2

CONFIGS_UPDATE_URL = 'http://github.com/ojii/supermin/raw/master/supermin/default_configs.cfg'

class Configuration(object):
    def __init__(self):
        self.cfg = RawConfigParser()
        if not os.path.exists(self.filename):
            default = os.path.abspath(os.path.join(os.path.dirname(__file__), 'default_configs.cfg'))
            handle = open(default)
            self.update(handle)
            handle.close()
        self.cfg.read(self.filename)
        
    @property
    def filename(self):
        return os.path.join(os.path.expanduser('~'), '.supermin.cfg')
    
    def write(self):
        fp = open(self.filename, 'w')
        self.cfg.write(fp)
        fp.close()
    
    @property
    def engines(self):
        return self.cfg.items('engines')
    
    @property
    def templates(self):
        return self.cfg.items('templates')
    
    def has_engine(self, name):
        return self.cfg.has_option('engines', name)
    
    def has_template(self, name):
        return self.cfg.has_option('templates', name)
    
    def get_engine(self, name):
        assert self.has_engine(name)
        assert self.has_template(name)
        return self.cfg.get('engines', name), self.cfg.get('templates', name)
    
    def add_template(self, name, template):
        assert '%(bin)' in template
        assert '%(in)' in template
        if not self.cfg.has_section('templates'):
            self.cfg.add_section('templates')
        self.cfg.set('templates', name, template)
        
    def add_engine(self, name, path):
        assert os.path.exists(path)
        if not self.cfg.has_section('engines'):
            self.cfg.add_section('engines')
        self.cfg.set('engines', name, path)
        
    def update(self, handle=None):
        if not handle:
            handle = urllib2.urlopen(CONFIGS_UPDATE_URL) 
        cfg2 = RawConfigParser()
        cfg2.readfp(handle, 'updatecfg')
        for name, tpl in cfg2.items('templates'):
            if not self.has_template(name):
                self.add_template(name, tpl)
        for name, path in cfg2.items('engines'):
            if not self.has_engine(name):
                self.add_engine(name, path)
        self.write()
        
        
config = Configuration()