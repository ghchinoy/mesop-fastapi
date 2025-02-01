from dataclasses import asdict, dataclass
from typing import Any, Callable

import mesop.labs as mel
from pydantic import BaseModel


class Value(BaseModel):
    value: str


@mel.web_component(path="./web_component.js")
def web_component(
    on_value: Callable[[mel.WebEvent], Any],

):
    """
    Mesop definition of included web component that interacts with FastAPI endpoint
    This will insert the web component into the render tree
    """
    mel.insert_web_component(
        name="fetch-web-component",
        # events must have a key that matches the web component property name
        events={"valueHandlerId": on_value},

    )
