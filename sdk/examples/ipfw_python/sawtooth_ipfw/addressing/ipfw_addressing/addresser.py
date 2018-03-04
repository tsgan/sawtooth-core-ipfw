# Copyright 2017 Intel Corporation
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
# -----------------------------------------------------------------------------

import enum
import hashlib


IPFW_NAMESPACE = hashlib.sha512('ipfw'.encode("utf-8")).hexdigest()[0:6]


def make_ipfw_address(num):
    return IPFW_NAMESPACE + \
        hashlib.sha512(num.encode('utf-8')).hexdigest()[:64]
#        hashlib.sha512(num.encode('utf-8')).hexdigest()[:64] + '0123456789' + num

