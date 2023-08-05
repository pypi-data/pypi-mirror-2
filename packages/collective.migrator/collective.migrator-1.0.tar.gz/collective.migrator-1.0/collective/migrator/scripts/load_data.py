from StringIO import StringIO
def meth(self):
    out = StringIO()
    mtool = self.portal_membership
    dtool = self.portal_memberdata
    props = dtool.propertyIds()
    fp = open('%s/Extensions/memberdata.txt' % INSTANCE_HOME)
    last_id = ''
    last_props = {}
    for line in fp:
        mem_id, prop, val = line.strip().split(',', 2)
        if mem_id != last_id:
            if last_id:
                mem = mtool.getMemberById(last_id)
                if not mem:
                    print >> out, 'mem %s does not exist' % last_id
                    continue
                if last_props:
                    mem.setMemberProperties(last_props)
                    last_props = {}
            last_id = mem_id
        val = val.replace('\\n', '\n')
        if val.startswith('(') and val.endswith(')'):
            val = eval(val)
        last_props[prop] = val
    print >> out, 'Done'
    return out.getvalue()

def load_siteprops(self):
    out = StringIO()
    ptool = self.portal_properties.site_properties
    fp = open('%s/Extensions/siteprops.txt' % INSTANCE_HOME)
    prop_vals = {}
    for line in fp:
        prop, prop_type, val = line.strip().split(', ', 2)
        old_val = ptool.getProperty(prop)
        if prop_type in ('int', 'lines', 'boolean'):
            val = eval(val)
        elif prop_type != 'string':
            print >> out, 'Unknown type %s' % prop_type
            continue
        if val != old_val:
            prop_vals[prop] = val
            print >> out, 'Changed %s from %s to %s' % (prop, old_val, val)
    ptool.manage_changeProperties(prop_vals)
    print >> out, 'Done'
    return out.getvalue()
