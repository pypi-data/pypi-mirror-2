# This file is part of the MapProxy project.
# Copyright (C) 2010 Omniscale <http://omniscale.de>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement
from mapproxy.core.client import HTTPClient, HTTPClientError
from mapproxy.core.client import TMSClient, TileClient, TileURLTemplate
from mapproxy.wms.client import WMSClient
from mapproxy.wms.request import wms_request, WMS111MapRequest, WMS100MapRequest,\
                                 WMS130MapRequest
from mapproxy.core.srs import bbox_equals
from mapproxy.core.request import Request, url_decode
from mapproxy.core.config import base_config
from mapproxy.tests.http import mock_httpd, query_eq, make_wsgi_env
from mapproxy.tests.helper import assert_re, TempFiles

from nose.tools import eq_
from nose.plugins.skip import SkipTest

TESTSERVER_ADDRESS = ('127.0.0.1', 56413)
TESTSERVER_URL = 'http://%s:%s' % TESTSERVER_ADDRESS

class TestHTTPClient(object):
    def setup(self):
        self.client = HTTPClient()
    def test_internal_error_response(self):
        try:
            with mock_httpd(TESTSERVER_ADDRESS, [({'path': '/'},
                                                  {'status': '500', 'body': ''})]):
                self.client.open(TESTSERVER_URL + '/')
        except HTTPClientError, e:
            assert_re(e.args[0], r'HTTP Error \(.*\): 500')
        else:
            assert False, 'expected HTTPClientError'
    def test_invalid_url_type(self):
        try:
            self.client.open('htp://example.org')
        except HTTPClientError, e:
            assert_re(e.args[0], r'No response .* \(htp://example.*\): unknown url type')
        else:
            assert False, 'expected HTTPClientError'
    def test_invalid_url(self):
        try:
            self.client.open('this is not a url')
        except HTTPClientError, e:
            assert_re(e.args[0], r'URL not correct \(this is not.*\): unknown url type')
        else:
            assert False, 'expected HTTPClientError'
    def test_unknown_host(self):
        try:
            self.client.open('http://thishostshouldnotexist000136really42.org')
        except HTTPClientError, e:
            assert_re(e.args[0], r'No response .* \(http://thishost.*\): .*')
        else:
            assert False, 'expected HTTPClientError'
    def test_no_connect(self):
        try:
            self.client.open('http://localhost:53871')
        except HTTPClientError, e:
            assert_re(e.args[0], r'No response .* \(http://localhost.*\): Connection refused')
        else:
            assert False, 'expected HTTPClientError'
    def test_internal_error(self):
        try:
            self.client.open('http://localhost:53871', invalid_key='argument')
        except HTTPClientError, e:
            assert_re(e.args[0], r'Internal HTTP error \(http://localhost.*\): TypeError')
        else:
            assert False, 'expected HTTPClientError'

    
    def test_https_no_ssl_module_error(self):
        from mapproxy.core import client
        old_ssl = client.ssl
        try:
            client.ssl = None
            try:
                self.client = HTTPClient('https://trac.osgeo.org/')
            except ImportError:
                pass
            else:
                assert False, 'no ImportError for missing ssl module'
        finally:
            client.ssl = old_ssl
    
    def test_https_no_ssl_module_insecure(self):
        from mapproxy.core import client
        old_ssl = client.ssl
        try:
            client.ssl = None
            base_config().http.ssl.insecure = True
            self.client = HTTPClient('https://trac.osgeo.org/')
            self.client.open('https://trac.osgeo.org/')
        finally:
            client.ssl = old_ssl
            base_config().http.ssl.insecure = False
    
    def test_https_valid_cert(self):
        try:
            import ssl
        except ImportError:
            raise SkipTest()
        
        with TempFiles(1) as tmp:
            with open(tmp[0], 'w') as f:
                f.write(OSGEO_CERT)
            base_config().http.ssl.ca_certs = tmp[0]
            self.client = HTTPClient('https://trac.osgeo.org/')
            self.client.open('https://trac.osgeo.org/')
    
    def test_https_invalid_cert(self):
        try:
            import ssl
        except ImportError:
            raise SkipTest()
        
        with TempFiles(1) as tmp:
            base_config().http.ssl.ca_certs = tmp[0]
            self.client = HTTPClient('https://trac.osgeo.org/')
            try:
                self.client.open('https://trac.osgeo.org/')
            except HTTPClientError, e:
                assert_re(e.args[0], r'Could not verify connection to URL')
        
