"""
When a view's update() method redirects somewhere else, the template
is not executed subsequently.

  >>> grok.testing.grok(__name__)

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope.component import getMultiAdapter
  >>> view = getMultiAdapter((manfred, request), name='cavepainting')
  >>> print view()
  None
  >>> print request.response.getStatus()
  302
  >>> print request.response.getHeader('Location')
  somewhere-else

"""
import grokcore.view as grok

class Mammoth(grok.Context):
    pass

class CavePainting(grok.View):
    def update(self):
        self.request.response.redirect('somewhere-else')


cavepainting = grok.PageTemplate("""\
<html>
<body>
<h1 tal:content="this-is-an-error" />
</body>
</html>
""")
