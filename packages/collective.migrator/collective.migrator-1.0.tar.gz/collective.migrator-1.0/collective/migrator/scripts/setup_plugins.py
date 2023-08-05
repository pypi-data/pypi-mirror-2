from StringIO import StringIO
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
def meth(self):
    out = StringIO()
    activatePluginInterfaces(self, 'source_users')
    activatePluginInterfaces(self, 'source_groups')
    print >> out, 'Done'
    return out.getvalue()
