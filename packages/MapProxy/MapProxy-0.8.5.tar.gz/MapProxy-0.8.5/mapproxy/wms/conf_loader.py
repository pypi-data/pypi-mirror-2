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

"""
Configuration loading and system initializing.
"""
from __future__ import with_statement

import os
import types
import hashlib
import pkg_resources

import logging
log = logging.getLogger(__name__)

from mapproxy.core.conf_loader import Source, CacheSource
from mapproxy.core.client import auth_data_from_url, HTTPClient
from mapproxy.wms.cache import WMSTileSource
from mapproxy.wms.layer import (DirectLayer, WMSCacheLayer, DebugLayer, VLayer,
                                 FeatureInfoSource, MultiLayer, AttributionLayer,
                                 WMSCacheDirectLayer)
from mapproxy.core.layer import LayerMetaData
from mapproxy.core.grid import tile_grid_for_epsg
from mapproxy.wms.server import WMSServer
from mapproxy.wms.request import WMS100MapRequest, WMS111MapRequest, WMS130MapRequest,\
                                  WMS100FeatureInfoRequest, WMS111FeatureInfoRequest,\
                                  WMS130FeatureInfoRequest
from mapproxy.wms.client import WMSClient
from mapproxy.tms.conf_loader import configured_cache_layers
from mapproxy.core.config import base_config, abspath
from mapproxy.core.request import split_mime_type
from mapproxy.core.odict import odict
from mapproxy.core.utils import SemLock


def load_request_parser():
    request_parsers = {}
    for entry_point in pkg_resources.iter_entry_points('mapproxy.wms.request_parser'):
        request_parsers[entry_point.name] = entry_point
    req_parser_name = base_config().wms.request_parser
    request_parser = None
    if req_parser_name != 'default':
        if req_parser_name in request_parsers:
            request_parser = request_parsers[req_parser_name].load()
        else:
            log.warn("configured wms request parser ('%s') not found", req_parser_name)
    return request_parser

request_parser = load_request_parser()
del load_request_parser

def load_client_request():
    client_requests = {}
    for entry_point in pkg_resources.iter_entry_points('mapproxy.wms.client_request'):
        client_requests[entry_point.name] = entry_point
    req_name = base_config().wms.client_request
    client_request = None
    if req_name != 'default':
        if req_name in client_requests:
            client_request = client_requests[req_name].load()
        else:
            log.warn("configured wms client request ('%s') not found", req_name)
    return client_request
client_request = load_client_request()
del load_client_request

def create_wms_server(proxy_conf):
    layers = odict()
    for name, layer in proxy_conf.layer_confs.iteritems():
        layers[name] = configured_layer(layer)
    tile_layers = configured_cache_layers(proxy_conf)    
    layers['__debug__'] = DebugLayer()
    return WMSServer(layers, proxy_conf.service_md, request_parser=request_parser, tile_layers=tile_layers)

def configured_layer(layer_conf):
    """
    Returns a configured layer (WMSCacheLayer, MultiLayer, VLayer, etc).
    """
    attribution_layer = get_attribution_layer(layer_conf)
    if layer_conf.multi_layer:
        layers = [_configured_layer(layer_conf, source, attribution_layer)
                  for source in layer_conf.sources]
        md = layer_conf.layer['md'].copy()
        md['name'] = layer_conf.name
        return MultiLayer(layers, md)
    else:
        return _configured_layer(layer_conf, layer_conf.sources, attribution_layer)

def get_attribution_layer(layer_conf):
    attribution_text = layer_conf.layer.get('attribution', {}).get('text', None)
    if attribution_text is None:
        attribution_text = layer_conf.service.get('attribution', {}).get('text', None)
    if attribution_text is None or attribution_text is '':
        return None
    attribution_inverse = layer_conf.layer.get('attribution', {}).get('inverse', None)
    if attribution_inverse is None:
        attrib = layer_conf.service.get('attribution', {})
        attribution_inverse = attrib.get('inverse', False)
    
    if isinstance(attribution_inverse, basestring):
        if attribution_inverse.lower() == 'true':
            attribution_inverse = True
        else:
            attribution_inverse = False
    return AttributionLayer(attribution_text, inverse=attribution_inverse)

def _configured_layer(layer_conf, sources, attribution_layer=None):
    layer = []
    for source in sources:
        try:
            layer.append(source.configured_layer())
        except NotImplementedError:
            layer.append(WMSCacheLayer(source.configured_cache()))
    layer.reverse()
    if attribution_layer is not None:
        layer.append(attribution_layer)
    md = layer_conf.layer['md'].copy()
    md['name'] = layer_conf.name
    if len(layer) == 1:
        layer = layer[0]
        layer.md = LayerMetaData(md)
        return layer
    return VLayer(md, layer)