OSGEO_CERT = """
-----BEGIN CERTIFICATE-----
MIIE2DCCBEGgAwIBAgIEN0rSQzANBgkqhkiG9w0BAQUFADCBwzELMAkGA1UEBhMC
VVMxFDASBgNVBAoTC0VudHJ1c3QubmV0MTswOQYDVQQLEzJ3d3cuZW50cnVzdC5u
ZXQvQ1BTIGluY29ycC4gYnkgcmVmLiAobGltaXRzIGxpYWIuKTElMCMGA1UECxMc
KGMpIDE5OTkgRW50cnVzdC5uZXQgTGltaXRlZDE6MDgGA1UEAxMxRW50cnVzdC5u
ZXQgU2VjdXJlIFNlcnZlciBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTAeFw05OTA1
MjUxNjA5NDBaFw0xOTA1MjUxNjM5NDBaMIHDMQswCQYDVQQGEwJVUzEUMBIGA1UE
ChMLRW50cnVzdC5uZXQxOzA5BgNVBAsTMnd3dy5lbnRydXN0Lm5ldC9DUFMgaW5j
b3JwLiBieSByZWYuIChsaW1pdHMgbGlhYi4pMSUwIwYDVQQLExwoYykgMTk5OSBF
bnRydXN0Lm5ldCBMaW1pdGVkMTowOAYDVQQDEzFFbnRydXN0Lm5ldCBTZWN1cmUg
U2VydmVyIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MIGdMA0GCSqGSIb3DQEBAQUA
A4GLADCBhwKBgQDNKIM0VBuJ8w+vN5Ex/68xYMmo6LIQaO2f55M28Qpku0f1BBc/
I0dNxScZgSYMVHINiC3ZH5oSn7yzcdOAGT9HZnuMNSjSuQrfJNqc1lB5gXpa0zf3
wkrYKZImZNHkmGw6AIr1NJtl+O3jEP/9uElY3KDegjlrgbEWGWG5VLbmQwIBA6OC
AdcwggHTMBEGCWCGSAGG+EIBAQQEAwIABzCCARkGA1UdHwSCARAwggEMMIHeoIHb
oIHYpIHVMIHSMQswCQYDVQQGEwJVUzEUMBIGA1UEChMLRW50cnVzdC5uZXQxOzA5
BgNVBAsTMnd3dy5lbnRydXN0Lm5ldC9DUFMgaW5jb3JwLiBieSByZWYuIChsaW1p
dHMgbGlhYi4pMSUwIwYDVQQLExwoYykgMTk5OSBFbnRydXN0Lm5ldCBMaW1pdGVk
MTowOAYDVQQDEzFFbnRydXN0Lm5ldCBTZWN1cmUgU2VydmVyIENlcnRpZmljYXRp
b24gQXV0aG9yaXR5MQ0wCwYDVQQDEwRDUkwxMCmgJ6AlhiNodHRwOi8vd3d3LmVu
dHJ1c3QubmV0L0NSTC9uZXQxLmNybDArBgNVHRAEJDAigA8xOTk5MDUyNTE2MDk0
MFqBDzIwMTkwNTI1MTYwOTQwWjALBgNVHQ8EBAMCAQYwHwYDVR0jBBgwFoAU8Bdi
E1U9s/8KAGv7UISX8+1i0BowHQYDVR0OBBYEFPAXYhNVPbP/CgBr+1CEl/PtYtAa
MAwGA1UdEwQFMAMBAf8wGQYJKoZIhvZ9B0EABAwwChsEVjQuMAMCBJAwDQYJKoZI
hvcNAQEFBQADgYEAkNwwAvpkdMKnCqV8IY00F6j7Rw7/JXyNEwr75Ji174z4xRAN
95K+8cPV1ZVqBLssziY2ZcgxxufuP+NXdYR6Ee9GTxj005i7qIcyunL2POI9n9cd
2cNgQ4xYDiKWL2KjLB+6rQXvqzJ4h6BUcxm1XAX5Uj5tLUUL9wqT6u0G+bI=
-----END CERTIFICATE-----

"""

