import logging, os, zc.buildout
import utils

class Mkdir:

    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              options['path'],
                              )
        if not os.path.isdir(os.path.dirname(options['path'])):
            logging.getLogger(self.name).error(
                'Cannot create %s. %s is not a directory.',
                options['path'], os.path.dirname(options['path']))
            raise zc.buildout.UserError('Invalid Path')


    def install(self):
        path = self.options['path']
        logging.getLogger(self.name).info(
            'Creating directory %s', os.path.basename(path))
        os.mkdir(path)
        return path

    def update(self):
        pass


class ExportObject:

    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        instance = options['instance']
        self.obj_path = options['obj'].split()
        self.instance = buildout[instance]
        self.path = os.path.join(buildout['buildout']['directory'], 'parts', self.name)

    def install(self):
        br = utils.get_browser(self.instance)
        for obj1 in self.obj_path:
            if not utils.export_one(self.instance, obj1, br):
                raise zc.buildout.UserError('%s Export failed' % obj1)
        if not os.path.exists(self.path): os.mkdir(self.path)
        return self.path

    def update(self):
        pass

class CopyFile:

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.path = os.path.join(buildout['buildout']['directory'], 'parts', self.name)
        self.files = options['files'].split()
        self.source = buildout[options['source']]
        self.target = buildout[options['target']]
        self.source_dir = options['source_dir']
        self.target_dir = options['target_dir']

    def install(self):
        """ copy file, create external method and run it """
        for f1 in self.files:
            utils.copy_file(self.source, self.source_dir, f1, self.target, self.target_dir)
        if not os.path.exists(self.path): os.mkdir(self.path)
        return self.path

    def update(self):
        pass

class ExternalMethod:

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        file_path = os.path.join(buildout['buildout']['directory'], options['source'])
        self.source_dir, self.source_file = os.path.split(file_path)
        instance = options['instance']
        self.instance = buildout[instance]
        self.function = options['func']
        self.out_file = options['output']
        self.path = os.path.join(buildout['buildout']['directory'], 'parts', self.name)
        self.args = {}
        if 'args' in options:
            for arg in options['args'].split():
                self.args[arg] = options[arg]

    def install(self):
        """ copy file, create external method and run it """
        local_instance = {}
        local_instance['host'] = 'localhost'
        utils.copy_file(local_instance, self.source_dir, self.source_file,
                        self.instance, self.instance['extensions'])
        br = utils.get_browser(self.instance)
        utils.create_ext_method(self.instance, self.function, self.source_file, self.function, br)
        utils.run_ext_method(self.instance, self.function, self.args, self.out_file, br)
        if not os.path.exists(self.path): os.mkdir(self.path)
        return self.path
 

    def update(self):
        pass


class DelObject:

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        instance = options['instance']
        self.obj = options['obj']
        self.host_name = buildout[instance]['host']
        self.port = buildout[instance]['port']
        self.zmi_user = buildout[instance]['zmi_user']
        self.zmi_pwd = buildout[instance]['zmi_pwd']
        self.plone_root = buildout[instance]['root']

    def install(self):
        """ copy file, create external method and run it """
        br = utils.get_browser(self.host_name, self.port, self.zmi_user, self.zmi_pwd)
        utils.del_object(self.host_name, self.port, self.plone_root, self.obj, br)
        path = os.path.join(buildout['buildout']['directory'], self.name)
        if not os.path.exists(path): os.mkdir(path)
        return path

    def update(self):
        pass



class ImportObject:

    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        instance = options['instance']
        self.obj = options['obj'].split()
        self.instance = buildout[instance]
        self.path = os.path.join(buildout['buildout']['directory'], 'parts', self.name)

    def install(self):
        """ copy file, create external method and run it """
        br = utils.get_browser(self.instance)
        for obj1 in self.obj:
            utils.import_one(self.instance, obj1, br)
        if not os.path.exists(self.path): os.mkdir(self.path)
        return self.path

    def update(self):
        pass


