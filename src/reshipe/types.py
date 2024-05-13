from .resource import Resource
from typing import Type, Union, List

ResourceType = Type[Union[Resource, List[Resource]]]