class TestWMSClient(object):
    def setup(self):
        self.req = WMS111MapRequest(url=TESTSERVER_URL + '/service?map=foo')
        self.wms = WMSClient(self.req)
    def test_request(self):
        expected_req = ({'path': r'/service?map=foo&LAYERS=foo&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetMap&HEIGHT=256&SRS=EPSG%3A4326'
                                  '&VERSION=1.1.1&BBOX=-180.0,-90.0,180.0,90.0&WIDTH=512&STYLES='},
                        {'body': 'no image', 'headers': {'content-type': 'image/png'}})
        with mock_httpd(TESTSERVER_ADDRESS, [expected_req]):
            req = WMS111MapRequest(url=TESTSERVER_URL + '/service?map=foo',
                                   param={'layers': 'foo', 'bbox': '-180.0,-90.0,180.0,90.0'})
            req.params.size = (512, 256)
            req.params['format'] = 'image/png'
            req.params['srs'] = 'EPSG:4326'
            resp = self.wms.get_map(req)
    
    def test_request_w_auth(self):
        wms = WMSClient(self.req, http_client=HTTPClient(self.req.url, username='foo', password='bar'))
        def assert_auth(req_handler):
            assert 'Authorization' in req_handler.headers
            auth_data = req_handler.headers['Authorization'].split()[1]
            auth_data = auth_data.decode('base64')
            eq_(auth_data, 'foo:bar')
            return True
        expected_req = ({'path': r'/service?map=foo&LAYERS=foo&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetMap&HEIGHT=256&SRS=EPSG%3A4326'
                                  '&VERSION=1.1.1&BBOX=-180.0,-90.0,180.0,90.0&WIDTH=512&STYLES=',
                         'require_basic_auth': True,
                         'req_assert_function': assert_auth},
                        {'body': 'no image', 'headers': {'content-type': 'image/png'}})
        with mock_httpd(TESTSERVER_ADDRESS, [expected_req]):
            req = WMS111MapRequest(url=TESTSERVER_URL + '/service?map=foo',
                                   param={'layers': 'foo', 'bbox': '-180.0,-90.0,180.0,90.0'})
            req.params.size = (512, 256)
            req.params['format'] = 'image/png'
            req.params['srs'] = 'EPSG:4326'
            resp = wms.get_map(req)

    def test_get_tile_non_image_content_type(self):
        expected_req = ({'path': r'/service?map=foo&LAYERS=foo&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetMap&HEIGHT=256&SRS=EPSG%3A4326&STYLES='
                                  '&VERSION=1.1.1&BBOX=-180.0,-90.0,180.0,90.0&WIDTH=512'},
                        {'body': 'error', 'headers': {'content-type': 'text/plain'}})
        with mock_httpd(TESTSERVER_ADDRESS, [expected_req]):
            try:
                req = WMS111MapRequest(url=TESTSERVER_URL + '/service?map=foo',
                                       param={'layers': 'foo', 'bbox': '-180.0,-90.0,180.0,90.0'})
                req.params.size = (512, 256)
                req.params['format'] = 'image/png'
                req.params['srs'] = 'EPSG:4326'
                resp = self.wms.get_map(req)
            except HTTPClientError, e:
                assert_re(e.args[0], r'response is not an image')
            else:
                assert False, 'expected HTTPClientError'
    
    def test__transform_fi_request(self):
        default_req = WMS111MapRequest(url_decode('srs=EPSG%3A4326'))
        fi_req = Request(make_wsgi_env('''LAYERS=mapserver_cache&
         QUERY_LAYERS=mapnik_mapserver&X=601&Y=528&FORMAT=image%2Fpng&SERVICE=WMS&
         VERSION=1.1.1&REQUEST=GetFeatureInfo&STYLES=&
         EXCEPTIONS=application%2Fvnd.ogc.se_inimage&SRS=EPSG%3A900913&
         BBOX=730930.9303206909,6866851.379301955,1031481.3254841676,7170153.507483206&
         WIDTH=983&HEIGHT=992'''.replace('\n', '').replace(' ', '')))
        wms_client = WMSClient(default_req)
        orig_req = wms_request(fi_req)
        req = wms_request(fi_req)
        wms_client._transform_fi_request(req)
        
        eq_(req.params.srs, 'EPSG:4326')
        eq_(req.params.pos, (601, 523))

        default_req = WMS111MapRequest(url_decode('srs=EPSG%3A900913'))
        wms_client = WMSClient(default_req)
        wms_client._transform_fi_request(req)
        
        eq_(req.params.srs, 'EPSG:900913')
        eq_(req.params.pos, (601, 528))
        assert bbox_equals(orig_req.params.bbox, req.params.bbox, 0.1)
        
