A test layer for running JavaScript test jobs on a TestSwarm instance
=====================================================================

This uses plone.app.testing.layers.PLONE_ZSERVER as a base to start a plone instance. The test job can be configured either from buildout or overridden with shell environment variables. After the job is scheduled the plone instance runs until the timeout is reached. Results are not yet collected from the TestSwarm instance.


How to configure your project to use collective.testswarm
---------------------------------------------------------

First you will need to set up a testswarm instance: https://github.com/jquery/testswarm

Add a user (e.g. tsuser) and find out the auth key for that user (mysql: select auth from users where name = "tsuser";). This is the user account that your tests can use for adding test jobs. Use these details in the buildout section described below or pass them as environment variables (uppercase) to the test runner::

  $ TS_USER=myuser ./bin/test

your.product/setup.py::

  extras_require={
      'test': 'collective.testswarm'
      }

buildout.cfg::

  [test]
  recipe = zc.recipe.testrunner
  eggs = your.product [test]
  environment = testswarm-instance

  [testswarm-instance]
  ts_url = http://testswarm
  ts_user = tsuser
  ts_auth = asdf1234asdf #select auth from users where name = "tsuser";
  ts_job_name = Test collective.testswarm
  ts_urls = http://localhost:55555/plone/example-qunit-suite
  ts_suites = QUnit example
  ts_browsers = popularbeta
  ts_max_jobs = 1
  ZSERVER_HOST = 55555
  ZSERVER_PORT = localhost

How to use the collective.testswarm layer
-----------------------------------------

your.product/your/product/tests/layers.py::

  from plone.app.testing import PloneSandboxLayer

  from collective.testswarm.layers import TESTSWARM_LAYER

  class YourProductLayer(PloneSandboxLayer):
      defaultBases = (TESTSWARM_LAYER, )

      def setUpPloneSite(self, portal):
          self.applyProfile(portal, 'your.product:testswarm')

  YOURPRODUCT_LAYER = YourProductLayer()

your.product/your/product/tests/test_swarm.py::

  import unittest2 as unittest

  from layers import YOURPRODUCT_LAYER


  class TestSwarmTestCase(unittest.TestCase):
      layer = YOURPRODUCT_LAYER

      def test_your_product_swarm(self):
          """ You need one test for the testrunner to sniff out
          """






