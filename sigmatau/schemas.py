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

__author__ = "Paolo Di Prodi"
__copyright__ = "Copyright 2023, Priam Cyber AI ltd"
__credits__ = []
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "Paolo Di Prodi"
__email__ = "info@priam.ai"
__status__ = "Production"

from pydantic import BaseModel, validator
from pydantic_yaml import YamlStrEnum, YamlModel
from pydantic.types import Optional,Union,List
from pydantic import BaseModel, ValidationError, Extra, root_validator

class StatusEnum(YamlStrEnum):
    """This is a custom enumeration that is YAML-safe."""

    s:str = "stable"
    e:str = "experimental"
    t: str = "test"
    d: str = "deprecated"
    u: str = "unsupported"

class LevelEnum(YamlStrEnum):
    """This is a custom enumeration that is YAML-safe."""

    s:str = "informational"
    e:str = "low"
    t: str = "medium"
    d: str = "high"
    u: str = "critical"

class LogSource(YamlModel):
    category: Optional[str]
    product: Optional[str]
    service: Optional[str]
    definition: Optional[str]
    class Config:
        extra = Extra.forbid
class Sigma(YamlModel):
    """
    Standard Sigma validator
    The detection field needs more granularity
    """
    title: str
    id: Optional[str]
    related: Optional[List[str]]
    status:  Optional[StatusEnum]
    description: Optional[str]
    references: Optional[List[str]]
    author: Optional[str]
    date: Optional[str]
    modified: Optional[str]
    fields: Optional[List[str]]
    tags: Optional[List[str]]
    logsource: Optional[LogSource]
    falsepositives: Union[str,List[str]]
    level: Optional[LevelEnum]
    detection: Optional[dict]
    class Config:
        extra = Extra.forbid


class Derived(YamlModel):
    precision: float = None
    recall: float = None
    f1: float = None
    class Config:
        extra = Extra.forbid

class Matrix(YamlModel):
    tp: float = None
    fp: float = None
    tn: float = None
    fn: float = None
    class Config:
        extra = Extra.forbid

    @root_validator(pre=True)
    def check_terms(cls, values):
        # at least one present
        assert len(values) > 0, 'confusion matrix is empty'
        # check row and columns
        return values

    @validator('tp')
    def set_tp(cls, v):
        assert v>=0.0 and v<=1.0, 'outside bound'

    @validator('fp')
    def set_fp(cls, v):
        assert v>=0.0 and v<=1.0, 'outside bound'

    @validator('fn')
    def set_fn(cls, v):
        assert v>=0.0 and v<=1.0, 'outside bound'

    @validator('tn')
    def set_tn(cls, v):
        assert v>=0.0 and v<=1.0, 'outside bound'
class Report(YamlModel):
    id: str
    matrix: Matrix
    derived: Optional[Derived]
    format: str
    samples: int
    class Config:
        extra = Extra.forbid

class Metrics(YamlModel):
    version: str
    signature_type: str
    reports: List[Report]
    class Config:
        extra = Extra.forbid

class SigmaTau(Sigma):
    """
    Standard Sigma validator
    The detection field needs more granularity
    """
    metrics: Optional[Metrics]

    class Config:
        extra = Extra.forbid