class TestTMSClient(object):
    def setup(self):
        self.client = TMSClient(TESTSERVER_URL)
    def test_get_tile(self):
        with mock_httpd(TESTSERVER_ADDRESS, [({'path': '/9/5/13.png'},
                                                {'body': 'tile', 'headers': {'content-type': 'image/png'}})]):
            resp = self.client.get_tile((5, 13, 9)).read()
            eq_(resp, 'tile')

class TestTileClient(object):
    def test_tc_path(self):
        template = TileURLTemplate(TESTSERVER_URL + '/%(tc_path)s.png')
        client = TileClient(template)
        with mock_httpd(TESTSERVER_ADDRESS, [({'path': '/09/000/000/005/000/000/013.png'},
                                              {'body': 'tile',
                                               'headers': {'content-type': 'image/png'}})]):
            resp = client.get_tile((5, 13, 9)).read()
            eq_(resp, 'tile')

    def test_quadkey(self):
        template = TileURLTemplate(TESTSERVER_URL + '/key=%(quadkey)s&format=%(format)s')
        client = TileClient(template)
        with mock_httpd(TESTSERVER_ADDRESS, [({'path': '/key=000002303&format=png'},
                                              {'body': 'tile',
                                               'headers': {'content-type': 'image/png'}})]):
            resp = client.get_tile((5, 13, 9)).read()
            eq_(resp, 'tile')
    def test_xyz(self):
        template = TileURLTemplate(TESTSERVER_URL + '/x=%(x)s&y=%(y)s&z=%(z)s&format=%(format)s')
        client = TileClient(template)
        with mock_httpd(TESTSERVER_ADDRESS, [({'path': '/x=5&y=13&z=9&format=png'},
                                              {'body': 'tile',
                                               'headers': {'content-type': 'image/png'}})]):
            resp = client.get_tile((5, 13, 9)).read()
            eq_(resp, 'tile')

class TestWMSMapRequest100(object):
    def setup(self):
        self.r = WMS100MapRequest(param=dict(layers='foo', version='1.1.1', request='GetMap'))
        self.r.params = self.r.adapt_params_to_version()
    def test_version(self):
        eq_(self.r.params['WMTVER'], '1.0.0')
        assert 'VERSION' not in self.r.params
    def test_service(self):
        assert 'SERVICE' not in self.r.params 
    def test_request(self):
        eq_(self.r.params['request'], 'map')
    def test_str(self):
        eq_(str(self.r.params), 'layers=foo&styles=&request=map&wmtver=1.0.0')

class TestWMSMapRequest130(object):
    def setup(self):
        self.r = WMS130MapRequest(param=dict(layers='foo', WMTVER='1.0.0'))
        self.r.params = self.r.adapt_params_to_version()
    def test_version(self):
        eq_(self.r.params['version'], '1.3.0')
        assert 'WMTVER' not in self.r.params
    def test_service(self):
        eq_(self.r.params['service'], 'WMS' )
    def test_request(self):
        eq_(self.r.params['request'], 'GetMap')
    def test_str(self):
        query_eq(str(self.r.params), 'layers=foo&styles=&service=WMS&request=GetMap&version=1.3.0')

class TestWMSMapRequest111(object):
    def setup(self):
        self.r = WMS111MapRequest(param=dict(layers='foo', WMTVER='1.0.0'))
        self.r.params = self.r.adapt_params_to_version()
    def test_version(self):
        eq_(self.r.params['version'], '1.1.1')
        assert 'WMTVER' not in self.r.params