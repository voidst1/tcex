# -*- coding: utf-8 -*-
"""Test the TcEx Session Module."""


# pylint: disable=R0201,W0201
class TestUtils:
    """Test the TcEx Session Module."""

    @staticmethod
    def test_session_external(tcex):
        """Test tc.session_external property.

        Args:
            tcex (TcEx, fixture): An instantiated instance of TcEx object.
        """
        r = tcex.session_external.get('https://www.google.com')
        assert tcex.session_external.proxies == {}
        assert r.status_code == 200

    @staticmethod
    def test_session_external_proxy(tcex_proxy_external):
        """Test tc.session_external property with proxy.

        Args:
            tcex (TcEx, fixture): An instantiated instance of TcEx object.
        """
        r = tcex_proxy_external.session_external.get('https://www.google.com', verify=False)
        assert tcex_proxy_external.session_external.proxies is not None
        assert r.status_code == 200
