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

from __future__ import with_statement, division
import os
import re
import sys
from mapproxy.platform.image import Image
import functools

from cStringIO import StringIO
from webtest import TestApp
import mapproxy.config
from mapproxy.srs import SRS
from mapproxy.wsgiapp import make_wsgi_app 
from mapproxy.request.wms import WMS100MapRequest, WMS111MapRequest, WMS130MapRequest, \
                                 WMS111FeatureInfoRequest, WMS111CapabilitiesRequest, \
                                 WMS130CapabilitiesRequest, WMS100CapabilitiesRequest, \
                                 WMS100FeatureInfoRequest, WMS130FeatureInfoRequest, \
                                 wms_request
from mapproxy.test.unit.test_grid import assert_almost_equal_bbox
from mapproxy.test.image import is_jpeg, is_png, tmp_image
from mapproxy.test.http import mock_httpd
from mapproxy.test.helper import validate_with_dtd, validate_with_xsd
from nose.tools import eq_, assert_almost_equal

global_app = None

def setup_module():
    fixture_dir = os.path.join(os.path.dirname(__file__), 'fixture')
    fixture_layer_conf = os.path.join(fixture_dir, 'layer.yaml')
    fixture_cache_data = os.path.join(fixture_dir, 'cache_data')
    mapproxy.config.base_config().debug_mode = True
    mapproxy.config.base_config().services_conf = fixture_layer_conf
    mapproxy.config.base_config().cache.base_dir = fixture_cache_data
    mapproxy.config.base_config().image.paletted = False
    mapproxy.config._service_config = None
    
    global global_app
    global_app = TestApp(make_wsgi_app(fixture_layer_conf), use_unicode=False)

def teardown_module():
    mapproxy.config._config = None
    mapproxy.config._service_config = None

def test_invalid_url():
    global_app.get('/invalid?fop', status=404)

class WMSTest(object):
    def setup(self):
        self.app = global_app
        self.created_tiles = []
    
    def created_tiles_filenames(self):
        base_dir = mapproxy.config.base_config().cache.base_dir
        for filename in self.created_tiles:
            yield os.path.join(base_dir, filename)
    
    def _test_created_tiles(self):
        for filename in self.created_tiles_filenames():
            if not os.path.exists(filename):
                assert False, "didn't found tile " + filename
    
    def teardown(self):
        self._test_created_tiles()
        for filename in self.created_tiles_filenames():
            if os.path.exists(filename):
                os.remove(filename)


def is_100_capa(xml):
    return validate_with_dtd(xml, dtd_name='wms/1.0.0/capabilities_1_0_0.dtd')

def is_111_exception(xml, msg=None, code=None, re_msg=None):
    eq_(xml.xpath('/ServiceExceptionReport/@version')[0], '1.1.1')
    if msg:
        eq_(xml.xpath('//ServiceException/text()')[0], msg)
    if re_msg:
        exception_msg = xml.xpath('//ServiceException/text()')[0]
        assert re.match(re_msg, exception_msg, re.I), "'%r' does not match '%s'" % (
            re_msg, exception_msg)
    if code is not None:
        eq_(xml.xpath('/ServiceExceptionReport/ServiceException/@code')[0], code)
    assert validate_with_dtd(xml, 'wms/1.1.1/exception_1_1_1.dtd')
    
def is_111_capa(xml):
    return validate_with_dtd(xml, dtd_name='wms/1.1.1/WMS_MS_Capabilities.dtd')
def is_130_capa(xml):
    return validate_with_xsd(xml, xsd_name='wms/1.3.0/capabilities_1_3_0.xsd')

class TestWMSVersionDispatch(object):
    def setup(self):
        self.app = global_app
        
    def test_unknown_version_110(self):
        resp = self.app.get('http://localhost/service?SERVICE=WMS&REQUEST=GetCapabilities'
                            '&VERSION=1.1.0')
        assert is_100_capa(resp.lxml)
    def test_unknown_version_113(self):
        resp = self.app.get('http://localhost/service?SERVICE=WMS&REQUEST=GetCapabilities'
                            '&VERSION=1.1.3')
        assert is_111_capa(resp.lxml)
    def test_unknown_version_090(self):
        resp = self.app.get('http://localhost/service?SERVICE=WMS&REQUEST=GetCapabilities'
                            '&WMTVER=0.9.0')
        assert is_100_capa(resp.lxml)
    def test_unknown_version_200(self):
        resp = self.app.get('http://localhost/service?SERVICE=WMS&REQUEST=GetCapabilities'
                            '&VERSION=2.0.0')
        assert is_130_capa(resp.lxml)

