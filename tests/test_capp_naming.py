#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import logging

from coshed_model.naming import cfapp_base_url

ENV_DATA = {
    "CONTAINER_APP_ENV_DNS_SUFFIX": "lustylepi-ffffffff.westeurope.azurecontainerapps.io",
    "ENV_NAME": "dev",
    "ENV_DOMAIN_PROD": "promiscuouspadawan-00000000.westeurope.azurecontainerapps.io",
    "ENV_DOMAIN_DEV": "dominatingdressellian-11111111.westeurope.azurecontainerapps.io",
    "ENV_DOMAIN_QA": "quackyquarren-22222222.westeurope.azurecontainerapps.io",

}

class TestBaseURLs(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger(__name__)

    def setUp(self):
        for key, val in ENV_DATA.items():
            os.environ[key] = val

    @classmethod
    def tearDownClass(cls):
        for key in ENV_DATA.keys():
            try:
                del os.environ[key]
            except KeyError:
                pass

    def test_old_gods(self):
        for key in ENV_DATA.keys():
            try:
                del os.environ[key]
            except KeyError:
                pass

        self.assertEqual("https://crap.cfapps.eu10.hana.ondemand.com", cfapp_base_url("crap"))
        self.assertEqual("https://crap.cfapps.eu10.hana.ondemand.com", cfapp_base_url("crap", env_name="prod"))
        self.assertEqual("https://crap-dev.cfapps.eu10.hana.ondemand.com", cfapp_base_url("crap", env_name="dev"))
        self.assertEqual("https://crap-qa.cfapps.eu10.hana.ondemand.com", cfapp_base_url("crap", env_name="qa"))
        self.assertEqual("https://dev-crap.cfapps.eu10.hana.ondemand.com", cfapp_base_url("crap", env_name="dev", prefixed=True))

    def test__same_env(self):
        env_name = ENV_DATA["ENV_NAME"]
        app_name = "something"
        expectation = f"https://{app_name}.{ENV_DATA['CONTAINER_APP_ENV_DNS_SUFFIX']}"
        result = cfapp_base_url(app_name, env_name=env_name)
        self.assertEqual(expectation, result)

    def test__no_env_name(self):
        app_name = "something"
        expectation = f"https://{app_name}.{ENV_DATA['CONTAINER_APP_ENV_DNS_SUFFIX']}"
        result = cfapp_base_url(app_name)
        self.assertEqual(expectation, result)

    def test__qa_env_name(self):
        app_name = "something"
        expectation = f"https://{app_name}.{ENV_DATA['ENV_DOMAIN_QA']}"
        result = cfapp_base_url(app_name, env_name="qa")
        self.assertEqual(expectation, result)

    def test__qa_env_name_scheme_http(self):
        app_name = "something"
        expectation = f"http://{app_name}.{ENV_DATA['ENV_DOMAIN_QA']}"
        result = cfapp_base_url(app_name, env_name="qa", scheme="http")
        self.assertEqual(expectation, result)

    def test__qa_env_name_scheme_http_want_fqdn_false(self):
        app_name = "something"
        expectation = f"http://{app_name}"
        result = cfapp_base_url(app_name, env_name="qa", scheme="http", want_fqdn=False)
        self.assertEqual(expectation, result)

    def test__prod_env_name(self):
        app_name = "something"
        expectation = f"https://{app_name}.{ENV_DATA['ENV_DOMAIN_PROD']}"
        result = cfapp_base_url(app_name, env_name="prod")
        self.assertEqual(expectation, result)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    unittest.main()
