import unittest

from repoze.what import predicates 
from repoze.what.plugins.ip import ip_from


# From repoze.what tests
class BasePredicateTester(unittest.TestCase):
    """Base test class for predicates."""

    def eval_met_predicate(self, p, environ):
        """Evaluate a predicate that should be met"""
        self.assertEqual(p.check_authorization(environ), None)
        self.assertEqual(p.is_met(environ), True)

    def eval_unmet_predicate(self, p, environ, expected_error):
        """Evaluate a predicate that should not be met"""
        credentials = environ.get('repoze.what.credentials')
        # Testing check_authorization
        try:
            p.evaluate(environ, credentials)
            self.fail('Predicate must not be met; expected error: %s' %
                      expected_error)
        except predicates.NotAuthorizedError, error:
            self.assertEqual(unicode(error), expected_error)
        # Testing is_met:
        self.assertEqual(p.is_met(environ), False)

    def _make_environ(self, params=None):
        """Make a WSGI enviroment with the credentials dict"""
        environ = {
            'REQUEST_METHOD': 'GET',
            'repoze.who.identity': {
                #'repoze.who.userid': None
            },
            'repoze.what.credentials': {
                #'repoze.what.userid': None
            }
        }
        if params:
            environ.update(params)
        return environ


class TestIpFrom(BasePredicateTester):
    r"""Tests for ip_from predicate"""

    def test_without_credentials(self):
        r"""Test how ip_from behaves without credentials"""
        env = self._make_environ()
        p = ip_from()
        self.eval_unmet_predicate(p, env, 'Access denied for this IP')

    def test_with_credentials(self):
        r"""Test how ip_from handles IP addresses"""
        env = self._make_environ({
            'REMOTE_ADDR': '127.0.0.1'
        })
        p = ip_from(allowed='127.0.0.1')
        self.eval_met_predicate(p, env)
        # The extracted IP is placed in repoze identity
        self.assertEqual(env['repoze.who.identity']['ip'], '127.0.0.1')
        # No proxy found
        self.assertFalse('proxy' in env['repoze.who.identity'])

        env = self._make_environ({
            'REMOTE_ADDR': '127.0.0.2'
        })
        p = ip_from(allowed='127.0.0.1')
        self.eval_unmet_predicate(p, env, 'Access denied for this IP')
        # No valid IP found - no IP in the environment
        self.assertFalse('ip' in env['repoze.who.identity'])
        self.assertFalse('proxy' in env['repoze.who.identity'])

        # If we did not ask for proxies, we won't accept them even if we trust
        # them
        env = self._make_environ({
            'REMOTE_ADDR': '192.168.1.5',
            'HTTP_X_FORWARDED_FOR': '4.2.2.1',
        })
        p = ip_from(allowed=['4.2.2.1', '192.168.1.5'])
        self.eval_unmet_predicate(p, env, 'Access through proxies denied')

        # But as soon as we accept proxies all is good again
        env = self._make_environ({
            'REMOTE_ADDR': '192.168.1.5',
            'HTTP_X_FORWARDED_FOR': '4.2.2.1',
        })
        # The plugin should create the identity itself
        del env['repoze.who.identity']
        p = ip_from(allowed=['4.2.2.1', '192.168.1.5'], proxies=True)
        self.eval_met_predicate(p, env)
        self.assertEqual(env['repoze.who.identity']['ip'], '4.2.2.1')
        self.assertEqual(env['repoze.who.identity']['proxy'], '192.168.1.5')

        # The proxies are verified if provided
        env = self._make_environ({
            'REMOTE_ADDR': '192.168.1.5',
            'HTTP_X_FORWARDED_FOR': '4.2.2.1',
        })
        p = ip_from(allowed=['4.2.2.1'], proxies=['192.168.1.5'])
        self.eval_met_predicate(p, env)
        p = ip_from(allowed=['4.2.2.1'], proxies=['192.168.1.1'])
        self.eval_unmet_predicate(p, env, 'Access denied through this proxy')

        # And the IPs behind proxies too
        env = self._make_environ({
            'REMOTE_ADDR': '192.168.1.5',
            'HTTP_X_FORWARDED_FOR': '4.2.2.1',
        })
        p = ip_from(allowed=['4.2.2.1'], proxies=['192.168.1.5'])
        self.eval_met_predicate(p, env)
        p = ip_from(allowed=['4.2.2.2'], proxies=['192.168.1.5'])
        self.eval_unmet_predicate(p, env, 'Access denied for this IP')

        # Now check that bad IPs are silently ignored and all the errors caught.
        # And no permission for them, of course
        env = self._make_environ({
            'REMOTE_ADDR': 'not_an_ip',
            'HTTP_X_FORWARDED_FOR': 3.14,
        })
        p = ip_from(allowed=["what's up?"], proxies=['hidden'])
        self.eval_unmet_predicate(p, env, 'Access denied for this IP')

        env = self._make_environ({
            'REMOTE_ADDR': '1.1.1.1',
            'HTTP_X_FORWARDED_FOR': 3.14,
        })
        p = ip_from(allowed=['1.1.1.1'], proxies=['hidden'])
        self.eval_unmet_predicate(p, env, 'Access denied for this IP')