class TestWMS111(WMSTest):
    def setup(self):
        WMSTest.setup(self)
        self.common_req = WMS111MapRequest(url='/service?', param=dict(service='WMS', 
             version='1.1.1'))
        self.common_map_req = WMS111MapRequest(url='/service?', param=dict(service='WMS', 
             version='1.1.1', bbox='-180,0,0,80', width='200', height='200',
             layers='wms_cache', srs='EPSG:4326', format='image/png',
             styles='', request='GetMap'))
        self.common_fi_req = WMS111FeatureInfoRequest(url='/service?',
            param=dict(x='10', y='20', width='200', height='200', layers='wms_cache',
                       format='image/png', query_layers='wms_cache', styles='',
                       bbox='1000,400,2000,1400', srs='EPSG:900913'))
    
    def test_invalid_request_type(self):
        req = str(self.common_map_req).replace('GetMap', 'invalid')
        resp = self.app.get(req)
        is_111_exception(resp.lxml, "unknown WMS request type 'invalid'")
        
    def test_wms_capabilities(self):
        req = WMS111CapabilitiesRequest(url='/service?').copy_with_request_params(self.common_req)
        resp = self.app.get(req)
        eq_(resp.content_type, 'application/vnd.ogc.wms_xml')
        xml = resp.lxml
        eq_(xml.xpath('//GetMap//OnlineResource/@xlink:href',
                      namespaces=dict(xlink="http://www.w3.org/1999/xlink"))[0],
            'http://localhost:80/service?')
        layer_names = set(xml.xpath('//Layer/Layer/Name/text()'))
        expected_names = set(['direct', 'wms_cache', 'wms_cache_100', 'wms_cache_130',
                              'wms_merge', 'tms_cache', 'wms_cache_multi',
                              'wms_cache_link_single'])
        eq_(layer_names, expected_names)
        assert validate_with_dtd(xml, dtd_name='wms/1.1.1/WMS_MS_Capabilities.dtd')
    
    def test_invalid_layer(self):
        self.common_map_req.params['layers'] = 'invalid'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'application/vnd.ogc.se_xml')
        is_111_exception(resp.lxml, 'unknown layer: invalid', 'LayerNotDefined')
    
    def test_invalid_format(self):
        self.common_map_req.params['format'] = 'image/ascii'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'application/vnd.ogc.se_xml')
        is_111_exception(resp.lxml, 'unsupported image format: image/ascii', 
                         'InvalidFormat')
    
    def test_invalid_format_img_exception(self):
        self.common_map_req.params['format'] = 'image/ascii'
        self.common_map_req.params['exceptions'] = 'application/vnd.ogc.se_inimage'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'image/png')
        assert is_png(StringIO(resp.body))
    
    def test_missing_format_img_exception(self):
        del self.common_map_req.params['format']
        self.common_map_req.params['exceptions'] = 'application/vnd.ogc.se_inimage'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'image/png')
        assert is_png(StringIO(resp.body))
    
    def test_invalid_srs(self):
        self.common_map_req.params['srs'] = 'EPSG:1234'
        resp = self.app.get(self.common_map_req)
        is_111_exception(resp.lxml, 'unsupported srs: EPSG:1234', 'InvalidSRS')
    
    def test_get_map_png(self):
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/png'
        data = StringIO(resp.body)
        assert is_png(data)
        assert Image.open(data).mode == 'RGB'
        
    def test_get_map_png_transparent(self):
        self.common_map_req.params['transparent'] = 'True'
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/png'
        data = StringIO(resp.body)
        assert is_png(data)
        assert Image.open(data).mode == 'RGBA'
    
    def test_get_map_jpeg(self):
        self.common_map_req.params['format'] = 'image/jpeg'
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/jpeg'
        assert is_jpeg(StringIO(resp.body))
    
    def test_get_map_xml_exception(self):
        self.common_map_req.params['bbox'] = '0,0,90,90'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'application/vnd.ogc.se_xml')
        xml = resp.lxml
        eq_(xml.xpath('/ServiceExceptionReport/ServiceException/@code'), [])
        assert 'No response from URL' in xml.xpath('//ServiceException/text()')[0]
        assert validate_with_dtd(xml, 'wms/1.1.1/exception_1_1_1.dtd')
    
    def test_direct_layer_error(self):
        self.common_map_req.params['layers'] = 'direct'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'application/vnd.ogc.se_xml')
        xml = resp.lxml
        eq_(xml.xpath('/ServiceExceptionReport/ServiceException/@code'), [])
        # TODO hide error
        # assert 'unable to get map for layers: direct' in \
        #     xml.xpath('//ServiceException/text()')[0]
        assert 'No response from URL' in \
             xml.xpath('//ServiceException/text()')[0]
        
        assert validate_with_dtd(xml, 'wms/1.1.1/exception_1_1_1.dtd')
    
    def test_get_map(self):
        self.created_tiles.append('wms_cache_EPSG900913/01/000/000/001/000/000/001.jpeg')
        with tmp_image((256, 256), format='jpeg') as img:
            expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fjpeg'
                                      '&REQUEST=GetMap&HEIGHT=256&SRS=EPSG%3A900913&styles='
                                      '&VERSION=1.1.1&BBOX=0.0,0.0,20037508.3428,20037508.3428'
                                      '&WIDTH=256'},
                            {'body': img.read(), 'headers': {'content-type': 'image/jpeg'}})
            with mock_httpd(('localhost', 42423), [expected_req]):
                self.common_map_req.params['bbox'] = '0,0,180,90'
                resp = self.app.get(self.common_map_req)
                assert 35000 < int(resp.headers['Content-length']) < 75000
                eq_(resp.content_type, 'image/png')
    
    def test_get_map_use_direct(self):
        with tmp_image((200, 200), format='png') as img:
            expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                      '&REQUEST=GetMap&HEIGHT=200&SRS=EPSG%3A4326&styles='
                                      '&VERSION=1.1.1&BBOX=5.0,-10.0,6.0,-9.0'
                                      '&WIDTH=200'},
                            {'body': img.read(), 'headers': {'content-type': 'image/png'}})
            with mock_httpd(('localhost', 42423), [expected_req]):
                self.common_map_req.params['bbox'] = '5,-10,6,-9'
                resp = self.app.get(self.common_map_req)
                img.seek(0)
                assert resp.body == img.read()
                is_png(img)
                eq_(resp.content_type, 'image/png')
        
    def test_get_map_use_direct_with_transform(self):
        bbox_900913 = [1110868.98971,6444038.14317,1229263.18538,6623564.86585]
        with tmp_image((200, 200), format='png') as img:
            expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                      '&REQUEST=GetMap&HEIGHT=303&SRS=EPSG%3A900913&styles='
                                      '&VERSION=1.1.1&BBOX=1110868.98971,6444038.14317,1229263.18538,6623564.86585'
                                      '&WIDTH=200'},
                            {'body': img.read(), 'headers': {'content-type': 'image/png'}})
            with mock_httpd(('localhost', 42423), [expected_req]):
                self.common_map_req.params['bbox'] = '3570269,5540889,3643458,5653553'
                self.common_map_req.params['srs'] = 'EPSG:31467'
                resp = self.app.get(self.common_map_req)
                img.seek(0)
                assert resp.body != img.read()
                is_png(img)
                eq_(resp.content_type, 'image/png')
    
    def test_get_map_invalid_bbox(self):
        # min x larger than max x
        url =  """/service?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&BBOX=7,2,-9,10&SRS=EPSG:4326&WIDTH=164&HEIGHT=388&LAYERS=wms_cache&STYLES=&FORMAT=image/png&TRANSPARENT=TRUE"""
        resp = self.app.get(url)
        is_111_exception(resp.lxml, 'invalid bbox 7,2,-9,10')
    
    def test_get_map_invalid_bbox2(self):
        # broken bbox for the requested srs
        url =  """/service?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&BBOX=-72988843.697212,-255661507.634227,142741550.188860,255661507.634227&SRS=EPSG:25833&WIDTH=164&HEIGHT=388&LAYERS=wms_cache_100&STYLES=&FORMAT=image/png&TRANSPARENT=TRUE"""
        resp = self.app.get(url)
        is_111_exception(resp.lxml, 'Request too large or invalid BBOX.')
    
    def test_get_map_broken_bbox(self):
        url = """/service?VERSION=1.1.11&REQUEST=GetMap&SRS=EPSG:31467&BBOX=-10000855.0573254,2847125.18913603,-9329367.42767611,4239924.78564583&WIDTH=130&HEIGHT=62&LAYERS=wms_cache&STYLES=&FORMAT=image/png&TRANSPARENT=TRUE"""
        resp = self.app.get(url)
        is_111_exception(resp.lxml, 'Could not transform BBOX: Invalid result.')
        
    def test_get_map100(self):
        self.created_tiles.append('wms_cache_100_EPSG900913/01/000/000/001/000/000/001.jpeg')
        # request_format tiff, cache format jpeg, wms request in png
        with tmp_image((256, 256), format='tiff') as img:
            expected_req = ({'path': r'/service?LAYERs=foo,bar&FORMAT=image%2Ftiff'
                                      '&REQUEST=map&HEIGHT=256&SRS=EPSG%3A900913&styles='
                                      '&WMTVER=1.0.0&BBOX=0.0,0.0,20037508.3428,20037508.3428'
                                      '&WIDTH=256'},
                            {'body': img.read(), 'headers': {'content-type': 'image/tiff'}})
            with mock_httpd(('localhost', 42423), [expected_req]):
                self.common_map_req.params['bbox'] = '0,0,180,90'
                self.common_map_req.params['layers'] = 'wms_cache_100'
                resp = self.app.get(self.common_map_req)
                eq_(resp.content_type, 'image/png')
    
    def test_get_map130(self):
        self.created_tiles.append('wms_cache_130_EPSG900913/01/000/000/001/000/000/001.jpeg')
        with tmp_image((256, 256), format='jpeg') as img:
            expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fjpeg'
                                      '&REQUEST=GetMap&HEIGHT=256&CRS=EPSG%3A900913&styles='
                                      '&VERSION=1.3.0&BBOX=0.0,0.0,20037508.3428,20037508.3428'
                                      '&WIDTH=256'},
                            {'body': img.read(), 'headers': {'content-type': 'image/jgeg'}})
            with mock_httpd(('localhost', 42423), [expected_req]):
                self.common_map_req.params['bbox'] = '0,0,180,90'
                self.common_map_req.params['layers'] = 'wms_cache_130'
                resp = self.app.get(self.common_map_req)
                eq_(resp.content_type, 'image/png')
    
    def test_get_map130_axis_order(self):
        self.created_tiles.append('wms_cache_multi_EPSG4326/02/000/000/003/000/000/001.jpeg')
        with tmp_image((256, 256), format='jpeg') as img:
            img = img.read()
            expected_reqs = [({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fjpeg'
                                      '&REQUEST=GetMap&HEIGHT=256&CRS=EPSG%3A4326&styles='
                                      '&VERSION=1.3.0&BBOX=0.0,90.0,90.0,180.0'
                                      '&WIDTH=256'},
                            {'body': img, 'headers': {'content-type': 'image/jgeg'}}),]
            with mock_httpd(('localhost', 42423), expected_reqs):
                self.common_map_req.params['bbox'] = '90,0,180,90'
                self.common_map_req.params['layers'] = 'wms_cache_multi'
                resp = self.app.get(self.common_map_req)
                eq_(resp.content_type, 'image/png')
    
    def test_get_featureinfo(self):
        expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetFeatureInfo&HEIGHT=200&SRS=EPSG%3A900913'
                                  '&VERSION=1.1.1&BBOX=1000.0,400.0,2000.0,1400.0&styles='
                                  '&WIDTH=200&QUERY_LAYERS=foo,bar&X=10&Y=20'},
                        {'body': 'info', 'headers': {'content-type': 'text/plain'}})
        with mock_httpd(('localhost', 42423), [expected_req]):
            resp = self.app.get(self.common_fi_req)
            print resp.body
            eq_(resp.content_type, 'text/plain')
            eq_(resp.body, 'info')

    def test_get_featureinfo_transformed(self):
        expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetFeatureInfo&HEIGHT=200&SRS=EPSG%3A900913'
                                  '&BBOX=1110868.98971,6444038.14317,1229263.18538,6623564.86585'
                                  '&styles=&VERSION=1.1.1'
                                  '&WIDTH=200&QUERY_LAYERS=foo,bar&X=10&Y=22'},
                        {'body': 'info', 'headers': {'content-type': 'text/plain'}})
        
        # out fi point at x=10,y=20
        p_31467  = (3570269+10*(3643458 - 3570269)/200, 5540889+20*(5653553 - 5540889)/200)
        # the transformed fi point at x=10,y=22
        p_900913 = (1110868.98971+10*(1229263.18538 - 1110868.98971)/200,
                    6444038.14317+22*(6623564.86585 - 6444038.14317)/200)
        # are they the same?
        assert_almost_equal(SRS(31467).transform_to(SRS(900913), p_31467)[0], p_900913[0], -2)
        assert_almost_equal(SRS(31467).transform_to(SRS(900913), p_31467)[1], p_900913[1], -2)
        
        with mock_httpd(('localhost', 42423), [expected_req]):
            self.common_fi_req.params['bbox'] = '3570269,5540889,3643458,5653553'
            self.common_fi_req.params['srs'] = 'EPSG:31467'
            resp = self.app.get(self.common_fi_req)
            print resp.body
            eq_(resp.content_type, 'text/plain')
            eq_(resp.body, 'info')

    def test_get_featureinfo_info_format(self):
        expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetFeatureInfo&HEIGHT=200&SRS=EPSG%3A900913'
                                  '&VERSION=1.1.1&BBOX=1000.0,400.0,2000.0,1400.0&styles='
                                  '&WIDTH=200&QUERY_LAYERS=foo,bar&X=10&Y=20'
                                  '&info_format=text%2Fhtml'},
                        {'body': 'info', 'headers': {'content-type': 'text/html'}})
        with mock_httpd(('localhost', 42423), [expected_req]):
            self.common_fi_req.params['info_format'] = 'text/html'
            resp = self.app.get(self.common_fi_req)
            eq_(resp.content_type, 'text/html')
            eq_(resp.body, 'info')
    
    def test_get_featureinfo_130(self):
        expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetFeatureInfo&HEIGHT=200&CRS=EPSG%3A900913'
                                  '&VERSION=1.3.0&BBOX=1000.0,400.0,2000.0,1400.0&styles='
                                  '&WIDTH=200&QUERY_LAYERS=foo,bar&I=10&J=20'},
                        {'body': 'info', 'headers': {'content-type': 'text/plain'}})
        with mock_httpd(('localhost', 42423), [expected_req]):
            self.common_fi_req.params['layers'] = 'wms_cache_130'
            self.common_fi_req.params['query_layers'] = 'wms_cache_130'
            resp = self.app.get(self.common_fi_req)
            eq_(resp.content_type, 'text/plain')
            eq_(resp.body, 'info')
        
    def test_get_featureinfo_missing_params(self):
        expected_req = (
            {'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                      '&REQUEST=GetFeatureInfo&HEIGHT=200&SRS=EPSG%3A900913'
                      '&VERSION=1.1.1&BBOX=1000.0,400.0,2000.0,1400.0&styles='
                      '&WIDTH=200&QUERY_LAYERS=foo,bar&X=10&Y=20'},
            {'body': 'info', 'headers': {'content-type': 'text/plain'}})
        with mock_httpd(('localhost', 42423), [expected_req]):
            del self.common_fi_req.params['format']
            del self.common_fi_req.params['styles']
            resp = self.app.get(self.common_fi_req)
            eq_(resp.content_type, 'text/plain')
            eq_(resp.body, 'info')
    
    def test_get_featureinfo_missing_params_strict(self):
        request_parser = self.app.app.handlers['service'].request_parser
        try:
            self.app.app.handlers['service'].request_parser = \
                functools.partial(wms_request, strict=True)
        
            del self.common_fi_req.params['format']
            del self.common_fi_req.params['styles']
            resp = self.app.get(self.common_fi_req)
            xml = resp.lxml
            assert 'missing parameters' in xml.xpath('//ServiceException/text()')[0]
            assert validate_with_dtd(xml, 'wms/1.1.1/exception_1_1_1.dtd')
        finally:
            self.app.app.handlers['service'].request_parser = request_parser
    
    def test_get_featureinfo_not_queryable(self):
        self.common_fi_req.params['query_layers'] = 'tms_cache'
        self.common_fi_req.params['exceptions'] = 'application/vnd.ogc.se_xml'
        resp = self.app.get(self.common_fi_req)
        print resp.body
        eq_(resp.content_type, 'application/vnd.ogc.se_xml')
        xml = resp.lxml
        eq_(xml.xpath('/ServiceExceptionReport/ServiceException/@code'), [])
        assert 'tms_cache is not queryable' in xml.xpath('//ServiceException/text()')[0]
        assert validate_with_dtd(xml, 'wms/1.1.1/exception_1_1_1.dtd')

