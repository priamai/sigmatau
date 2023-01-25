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

from pydantic import BaseModel, validator
from pydantic_yaml import YamlStrEnum, YamlModel

class MyEnum(YamlStrEnum):
    """This is a custom enumeration that is YAML-safe."""

    a = "a"
    b = "b"

class InnerModel(BaseModel):
    """This is a normal pydantic model that can be used as an inner class."""

    fld: float = 1.0

class MyModel(YamlModel):
    """This is our custom class, with a `.yaml()` method.

    The `parse_raw()` and `parse_file()` methods are also updated to be able to
    handle `content_type='application/yaml'`, `protocol="yaml"` and file names
    ending with `.yml`/`.yaml`
    """

    x: int = 1
    e: MyEnum = MyEnum.a
    m: InnerModel = InnerModel()

    @validator('x')
    def _chk_x(cls, v: int) -> int:  # noqa
        """You can add your normal pydantic validators, like this one."""
        assert v > 0
        return v

m1 = MyModel(x=2, e="b", m=InnerModel(fld=1.5))

# This dumps to YAML and JSON respectively
yml = m1.yaml()
jsn = m1.json()

m2 = MyModel.parse_raw(yml)  # This automatically assumes YAML
assert m1 == m2

m3 = MyModel.parse_raw(jsn)  # This will fallback to JSON
assert m1 == m3

m4 = MyModel.parse_raw(yml, proto="yaml")
assert m1 == m4

m5 = MyModel.parse_raw(yml, content_type="application/yaml")
assert m1 == m5
