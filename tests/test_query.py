# Copyright 2024, Sayan Nandan <nandansayan@outlook.com>
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
#
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from src.skytable_py.query import Query, UInt


class QueryTest(unittest.TestCase):
    def test_param_cnt(self):
        self.assertEqual(Query("sysctl report status").get_param_count(), 0)

    def test_encode_few_params(self):
        blob = Query(
            "insert into db.db { name: ?, random_num: ? }", "sayan", UInt(300))._buffer
        self.assertEqual(
            blob, b"insert into db.db { name: ?, random_num: ? }\x065\nsayan\x02300\n")
