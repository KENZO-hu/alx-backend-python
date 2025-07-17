#!/usr/bin/env python3
"""Unit tests for utils.py module
"""

import unittest 
import unittest.mock as mock
from parameterized import parameterized
from client import GithubOrgClient
import fixtures import org_payload, repos_payload,expected_repos,apache2_repos
from parameterized import parameterized_class
import requests

# create a test class for GithubOrgClient
class TestGithubOrgClient(unittest.TestCase):
    """unit test for GithubOrgClient """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name,mock_get_json):
        """test Githuborgclient.org returns correct data get_json is mocked """
        # return the value 
        mock_reponse = {"login": org_name, "id":123}
        mock_get_json.return_value = mock_reponse

        # Instantiate the GithubOrgClient
        client = GithubOrgClient(org_name)
        result = client.org
        #check  that get_json was called exactly once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # verify the result
        self.assertEqual(result, mock_reponse)
    @parameterized.expand([
        ({"license":{"key":"my_license"},"my_license",True})
        ({"license":{"key":"other_license"},"my_license",False}),
    ])
    def test_has_license(self, repo, license_key, expected):
        """test that has_license returns true or false correctly"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)      
     @parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and setup fixture-based responses"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Mocking `.json()` return values based on URL
        def side_effect(url):
            mock_resp = MagicMock()
            if url == GithubOrgClient.ORG_URL.format("test_org"):
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters by license"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)       
        def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters by license 'apache-2.0'"""
        client = GithubOrgClient("test_org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
