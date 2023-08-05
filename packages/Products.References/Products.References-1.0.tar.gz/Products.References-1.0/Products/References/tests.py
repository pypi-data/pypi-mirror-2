from unittest import TestSuite, makeSuite

from Testing.ZopeTestCase import installProduct, ZopeTestCase

installProduct('PythonScripts')
installProduct('References')

class Tests(ZopeTestCase):
  def afterSetUp(self):
    app = self.app
    app.manage_addFolder('rf') # folder for references
    rf = self.rf = app.rf
    app.manage_addFolder('tf') # folder for targets
    self.tf = app.tf
    self.tf.attr = 'attr'
    rf.manage_addProduct['References'].manage_addReference('r', 'reference', '../tf')
    self.r = rf.r

  def test_target(self):
    self.assertEqual(self.r.getTarget().getId(), 'tf')

  def test_attribute_access_and_traversal(self):
    tf = self.tf
    tf.manage_addDTMLMethod('index_html')
    r = self.r
    # reference resolution
    self.assertEqual(r.title, 'reference')
    self.assertEqual(r.restrictedTraverse('title'), 'reference')
    # target resolution
    self.assertEqual(r.index_html.aq_inner.aq_parent.getId(), 'tf')
    self.assertEqual(r.restrictedTraverse('index_html').aq_inner.aq_parent.getId(),
                     'tf'
                     )

  def test_tales_path_expressions(self):
    from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
    pt = ZopePageTemplate('pt', '<tal:content content="context/r/attr"/>').__of__(self.rf)
    self.assertEqual(pt().strip(), 'attr')

  def test_aq_parent(self):
    # correct context and container for PythonScripts (and friends)
    tf = self.tf
    tf.manage_addProduct['PythonScripts'].manage_addPythonScript('tps')
    tps=tf.tps; tps.write('return context, container\n')
    rf = self.rf
    rf.manage_addProduct['References'].manage_addReference('rps','','../tf/tps')
    context, container = rf.rps()
    self.assertEqual(context.getId(), 'rf')
    self.assertEqual(container.getId(), 'tf')
    # correct parent for methods called
    def check_parent(self): return self.aq_parent
    tf.__class__.check_parent = check_parent
    self.assertEqual(self.r.check_parent().getId(), 'rf')

  def test_classmethod(self):
    tf = self.tf
    def clm(cls_): return cls_.__name__
    tf.__class__.clm = classmethod(clm)
    self.assertEqual(self.r.clm(), 'Folder')

def test_suite():
  return TestSuite(map(makeSuite,
    (Tests,)
                       ))



