from __future__ import annotations
import re
import warnings
from collections import OrderedDict
from typing import TYPE_CHECKING
from reshipe.resource import Resource
if TYPE_CHECKING:
    from typing import Optional
    from typing import Dict, List, Any
    from reshipe.types import ResourceType

class Recipe:
    targets: List[Resource]
    recipe: dict
    results: OrderedDict = OrderedDict()
    backward_comp: bool
    startup_scripts: List['str']
    
    def __init__(self, 
                 target: ResourceType, 
                 recipe: dict,
                 startup_scripts: Optional[List[str]] = None):
        self.targets = target if isinstance(target, list) else [target]
        self.recipe = recipe
        self.startup_scripts = startup_scripts or []
        self._parse_recipe()
        
    def _parse_recipe(self):
        for key, value in self.recipe.items():
            if key == 'startup':
                scripts = [s for s in value if s is not None]
                self.startup_scripts.extend(scripts)
            else:
                if value := self._eval_value(value):
                    self.results[key] = value
    
    def _eval_value(self, value: Any):
        if isinstance(value, str):
            value = self._process_str(value)
        elif isinstance(value, list):
            value = self._process_list(value)
        elif isinstance(value, dict):
            value = self._process_dict(value)
        return value
    
    def _get_target_hasattr(self, attr):
        for t in self.targets:
            if hasattr(t, attr):
                return t
        return None
    
    def _process_str(self, str_obj: str):
        ptrn = r'(?P<attr>^[a-zA-Z][a-zA-Z0-9_]*)\.(?P<key>[a-zA-Z][a-zA-Z0-9_]*)'
        if matched := re.match(ptrn, str_obj):
            if target := self._get_target_hasattr(matched['attr']):
                attr = getattr(target, matched['attr'])
                return attr.get(matched['key'], None)
            else:
                return None
        else:
            return str_obj
    
    def _process_list(self, list_obj: List):
        processed_list = []
        for c in list_obj:
            processed = self._eval_value(c)
            if processed is not None:
                processed_list.append(processed)
            else:
                processed_list.append(c)
        return processed_list
    
    def _process_dict(self, dict_obj: Dict):
        if 'script' in dict_obj.keys():
            return self._process_dict_case_script(dict_obj, 'script')
        elif 'key' in dict_obj.keys():
            return self._process_dict_case_pick_from_list(dict_obj)
        elif 'first_avail' in dict_obj.keys() and len(dict_obj.keys()) == 1 and isinstance(dict_obj.values()[0], list):
            return self._
        else:
            processed = {}
            for key, value in dict_obj.items():
                if value := self._eval_value(value):
                    processed[key] = value
            return processed if len(processed) else None
        
    def _process_dict_case_first_avail(self, dict_obj: Dict):
        for c in dict_obj['first_avail']:
            processed = self._eval_value(c)
            if processed is not None:
                return processed
        return None
        
    def _process_dict_case_script(self, dict_obj: Dict, script_cmd: str):
        script = dict_obj[script_cmd]
        if self.startup_scripts:
            for s in self.startup_scripts:
                exec(s)
        for key, value in dict_obj.items():
            if key != script_cmd:
                value = self._eval_value(value)
                if value == None:
                    return None
                exec(f'global {key}')
                try:
                    exec(f'{key} = {value}')
                except NameError:
                    exec(f"{key} = '{value}'")
        exec(f"output = {script}", globals(), locals())
        return locals()['output']
    
    def _process_dict_case_pick_from_list(self, dict_obj: Dict):
        key = dict_obj.pop('key')
        value = self._process_str(key)
        if not isinstance(value, list):
            warnings.warn(f"The value returned from '{key}' is not of type 'list'.", UserWarning)
            return None
        if 'where' in dict_obj.keys():
            hint = self._eval_value(dict_obj.pop('where'))
            return value.index(hint) if hint in value else None
        elif 'idx' in dict_obj.keys():
            idx = self._eval_value(dict_obj.pop('idx'))
            return value[idx] if idx < len(value) else None
    
    def get(self):
        return self.results