class TestWMS100(WMSTest):
    def setup(self):
        WMSTest.setup(self)
        self.common_req = WMS100MapRequest(url='/service?', param=dict(wmtver='1.0.0'))
        self.common_map_req = WMS100MapRequest(url='/service?', param=dict(wmtver='1.0.0',
            bbox='-180,0,0,80', width='200', height='200',
            layers='wms_cache', srs='EPSG:4326', format='image/png',
            styles='', request='GetMap'))
        self.common_fi_req = WMS100FeatureInfoRequest(url='/service?',
            param=dict(x='10', y='20', width='200', height='200', layers='wms_cache_100',
                       format='image/png', query_layers='wms_cache_100', styles='',
                       bbox='1000,400,2000,1400', srs='EPSG:900913'))
        
    def test_wms_capabilities(self):
        req = WMS100CapabilitiesRequest(url='/service?').copy_with_request_params(self.common_req)
        resp = self.app.get(req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_(xml.xpath('/WMT_MS_Capabilities/Service/Title/text()')[0],
            'MapProxy test fixture')
        layer_names = set(xml.xpath('//Layer/Layer/Name/text()'))
        expected_names = set(['direct', 'wms_cache', 'wms_cache_100', 'wms_cache_130',
                              'wms_merge', 'tms_cache', 'wms_cache_multi',
                              'wms_cache_link_single'])
        eq_(layer_names, expected_names)
        #TODO srs
        assert validate_with_dtd(xml, dtd_name='wms/1.0.0/capabilities_1_0_0.dtd')
        
    
    def test_invalid_layer(self):
        self.common_map_req.params['layers'] = 'invalid'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_(xml.xpath('/WMTException/@version')[0], '1.0.0')
        eq_(xml.xpath('//WMTException/text()')[0].strip(), 'unknown layer: invalid')
    
    def test_invalid_format(self):
        self.common_map_req.params['format'] = 'image/ascii'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_(xml.xpath('/WMTException/@version')[0], '1.0.0')
        eq_(xml.xpath('//WMTException/text()')[0].strip(),
                      'unsupported image format: image/ascii')
    
    def test_invalid_format_img_exception(self):
        self.common_map_req.params['format'] = 'image/ascii'
        self.common_map_req.params['exceptions'] = 'INIMAGE'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'image/png')
        assert is_png(StringIO(resp.body))
    
    def test_missing_format_img_exception(self):
        del self.common_map_req.params['format']
        self.common_map_req.params['exceptions'] = 'INIMAGE'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'image/png')
        assert is_png(StringIO(resp.body))
    
    def test_invalid_srs(self):
        self.common_map_req.params['srs'] = 'EPSG:1234'
        print self.common_map_req.complete_url
        resp = self.app.get(self.common_map_req.complete_url)
        xml = resp.lxml
        eq_(xml.xpath('//WMTException/text()')[0].strip(), 'unsupported srs: EPSG:1234')
    
    def test_get_map_png(self):
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/png'
        data = StringIO(resp.body)
        assert is_png(data)
        eq_(Image.open(data).mode, 'RGB')
        
    def test_get_map_png_transparent_paletted(self):
        try:
            mapproxy.config.base_config().image.paletted = True
            self.common_map_req.params['transparent'] = 'True'
            resp = self.app.get(self.common_map_req)
            resp.content_type = 'image/png'
            data = StringIO(resp.body)
            assert is_png(data)
            assert Image.open(data).mode == 'P'
        finally:
            mapproxy.config.base_config().image.paletted = False
            
    def test_get_map_png_transparent(self):
        self.common_map_req.params['transparent'] = 'True'
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/png'
        data = StringIO(resp.body)
        assert is_png(data)
        assert Image.open(data).mode == 'RGBA'
    
    def test_get_map_jpeg(self):
        self.common_map_req.params['format'] = 'image/jpeg'
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/jpeg'
        assert is_jpeg(StringIO(resp.body))
    
    def test_get_map_xml_exception(self):
         self.common_map_req.params['bbox'] = '0,0,90,90'
         resp = self.app.get(self.common_map_req)
         xml = resp.lxml
         assert 'No response from URL' in xml.xpath('//WMTException/text()')[0]
    
    def test_get_map(self):
        self.created_tiles.append('wms_cache_EPSG900913/01/000/000/001/000/000/001.jpeg')
        with tmp_image((256, 256), format='jpeg') as img:
            expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fjpeg'
                                      '&REQUEST=GetMap&HEIGHT=256&SRS=EPSG%3A900913&styles='
                                      '&VERSION=1.1.1&BBOX=0.0,0.0,20037508.3428,20037508.3428'
                                      '&WIDTH=256'},
                            {'body': img.read(), 'headers': {'content-type': 'image/jgeg'}})
            with mock_httpd(('localhost', 42423), [expected_req]):
                self.common_map_req.params['bbox'] = '0,0,180,90'
                resp = self.app.get(self.common_map_req)
                eq_(resp.content_type, 'image/png')
    
    def test_get_featureinfo(self):
        expected_req = ({'path': r'/service?LAYERs=foo,bar&FORMAT=image%2Fpng'
                                  '&REQUEST=feature_info&HEIGHT=200&SRS=EPSG%3A900913'
                                  '&WMTVER=1.0.0&BBOX=1000.0,400.0,2000.0,1400.0&styles='
                                  '&WIDTH=200&QUERY_LAYERS=foo,bar&X=10&Y=20'},
                        {'body': 'info', 'headers': {'content-type': 'text/plain'}})
        with mock_httpd(('localhost', 42423), [expected_req]):
            resp = self.app.get(self.common_fi_req)
            eq_(resp.content_type, 'text/plain')
            eq_(resp.body, 'info')
    
    def test_get_featureinfo_not_queryable(self):
        self.common_fi_req.params['query_layers'] = 'tms_cache'
        self.common_fi_req.params['exceptions'] = 'application/vnd.ogc.se_xml'
        resp = self.app.get(self.common_fi_req)
        print resp.body
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        assert 'tms_cache is not queryable' in xml.xpath('//WMTException/text()')[0]

