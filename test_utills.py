
import json
from typing import Callable, Any
def pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=4))