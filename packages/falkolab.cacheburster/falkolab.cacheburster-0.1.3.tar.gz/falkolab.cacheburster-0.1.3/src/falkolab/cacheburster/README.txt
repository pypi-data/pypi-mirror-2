==================================
Cache Burster for Zope 3/BlueBream
==================================

This package contains the `IVersionedResourceLayer` layer. This layer supports 
a correct set of component registration and can be used for inheritation in 
custom skins.

Testing
-------

For testing the Cache Burster we use the testing skin defined in the tests 
package which uses the `IVersionedResourceLayer` layer as the only base layer.  
This means, that our testing skin provides only the views defined in the minimal 
package and it's testing views defined in tests.

Login as manager first:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.handleErrors = False
  
We have page template file that looks as:
     
  >>> print getTemplateContent('page.pt')
  <html><head>
  <script type="text/javascript" src="script.js"
  tal:attributes="src context/++resource++script.js"></script>
  <BLANKLINE>
  <script type="text/javascript" src="one-module.css"
  tal:attributes="src context/++resource++one-module.css"></script>
  </head>
  <body></body>
  </html> 

We have ``page.html`` view which is registred in the
``ftesting.zcml`` file with our skin for testing purposes:

  >>> browser.open('http://localhost/page.html')
  >>> browser.url
  'http://localhost/page.html'
  
Rendered view:

  >>> print browser.contents
  <html><head>
  <script type="text/javascript"
          src="http://localhost/@@/script.js"></script>
  <BLANKLINE>
  <script type="text/javascript"
          src="http://localhost/@@/one-module.css"></script>
  </head>
  <body></body>
  </html>
  
Nothing has changed, all right. 
  
Cache Burster rule
------------------
 
Now we register Cache Burster rule:

  >>> from zope.configuration import xmlconfig
  >>> import falkolab.cacheburster
  >>> context = xmlconfig.file('meta.zcml', falkolab.cacheburster)
  >>> def zcml(s, context):  
  ...     return xmlconfig.string(s, context)

  >>> context = zcml(r"""
  ...    <configure
  ...        xmlns="http://namespaces.zope.org/browser"
  ...        >
  ...
  ...      <cacheburster 
  ...          from="(script).js" 
  ...          to="\1.{version}.js"
  ...          fileset="tests/testfiles/*.js"
  ...          />
  ...
  ...    </configure>
  ... """, context)
  
OK. Render page again:

  >>> browser.open('http://localhost/page.html')
  >>> print browser.contents
  <html><head>
  <script type="text/javascript"
          src="http://localhost/@@/script.a5d90bae.js"></script>
  <BLANKLINE>
  <script type="text/javascript"
          src="http://localhost/@@/one-module.css"></script>
  </head>
  <body></body>
  </html>
  
The cacheburster directive `from` and `to` fields use python re syntax.
That looks similarly re.sub(from, to, resourcename)
We can specify from="(.*).js". It means that the rule was accepted by all 
resources that end with `.js`.

Test that resource URL is accessible:

  >>> browser.open('http://localhost/@@/script.a5d90bae.js')
  >>> print browser.contents 
  alert('script.js');

Add next rule:

  >>> context = zcml(r"""
  ...    <configure
  ...        xmlns="http://namespaces.zope.org/browser"
  ...        >
  ...
  ...      <cacheburster 
  ...          from="(.*)-module.css"
  ...          to="\1-module.css?{version}"
  ...          manager="md5"
  ...          />
  ...
  ...    </configure>
  ... """, context)
  
Render page again:

  >>> browser.open('http://localhost/page.html')
  >>> print browser.contents
  <html><head>
  <script type="text/javascript"
          src="http://localhost/@@/script.a5d90bae.js"></script>
  <BLANKLINE>
  <script type="text/javascript"
          src="http://localhost/@@/one-module.css?c25661cc824732136e9ec697d97afaed"></script>
  </head>
  <body></body>
  </html>
  
Test that resource URL is accessible:

  >>> browser.open('http://localhost/@@/one-module.css?579d7fcdc5acc3fe9f063020b2f573cf')
  >>> print browser.contents 
  body {background:#ffffff;}  

No-file resource
----------------
  
Register resource and rule:

  >>> import zope.browserresource
  >>> context = xmlconfig.file('meta.zcml', zope.browserresource, context)
  >>> context = zcml(r"""
  ...    <configure
  ...        xmlns="http://namespaces.zope.org/browser"
  ...        >
  ...    <resource 
  ...       name="nofile"
  ...       factory="falkolab.cacheburster.testing.NoFileResourceFactory"
  ...       layer="falkolab.cacheburster.interfaces.IVersionedResourceLayer"
  ...       />
  ...
  ...      <cacheburster 
  ...          from="nofile"
  ...          to="{version}.nofile"
  ...          />
  ...
  ...    </configure>
  ... """, context)
  
  >>> browser.open('http://localhost/page2.html')
  >>> print browser.contents
  <html><head>
  <script type="text/javascript"
          src="http://localhost/@@/fdd9b757.nofile"></script>
  </head>
  <body></body>
  </html>
  
Test that resource URL is accessible:

  >>> browser.open('http://localhost/@@/fdd9b757.nofile')
  >>> print browser.contents 
  no file resource body
  
Resource Directory
------------------

  >>> context = zcml(r"""
  ...    <configure
  ...        xmlns="http://namespaces.zope.org/browser"
  ...        >
  ...    <resourceDirectory 
  ...       name="resources"
  ...       directory="tests/testfiles"
  ...       layer="falkolab.cacheburster.interfaces.IVersionedResourceLayer"
  ...       />
  ...    </configure>
  ... """, context)
  
  >>> browser.open('http://localhost/@@/resources/script.a5d90bae.js')
  >>> print browser.contents 
  alert('script.js');
  
File Version Manager
--------------------

Create and register file manager as `versionfile`:

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()

  >>> pathToVersionFile = os.path.join(temp_dir, 'version.txt')
  >>> open(pathToVersionFile, 'w').write("1")

  >>> from zope.browserresource.interfaces import IResource
  >>> manager = falkolab.cacheburster.version.FileVersionManager(pathToVersionFile)

  >>> zope.component.provideAdapter(manager,
  ...     (zope.browserresource.interfaces.IResource, 
  ...     falkolab.cacheburster.interfaces.IVersionedResourceLayer), 
  ... falkolab.cacheburster.interfaces.IVersionManager, name='versionfile')

Add rule:

  >>> context = zcml(r"""
  ...    <configure
  ...        xmlns="http://namespaces.zope.org/browser"
  ...        >
  ...
  ...      <cacheburster 
  ...          from="(.*).pack" 
  ...          to="\1.{version}"
  ...          fileset="tests/testfiles/*.pack"
  ...          manager="versionfile"
  ...          />
  ...
  ...    </configure>
  ... """, context)

Look at the page:

  >>> print getTemplateContent('page3.pt')
  <html><head>
  <script type="text/javascript" src="any_script.pack"
  tal:attributes="src context/++resource++any_script.pack"></script>
  </head>
  <body></body>
  </html>
    
Render page:

  >>> browser.open('http://localhost/page3.html')
  >>> print browser.contents
  <html><head>
  <script type="text/javascript"
          src="http://localhost/@@/any_script.1"></script>
  </head>
  <body></body>
  </html>
  
Cleanup
-------

  >>> import shutil
  >>> shutil.rmtree(temp_dir)