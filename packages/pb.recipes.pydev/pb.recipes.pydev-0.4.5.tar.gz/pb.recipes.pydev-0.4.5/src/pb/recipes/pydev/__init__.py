from xml.dom import minidom, pulldom
import logging
import os
import shutil
import zc.recipe.egg

class PyDev(object):
    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        wd = self.buildout['buildout']['directory']

        self._remote_path = self.options.get('remote_path', None)

        res = []
        develop_locations = self.buildout['buildout']['directory']
        for _path in develop_locations:
            res.append(os.path.normpath(os.path.join(wd, './src')))
        self._ignored_paths = res

        self._fpath = self.options.get('pydevproject_path',
                                       os.path.join(wd, '.pydevproject'))
        self._backup_path = "%s.bak" % self._fpath
        self._python = options.get('target_python', 'python2.4')
        self._extra_paths = options.get('extra-paths', 
                                        options.get('extra_paths', '')
                                        ).split('\n')
        self._app_eggs = filter(None, options['eggs'].split('\n'))
        self.egg = zc.recipe.egg.Egg(self.buildout, self.name, self.options)

    def install(self):
        #egg_names, ws = egg.working_set(self._app_eggs)
        _reqs, ws = self.egg.working_set()
        egg_paths = ws.entries + self._extra_paths
        egg_paths = [p for p in egg_paths if p.strip() != '']   #strip empty paths
        
        # relocate eggs so paths are valid on remote computers (via nfs, smb, ...)
        if self._remote_path is not None:
            prefix = self.buildout['buildout']['directory']
            prefix_length = len(prefix)
            egg_paths = [p.startswith(prefix) and \
                            '%s%s'%(self._remote_path, p[prefix_length:]) or p \
                         for p in egg_paths]

        #strip develop paths,they're probably in Eclipse source path
        egg_paths = filter(lambda p: p not in self._ignored_paths, egg_paths)
        
        if not os.path.exists(self._fpath):
            logging.warning("Could not find .pydevproject file. Ignore this "
                            "message if you're not using Eclipse Pydev")
            return ""
        
        document = minidom.parse(self._fpath)
        project_node = document.getElementsByTagName('pydev_project')[0]

        nodes = document.getElementsByTagName('pydev_pathproperty')
        prop_nodes = filter(lambda node: (node.getAttribute('name') ==
                            'org.python.pydev.PROJECT_EXTERNAL_SOURCE_PATH'),
                       nodes
                   )
        for node in prop_nodes: #delete the PROJECT_EXTERNAL_SOURCE_PATH node
            project_node.removeChild(node)

        ext_node = document.createElement('pydev_pathproperty')
        ext_node.setAttribute('name',
                              'org.python.pydev.PROJECT_EXTERNAL_SOURCE_PATH')

        for p in egg_paths:
            node = document.createElement('path')
            node.appendChild(document.createTextNode(p))
            ext_node.appendChild(node)

        project_node.appendChild(ext_node)

        shutil.copy(self._fpath, self._backup_path) #make a copy of the file
        open(self._fpath, 'w').write(document.toxml())
            
        return ""

    update = install
