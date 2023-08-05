from StringIO import StringIO
def dump_memberdata(self):
    out = StringIO()
    mtool = self.portal_membership
    dtool = self.portal_memberdata
    props = dtool.propertyIds()
    defaults = {}
    defaults['listed'] = ('1', 'True', 'on')
    defaults['login_time'] = ('2000/01/01',)
    defaults['last_login_time'] = ('2000/01/01',)
    defaults['wysiwyg_editor'] = ('Kupu',)
    defaults['error_log_update'] = ('0.0',)
    defaults['must_change_password'] = ('0', 'False')
    defaults['visible_ids'] = ('0', 'False')
    defaults['ext_editor'] = ('0', 'False')
    defaults['news_subscribed'] = ('0', 'False')
    defaults['user_categories'] = ('()', "('',)")

    for mem_id in mtool.listMemberIds():
        mem = mtool.getMemberById(mem_id)
        for prop in props:
            val = str(mem.getProperty(prop))
            if val == '':
                continue
            if prop in defaults.keys() and val in defaults[prop]:
                continue
            val = val.replace('\n', '\\n')
            print >> out, "%s,%s,%s" % (mem_id, prop, val)
    return out.getvalue()

def dump_siteprops(self):
    out = StringIO()
    ptool = self.portal_properties.site_properties
    props = ptool.propertyIds()
    for p in props:
        print >> out, "%s, %s, %s" % (p, ptool.getPropertyType(p), ptool.getProperty(p))
    return out.getvalue()
