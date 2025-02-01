""" Mesop + FastAPI + WebComponent example """

import os
import random
import string

import mesop as me
import mesop.labs as mel
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from web_component.web_component import (
    Value,
    web_component,
)

# FastAPI app
app = FastAPI()


def generate_random_string(length=8):
    """Generates a random string"""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@app.get("/hello")
def hello():
    """Hello FastAPI endpoint"""
    return generate_random_string()


# Mesop
@me.stateclass
class State:
    """Mesop state class"""

    count: int = 0
    value: str


def increment(event: me.ClickEvent):  # pylint: disable=unused-argument
    """increment the mesop state counter on click handler"""
    state = me.state(State)
    state.count += 1

    print("trying to call web component")
    state.webcomponentinput = generate_random_string()


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_script_srcs=[
            "https://cdn.jsdelivr.net",
        ]
    )
)
def counter_page():
    """Main Mesop page"""
    state = me.state(State)

    with me.box(style=PAGE_STYLE):
        me.text(f"count={state.count}")
        me.text(f"state value (from web component doing fetch)={state.value}")
        me.button("Increment", on_click=increment, type="flat")
        
        me.box(style=me.Style(height=16))
        
        web_component(on_value=on_value)


def on_value(e: mel.WebEvent):
    """ 
    Mesop event receiver for WebComponent changes 
    This will receive a MesopEvent from a web component and 
    set the state with the value of the event.
    """
    value = Value(**e.value)
    me.state(State).value = value.value



# Mesop Page Style
PAGE_STYLE = me.Style(
    display="flex",
    flex_direction="column",
    gap=10,
    background=me.theme_var("background"),
    padding=me.Padding(top=24, left=24, right=24, bottom=24),
    margin=me.Margin.all(15),
)


# FastAPI: mount the Mesop app
app.mount(
    "/",
    WSGIMiddleware(
        me.create_wsgi_app(debug_mode=os.environ.get("DEBUG_MODE", "") == "true")
    ),
)

# Main
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
