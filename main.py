import os
import random
import string
from typing import Any, Callable

import mesop as me
import mesop.labs as mel
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from pydantic import BaseModel

app = FastAPI()


def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.get("/hello")
def hello():
    return generate_random_string()


@me.stateclass
class State:
    count: int = 0
    value: str


def increment(event: me.ClickEvent):
    state = me.state(State)
    state.count += 1


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_script_srcs=[
            "https://cdn.jsdelivr.net",
        ]
    )
)
def counter_page():
    state = me.state(State)
    me.text(f"count={state.count}")
    me.text(f"value (from web component doing fetch)={state.value}")
    me.button("Increment", on_click=increment, type="flat")
    web_component(on_value=on_value)


class Value(BaseModel):
    value: str


def on_value(e: mel.WebEvent):
    value = Value(**e.value)
    me.state(State).value = value.value


@mel.web_component(path="/web_component.js")
def web_component(on_value: Callable[[mel.WebEvent], Any]):
    mel.insert_web_component(
        name="fetch-web-component", events={"valueHandlerId": on_value}
    )


app.mount(
    "/",
    WSGIMiddleware(
        me.create_wsgi_app(debug_mode=os.environ.get("DEBUG_MODE", "") == "true")
    ),
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_includes=["*.py", "*.js"],
        timeout_graceful_shutdown=0,
    )