class DirectSource(Source):
    def __init__(self, layer_conf, source, param=None):
        Source.__init__(self, layer_conf, source, param)
        self.requests = [create_request(self.source['req'], self.param)]
    def has_featureinfo(self):
        return self.source.get('wms_opts', {}).get('featureinfo', False)
    def configured_layer(self):
        clients = wms_clients_for_requests(self.requests, self.supported_srs)
        return DirectLayer(clients[0], queryable=self.has_featureinfo())

class DebugSource(Source):
    def configured_layer(self):
        return DebugLayer()


class WMSCacheSource(CacheSource):
    def __init__(self, layer_conf, source, param=None):
        CacheSource.__init__(self, layer_conf, source, param)
        version = self.wms_client_version()
        self.requests = [create_request(self.source['req'], self.param,
                                        req_type='map', version=version)]
        self.client_lock = None
        concurrent_requests = self.param.get('concurrent_requests', None)
        if concurrent_requests:
            lock_dir = abspath(base_config().cache.lock_dir)
            md5 = hashlib.md5(self.source['req']['url'])
            lock_file = os.path.join(lock_dir, md5.hexdigest() + '.lck')
            self.client_lock = lambda: SemLock(lock_file, concurrent_requests)
        self.fi_requests = []
        if self.has_featureinfo():
            self.fi_requests.append(create_request(self.source['req'], self.param,
                                                   req_type='featureinfo', 
                                                   version=version))
    
    def wms_client_version(self):
        return self.source.get('wms_opts', {}).get('version', '1.1.1')
    
    def has_featureinfo(self):
        return self.source.get('wms_opts', {}).get('featureinfo', False)
    
    def configured_layer(self):
        fi_source = None
        if self.fi_requests:
            fi_clients = wms_clients_for_requests(self.fi_requests, self.supported_srs)
            fi_source = FeatureInfoSource(fi_clients)
        if 'use_direct_from_level' in self.param or 'use_direct_from_res' in self.param:
            clients = wms_clients_for_requests(self.requests[::-1], self.supported_srs,
                                               self.client_lock)
            direct_from_level = self.param.get('use_direct_from_level', None)
            direct_from_res = self.param.get('use_direct_from_res', None)
            if direct_from_level is not None and direct_from_res is not None:
                log.warn('only one of direct_from_level _or_ direct_from_res supported')
            return WMSCacheDirectLayer(self.configured_cache(), fi_source=fi_source,
                direct_clients=clients, direct_from_level=direct_from_level,
                direct_from_res=direct_from_res)
        return WMSCacheLayer(self.configured_cache(), fi_source=fi_source)
    
    def init_grid(self):
        req = self.requests[0]
        bbox = req.params.bbox
        self.transparent = req.params.transparent
        res = self.param['res']
        if isinstance(res, list): res.sort(reverse=True)
        srs = self.param['srs']
        tile_size = self.layer_conf.layer.get('param', {}).get('tile_size', (256, 256))
        self.grid = tile_grid_for_epsg(epsg=srs, tile_size=tile_size, bbox=bbox, res=res)
    def init_tile_source(self):
        clients = wms_clients_for_requests(self.requests[::-1], self.supported_srs,
                                           self.client_lock)
        format = self.layer_conf.layer.get('param', {}).get('format', None)
        if format is not None:
            _mime_class, format, _options = split_mime_type(format)
        self.src = WMSTileSource(self.grid, clients, format=format,
                                 meta_size=base_config().cache.meta_size,
                                 meta_buffer=base_config().cache.meta_buffer)
    
    def merge(self, other):
        if isinstance(other, WMSCacheSource) and self.param == other.param:
            self.requests.extend(other.requests)
            self.fi_requests.extend(other.fi_requests)
            return self
        else:
            return None


def wms_clients_for_requests(requests, supported_srs=None, lock=None):
    clients = []
    for req in requests:
        http_client = None
        url, (username, password) = auth_data_from_url(req.url)
        if username and password:
            req.url = url
            http_client = HTTPClient(url, username, password)
        client = WMSClient(req, client_request, http_client=http_client,
                           supported_srs=supported_srs, lock=lock)
        clients.append(client)
    return clients

wms_version_requests = {'1.0.0': {'featureinfo': WMS100FeatureInfoRequest,
                                  'map': WMS100MapRequest,},
                        '1.1.1': {'featureinfo': WMS111FeatureInfoRequest,
                                  'map': WMS111MapRequest,},
                        '1.3.0': {'featureinfo': WMS130FeatureInfoRequest,
                                  'map': WMS130MapRequest,},
                       }

def create_request(req_data, param, req_type='map', version='1.1.1'):
    url = req_data['url']
    req_data = req_data.copy()
    del req_data['url']
    if 'request_format' in param:
        req_data['format'] = param['request_format']
    else:
        req_data['format'] = param['format']
    req_data['bbox'] = param['bbox']
    if isinstance(req_data['bbox'], types.ListType):
        req_data['bbox'] = ','.join(str(x) for x in req_data['bbox'])
    req_data['srs'] = param['srs']
    
    return wms_version_requests[version][req_type](url=url, param=req_data)
