import os
import time
import base64
from zope.testbrowser.browser import Browser
from urllib2 import HTTPError

RETRIES = 1

Browsers = {}


def import_one(instance, obj, br):
    host_name, host_port, plone_root = (instance['host'], instance['port'], instance['root'])
    del_object(host_name, host_port, plone_root, obj, br)
    pos = obj.rfind('/')
    if pos == -1:
        url = 'http://%s:%s/%s/manage_importObject?file=%s.zexp&set_owner:int=0'% (host_name,
                   host_port, plone_root, obj)
    else:
        top_obj = obj[:pos]
        obj = obj[pos+1:]
        url = 'http://%s:%s/%s/%s/manage_importObject?file=%s.zexp&set_owner:int=0'% (host_name,
                   host_port, plone_root, top_obj, obj)

    for r1 in range(RETRIES):
        try:
            br.open(url)
        except HTTPError:
            # print '1=', sys.exc_info()[1]
            time.sleep(10)
            continue
        else:
            break
    s1 = br.contents
    return s1.find('successfully imported') != -1

def export_one(instance, obj, br):
    host_name, host_port, plone_root, user, export_folder = (instance['host'], instance['port'],
        instance['root'], instance['user'], instance['export'])
    pos = obj.rfind('/')
    if pos == -1:
        url = 'http://%s:%s/%s/manage_exportObject?id=%s&download:int=0&submit=Export'% (host_name,
                   host_port, plone_root, obj)
    else:
        top_obj = obj[:pos]
        obj = obj[pos+1:]
        url = 'http://%s:%s/%s/%s/manage_exportObject?id=%s&download:int=0&submit=Export'% (host_name,
                   host_port, plone_root, top_obj, obj)

    export_file = '%s/%s.zexp' % (export_folder, obj)

    cmd = 'rm -f %s' % export_file
    if host_name != 'localhost':
        cmd = 'ssh %s@%s %s' % (user, host_name, cmd)
    os.system(cmd)

    for r1 in range(RETRIES):
        try:
            f1 = br.open(url)
        except HTTPError:
            # print '1=', sys.exc_info()[1]
            time.sleep(10)
            continue
        else:
            break
    s1 = br.contents
    str1 = "successfully exported"
    return s1.find(str1) >= 0

def copy_file(source, source_dir, file_name, target, target_dir):
    if source['host'] == 'localhost':
        source_file = '%s/%s' % (source_dir, file_name)
    else:
        source_file = '%s@%s:%s/%s' % (source['user'], source['host'], source_dir, file_name)
    if target['host'] == 'localhost':
        target_file = target_dir
    else:
        target_file = '%s@%s:%s' % (target['user'], target['host'], target_dir)
    pos1 = source_file.find(':')
    pos2 = target_file.find(':')
    if pos1 == -1 and pos2 == -1:
        cmd = "cp %s %s" % (source_file, target_file)
    else:
        cmd = "scp %s %s" % (source_file, target_file)
    os.system(cmd)

def get_browser(instance):
    host_name, host_port, zmi_user, zmi_pwd = (instance['host'], instance['port'],
                                              instance['zmi_user'], instance['zmi_pwd'])
    key = '%s:%s' % (host_name, host_port)
    if key not in Browsers:
        br = Browser()
        br.addHeader('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % (zmi_user, zmi_pwd)))
        Browsers[key] = br
    return Browsers[key]
    

def create_ext_method(instance, meth_id, module, function, br):
    host_name, host_port, plone_root = (instance['host'], instance['port'], instance['root'])
    url = 'http://%s:%s/%s/manage_delObjects?ids=%s' % (host_name, host_port, plone_root, meth_id)
    try:
        br.open(url)
    except HTTPError:
        pass
    url = 'http://%s:%s/%s/manage_addProduct/ExternalMethod/methodAdd' % (host_name, host_port, plone_root)
    br.open(url)
    br.getControl(name='id').value = meth_id
    br.getControl(name='module').value = module
    br.getControl(name='function').value = function
    br.getControl(name='submit').click()

def run_ext_method(instance, meth_id, args, out_file, br):
    host_name, host_port, plone_root = (instance['host'], instance['port'], instance['root'])
    url = 'http://%s:%s/%s/%s' % (host_name, host_port, plone_root, meth_id)
    if args:
        url_add = []
        for k,v in args.items():
            url_add.append('%s=%s' % (k, v))
        url_add = '&'.join(url_add)
        url = url + '?' + url_add
    br.open(url)
    fp = open(out_file, "w")
    fp.write(br.contents)
    fp.close()

def del_object(host_name, host_port, plone_root, obj, br):
    pos = obj.rfind('/')
    if pos == -1:
        url = 'http://%s:%s/%s/manage_delObjects?ids=%s' % (host_name, host_port, plone_root, obj)
    else:
        top_obj = obj[:pos]
        obj = obj[pos+1:]
        url = 'http://%s:%s/%s/%s/manage_delObjects?ids=%s' % (host_name, host_port, plone_root, top_obj, obj)
    try:
        br.open(url)
    except HTTPError:
        pass
