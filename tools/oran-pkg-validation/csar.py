# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
import tempfile
import zipfile

import requests
from ruamel import yaml

import toscameta
import utils

LOG = logging.getLogger(__name__)

class _CSARReader(object):

    def __init__(self, source, destination, no_verify_cert=True):
        if os.path.isdir(destination) and os.listdir(destination):
            raise ValueError('{0} already exists and is not empty. '
                             'Please specify the location where the CSAR '
                             'should be extracted.'.format(destination))
        downloaded_csar = '://' in source
        if downloaded_csar:
            file_descriptor, download_target = tempfile.mkstemp()
            os.close(file_descriptor)
            self._download(source, download_target)
            source = download_target
        self.source = os.path.expanduser(source)
        self.destination = os.path.expanduser(destination)
        self.metadata = None
        self.manifest = None
        try:
            if not os.path.exists(self.source):
                raise ValueError('{0} does not exists. Please specify a valid CSAR path.'
                                 .format(self.source))
            if not zipfile.is_zipfile(self.source):
                raise ValueError('{0} is not a valid CSAR.'.format(self.source))
            self._extract()
            self._read_metadata()
        finally:
            if downloaded_csar:
                os.remove(self.source)

    @property
    def created_by(self):
        return self.metadata.created_by

    @property
    def csar_version(self):
        return self.metadata.csar_version

    @property
    def meta_file_version(self):
        return self.metadata.meta_file_version

    @property
    def entry_definitions(self):
        return self.metadata.entry_definitions

    @property
    def entry_definitions_yaml(self):
        with open(os.path.join(self.destination, self.entry_definitions)) as f:
            return yaml.safe_load(f)

    @property
    def entry_manifest_file(self):
        return self.metadata.entry_manifest_file

    @property
    def entry_history_file(self):
        return self.metadata.entry_history_file

    @property
    def entry_tests_dir(self):
        return self.metadata.entry_tests_dir

    @property
    def entry_licenses_dir(self):
        return self.metadata.entry_licenses_dir

    @property
    def entry_certificate_file(self):
        return self.metadata.entry_certificate_file

    def _extract(self):
        LOG.debug('Extracting CSAR contents')
        if not os.path.exists(self.destination):
            os.mkdir(self.destination)
        with zipfile.ZipFile(self.source) as f:
            f.extractall(self.destination)
        LOG.debug('CSAR contents successfully extracted')

    def _read_metadata(self):
        self.metadata = toscameta.create_from_file(self.destination)

    def _download(self, url, target):
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise ValueError('Server at {0} returned a {1} status code'
                             .format(url, response.status_code))
        LOG.info('Downloading {0} to {1}'.format(url, target))
        with open(target, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def read(source, destination, no_verify_cert=False):
    return _CSARReader(source=source,
                       destination=destination,
                       no_verify_cert=no_verify_cert)

