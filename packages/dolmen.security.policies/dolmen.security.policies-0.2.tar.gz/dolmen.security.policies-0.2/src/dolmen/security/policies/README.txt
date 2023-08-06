========================
dolmen.security.policies
========================

``dolmen.security.policies`` provides a pluggable way to handle
object-level security.

  >>> from zope.location import Location
  >>> from zope.interface import implements
  >>> from zope.annotation.interfaces import IAttributeAnnotatable

  >>> class Content(Location):
  ...     implements(IAttributeAnnotatable)
  ...     def __init__(self, parent, name):
  ...         self.__parent__ = parent
  ...         self.__name__ = name

  >>> class MyFolder(Location):
  ...     implements(IAttributeAnnotatable)
  ...     def __init__(self):
  ...         self.contents = {}

  >>> folder = MyFolder()
  >>> contentA = folder.contents['a'] = Content(folder, 'a')


Roles
=====

Standard behavior
-----------------

Out of the box settings
~~~~~~~~~~~~~~~~~~~~~~~

  >>> from zope.securitypolicy.zopepolicy import settingsForObject
  >>> pprint(settingsForObject(contentA))
  [('a',
    {'principalPermissions': [], 'principalRoles': [], 'rolePermissions': []}),
   (None,
    {'principalPermissions': [], 'principalRoles': [], 'rolePermissions': []}),
   ('global settings',
    {'principalPermissions': [{'permission': 'zope.View',
			       'principal': 'zope.test',
			       'setting': PermissionSetting: Allow}],
     'principalRoles': [],
     'rolePermissions': [{'permission': 'zope.ManageContent',
			  'role': 'test.role',
			  'setting': PermissionSetting: Allow}]})]


Assign a role to the test user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  >>> from zope.securitypolicy.interfaces import IPrincipalRoleManager
  >>> manager = IPrincipalRoleManager(folder)
  >>> manager.assignRoleToPrincipal('test.role', 'zope.test')


Test the role application
~~~~~~~~~~~~~~~~~~~~~~~~~

  >>> from zope.securitypolicy.interfaces import IPrincipalRoleMap
  >>> folder_rpm = IPrincipalRoleMap(folder)
  >>> print folder_rpm.getRolesForPrincipal('zope.test')
  [('test.role', PermissionSetting: Allow)]

  
Role inheritence
~~~~~~~~~~~~~~~~

  >>> pprint(settingsForObject(contentA))
  [('a',
    {'principalPermissions': [], 'principalRoles': [], 'rolePermissions': []}),
   (None,
    {'principalPermissions': [],
     'principalRoles': [{'principal': 'zope.test',
			 'role': 'test.role',
			 'setting': PermissionSetting: Allow}],
     'rolePermissions': []}),
   ('global settings',
    {'principalPermissions': [{'permission': 'zope.View',
			       'principal': 'zope.test',
			       'setting': PermissionSetting: Allow}],
     'principalRoles': [],
     'rolePermissions': [{'permission': 'zope.ManageContent',
			  'role': 'test.role',
			  'setting': PermissionSetting: Allow}]})]


Additive behavior
-----------------

  >>> import grokcore.component as grok
  >>> from grokcore.component.testing import grok_component
  >>> from zope.securitypolicy.interfaces import Allow
  >>> from zope.securitypolicy.securitymap import SecurityMap
  >>> from dolmen.security.policies.principalrole import ExtraRoleMap
  >>> from zope.securitypolicy.interfaces import IPrincipalRoleManager

  >>> class MyHomefolder(Location):
  ...     implements(IAttributeAnnotatable)
  ...     def __init__(self, id):
  ...        self.__name__ = "%s homepage" % id
  ...        self.userid = id

  >>> home = MyHomefolder('zope.test')
  >>> pprint(settingsForObject(home)[0])
  ('zope.test homepage',
     {'principalPermissions': [], 'principalRoles': [], 'rolePermissions': []})

  >>> class HomepageRoleManager(ExtraRoleMap):
  ...    grok.context(MyHomefolder)
  ...
  ...    def _compute_extra_data(self):
  ...        extra_map = SecurityMap()
  ...        extra_map.addCell('test.role', self.context.userid, Allow)
  ...        return extra_map

  >>> from zope.component import provideAdapter
  >>> from zope.securitypolicy.interfaces import (
  ...      IPrincipalRoleManager, IPrincipalRoleMap, IRolePermissionMap)

  >>> provideAdapter(
  ...     HomepageRoleManager, (MyHomefolder,), IPrincipalRoleManager)
  >>> provideAdapter(
  ...     HomepageRoleManager, (MyHomefolder,), IPrincipalRoleMap)

  >>> pprint(settingsForObject(home)[0])
  ('zope.test homepage',
   {'principalPermissions': [],
    'principalRoles': [{'principal': 'zope.test',
                        'role': 'test.role',
                        'setting': PermissionSetting: Allow}],
    'rolePermissions': []})


Checking the permissions::

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction
  >>> newInteraction(Participation(Principal('zope.test')))

  >>> from zope.security import checkPermission
  >>> checkPermission('zope.ManageContent', home)
  True

  >>> home.userid = "someone else"
  >>> checkPermission('zope.ManageContent', home)
  False

  >>> endInteraction()
