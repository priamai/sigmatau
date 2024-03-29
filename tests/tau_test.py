'''
 * Copyright 2023 Priam Cyber AI ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import unittest
import glob
from schemas import SigmaTau
class TauCase(unittest.TestCase):
    def test_stuff(self):
        for file in glob.glob('./rules/tau/*.yml'):
            print(file)
            try:
                s = SigmaTau.parse_file(file)
                print(s.metrics.reports[0])
            except Exception as e:
                print(e)


if __name__ == '__main__':
    unittest.main()
