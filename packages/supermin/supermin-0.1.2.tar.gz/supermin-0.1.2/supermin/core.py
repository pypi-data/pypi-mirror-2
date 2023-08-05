from supermin.config import config
import subprocess

def _minify(command):
    p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        return stdout
    return None

def minify(fpath):
    results = []
    for name, tpl in config.templates:
        if config.has_engine(name):
            engine, tpl = config.get_engine(name)
            command = tpl % {'bin': engine, 'in': fpath}
            minified = _minify(command)
            if not minified is None:
                results.append(minified)
    if not results:
        return None
    results.sort(key=lambda x: len(x))
    return results[0]

def get_available_templates():
    installed = []
    available = []
    for name, tpl in config.templates:
        if config.has_engine(name):
            installed.append(name)
        else:
            available.append(name)
    return installed, available

def get_available_engines():
    installed = []
    available = []
    for name, tpl in config.engines:
        if config.has_template(name):
            installed.append(name)
        else:
            available.append(name)
    return installed, available

def add_template(name, tpl):
    config.add_template(name, tpl)
    config.write()
    
def add_engine(name, path):
    config.add_engine(name, path)
    config.write()
    
def update_templates():
    config.update()
    