ns130 = {'wms': 'http://www.opengis.net/wms',
         'ogc': 'http://www.opengis.net/ogc'}

def eq_xpath(xml, xpath, expected, namespaces=None):
    eq_(xml.xpath(xpath, namespaces=namespaces)[0], expected)

eq_xpath_wms130 = functools.partial(eq_xpath, namespaces=ns130)

class TestWMS130(WMSTest):
    def setup(self):
        WMSTest.setup(self)
        self.common_req = WMS130MapRequest(url='/service?', param=dict(service='WMS', 
             version='1.3.0'))
        self.common_map_req = WMS130MapRequest(url='/service?', param=dict(service='WMS', 
             version='1.3.0', bbox='0,-180,80,0', width='200', height='200',
             layers='wms_cache', crs='EPSG:4326', format='image/png',
             styles='', request='GetMap'))
        self.common_fi_req = WMS130FeatureInfoRequest(url='/service?',
            param=dict(i='10', j='20', width='200', height='200', layers='wms_cache_130',
                       format='image/png', query_layers='wms_cache_130', styles='',
                       bbox='1000,400,2000,1400', crs='EPSG:900913'))
        
    def test_wms_capabilities(self):
        req = WMS130CapabilitiesRequest(url='/service?').copy_with_request_params(self.common_req)
        resp = self.app.get(req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_xpath_wms130(xml, '/wms:WMS_Capabilities/wms:Service/wms:Title/text()',
                        'MapProxy test fixture')
        layer_names = set(xml.xpath('//wms:Layer/wms:Layer/wms:Name/text()',
                                    namespaces=ns130))
        expected_names = set(['direct', 'wms_cache', 'wms_cache_100', 'wms_cache_130',
                              'wms_merge', 'tms_cache', 'wms_cache_multi',
                              'wms_cache_link_single'])
        eq_(layer_names, expected_names)
        assert is_130_capa(xml)
    
    def test_invalid_layer(self):
        self.common_map_req.params['layers'] = 'invalid'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_xpath_wms130(xml, '/ogc:ServiceExceptionReport/@version', '1.3.0')
        eq_xpath_wms130(xml, '/ogc:ServiceExceptionReport/ogc:ServiceException/@code',
            'LayerNotDefined')
        eq_xpath_wms130(xml, '//ogc:ServiceException/text()', 'unknown layer: invalid')
        assert validate_with_xsd(xml, xsd_name='wms/1.3.0/exceptions_1_3_0.xsd')
    
    def test_invalid_format(self):
        self.common_map_req.params['format'] = 'image/ascii'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_xpath_wms130(xml, '/ogc:ServiceExceptionReport/@version', '1.3.0')
        eq_xpath_wms130(xml, '/ogc:ServiceExceptionReport/ogc:ServiceException/@code',
            'InvalidFormat')
        eq_xpath_wms130(xml, '//ogc:ServiceException/text()', 'unsupported image format: image/ascii')
        assert validate_with_xsd(xml, xsd_name='wms/1.3.0/exceptions_1_3_0.xsd')
    
    def test_invalid_format_img_exception(self):
        self.common_map_req.params['format'] = 'image/ascii'
        self.common_map_req.params['exceptions'] = 'application/vnd.ogc.se_inimage'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'image/png')
        assert is_png(StringIO(resp.body))
    
    def test_missing_format_img_exception(self):
        del self.common_map_req.params['format']
        self.common_map_req.params['exceptions'] = 'application/vnd.ogc.se_inimage'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'image/png')
        assert is_png(StringIO(resp.body))
    
    def test_invalid_srs(self):
        self.common_map_req.params['srs'] = 'EPSG:1234'
        self.common_map_req.params['exceptions'] = 'text/xml'
        
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_xpath_wms130(xml, '/ogc:ServiceExceptionReport/ogc:ServiceException/@code',
            'InvalidCRS')
        eq_xpath_wms130(xml, '//ogc:ServiceException/text()', 'unsupported crs: EPSG:1234')
        assert validate_with_xsd(xml, xsd_name='wms/1.3.0/exceptions_1_3_0.xsd')
    
    def test_get_map_png(self):
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/png'
        data = StringIO(resp.body)
        assert is_png(data)
        assert Image.open(data).mode == 'RGB'
        
    def test_get_map_png_transparent(self):
        self.common_map_req.params['transparent'] = 'True'
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/png'
        data = StringIO(resp.body)
        assert is_png(data)
        assert Image.open(data).mode == 'RGBA'
    
    def test_get_map_jpeg(self):
        self.common_map_req.params['format'] = 'image/jpeg'
        resp = self.app.get(self.common_map_req)
        resp.content_type = 'image/jpeg'
        assert is_jpeg(StringIO(resp.body))
    
    def test_get_map_xml_exception(self):
        self.common_map_req.params['bbox'] = '0,0,90,90'
        resp = self.app.get(self.common_map_req)
        eq_(resp.content_type, 'text/xml')
        xml = resp.lxml
        eq_(xml.xpath('/ogc:ServiceExceptionReport/ogc:ServiceException/@code', namespaces=ns130), [])
        assert ('No response from URL' in
            xml.xpath('//ogc:ServiceException/text()', namespaces=ns130)[0])
        assert validate_with_xsd(xml, xsd_name='wms/1.3.0/exceptions_1_3_0.xsd')
    
    def test_get_map(self):
        self.created_tiles.append('wms_cache_EPSG900913/01/000/000/001/000/000/001.jpeg')
        with tmp_image((256, 256), format='jpeg') as img:
            expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fjpeg'
                                      '&REQUEST=GetMap&HEIGHT=256&SRS=EPSG%3A900913&styles='
                                      '&VERSION=1.1.1&BBOX=0.0,0.0,20037508.3428,20037508.3428'
                                      '&WIDTH=256'},
                            {'body': img.read(), 'headers': {'content-type': 'image/jgeg'}})
            with mock_httpd(('localhost', 42423), [expected_req]):
                self.common_map_req.params['bbox'] = '0,0,180,90' #internal axis-order
                resp = self.app.get(self.common_map_req)
                eq_(resp.content_type, 'image/png')
    
    def test_get_featureinfo(self):
        expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetFeatureInfo&HEIGHT=200&CRS=EPSG%3A900913'
                                  '&VERSION=1.3.0&BBOX=1000.0,400.0,2000.0,1400.0&styles='
                                  '&WIDTH=200&QUERY_LAYERS=foo,bar&I=10&J=20'},
                        {'body': 'info', 'headers': {'content-type': 'text/plain'}})
        with mock_httpd(('localhost', 42423), [expected_req]):
            resp = self.app.get(self.common_fi_req)
            eq_(resp.content_type, 'text/plain')
            eq_(resp.body, 'info')

    def test_get_featureinfo_111(self):
        expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                  '&REQUEST=GetFeatureInfo&HEIGHT=200&SRS=EPSG%3A900913'
                                  '&VERSION=1.1.1&BBOX=1000.0,400.0,2000.0,1400.0&styles='
                                  '&WIDTH=200&QUERY_LAYERS=foo,bar&X=10&Y=20'},
                        {'body': 'info', 'headers': {'content-type': 'text/plain'}})
        with mock_httpd(('localhost', 42423), [expected_req]):
            self.common_fi_req.params['layers'] = 'wms_cache'
            self.common_fi_req.params['query_layers'] = 'wms_cache'
            resp = self.app.get(self.common_fi_req)
            eq_(resp.content_type, 'text/plain')
            eq_(resp.body, 'info')

