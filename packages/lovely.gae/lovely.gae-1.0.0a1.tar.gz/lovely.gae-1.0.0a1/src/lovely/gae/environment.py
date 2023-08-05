##############################################################################
#
# Copyright 2009 Lovely Systems AG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################

import os
import sys
import logging

_log = logging.getLogger(__name__)

def BREAKPOINT():
    import pdb
    st = pdb.Pdb(None, sys.__stdin__, sys.__stdout__).set_trace
    st()

def add_appengine_paths(sdk_path=None, django=True):
    if sdk_path not in sys.path:
        sys.path.insert(0, sdk_path)
    import google.appengine
    from dev_appserver import EXTRA_PATHS
    if django:
        paths = EXTRA_PATHS
    else:
        paths = [p for p in EXTRA_PATHS if '/lib/django' not in p]
        for key in [key for key in sys.modules if
                    key.startswith('django')]:
            del sys.modules[key]
    sys.path = paths +  sys.path