if sys.platform != 'win32':
    class TestWMSLinkSingleColorImages(WMSTest):
        def setup(self):
            WMSTest.setup(self)
            self.common_map_req = WMS111MapRequest(url='/service?', param=dict(service='WMS', 
                 version='1.1.1', bbox='-180,0,0,80', width='200', height='200',
                 layers='wms_cache_link_single', srs='EPSG:4326', format='image/jpeg',
                 styles='', request='GetMap'))
    
        def test_get_map(self):
            link_name = 'wms_cache_link_single_EPSG900913/01/000/000/001/000/000/001.png'
            real_name = 'wms_cache_link_single_EPSG900913/single_color_tiles/fe0005.png'
            self.created_tiles.append(link_name)
            self.created_tiles.append(real_name)
            with tmp_image((256, 256), format='png', color='#fe0005') as img:
                expected_req = ({'path': r'/service?LAYERs=foo,bar&SERVICE=WMS&FORMAT=image%2Fpng'
                                          '&REQUEST=GetMap&HEIGHT=256&SRS=EPSG%3A900913&styles='
                                          '&VERSION=1.1.1&BBOX=0.0,0.0,20037508.3428,20037508.3428'
                                          '&WIDTH=256'},
                                {'body': img.read(), 'headers': {'content-type': 'image/png'}})
                with mock_httpd(('localhost', 42423), [expected_req]):
                    self.common_map_req.params['bbox'] = '0,0,180,90'
                    resp = self.app.get(self.common_map_req)
                    eq_(resp.content_type, 'image/jpeg')
            
                base_dir = mapproxy.config.base_config().cache.base_dir
                single_loc = os.path.join(base_dir, real_name)
                tile_loc = os.path.join(base_dir, link_name)
                assert os.path.exists(single_loc)
                assert os.path.islink(tile_loc)
            
                self.common_map_req.params['format'] = 'image/png'
                resp = self.app.get(self.common_map_req)
                eq_(resp.content_type, 'image/png')
            