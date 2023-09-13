import datetime

import js
import pyodide
# npm imports
# noinspection PyUnresolvedReferences
from js.npm import React, ReactDOM, MUI, MUIIcons

# shortcuts
e = React.createElement


# utils for easier react adoption
def jsobj(**kwargs):
    # return to_jsobj(kwargs)
    return js.Object.fromEntries(pyodide.ffi.to_js(kwargs))


def to_jsobj(data):
    return pyodide.ffi.to_js(data, dict_converter=js.Object.fromEntries)


def component(f):
    """
    Make a function usable as React component, props are handled like a Mapping
    """

    def wrapped(props, children):
        return f(props.as_object_map(), children)

    return pyodide.ffi.create_proxy(wrapped)


def el(obj, *children, **props):
    return e(obj, jsobj(**props), *children)


theme = MUI.createTheme(
    jsobj(
        palette=jsobj(
            primary=jsobj(main="#556cd6"),
            secondary=jsobj(main="#19857b"),
            error=jsobj(main="#FF1744"),
            background=jsobj(default="#fff"),
        )
    )
)


@component
def LightBulbIcon(props, children):
    return e(
        MUI.SvgIcon,
        props,
        e(
            "path",
            jsobj(
                d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7zm2.85 11.1l-.85.6V16h-4v-2.3l-.85-.6C7.8 12.16 7 10.63 7 9c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.63-.8 3.16-2.15 4.1z"
            ),
        ),
    )


@component
def ProTip(props, children):
    # classes = use_styles()
    return e(
        MUI.Typography,
        None,
        e(LightBulbIcon),
        "Pro tip: See more ",
        e(
            MUI.Link,
            jsobj(href="https://material-ui.com/getting-started/templates/"),
            "templates",
        ),
        " on the Material-UI documentation.",
    )


@component
def Copyright(props, children):
    return e(
        MUI.Typography,
        jsobj(variant="body2", color="textSecondary", align="center"),
        "Copyright © ",
        e(
            MUI.Link,
            jsobj(href="https://material-ui.com/", color="inherit"),
            "Your Website",
        ),
        f" {datetime.datetime.now().year}.",
    )


@component
def App(props: dict, children: list):
    value, setValue = React.useState(0)

    def onChange(event, newValue):
        setValue(newValue)

    return e(
        MUI.Container,
        jsobj(maxWidth="sm"),
        e(
            "div",
            # None,
            jsobj(style={'marginTop': 24}),
            e(
                MUI.Typography,
                jsobj(variant="h4", component="h1", gutterBottom=True),
                "PyScript PoC",
            ),
            e(ProTip),
            e(Copyright),

            # Slider
            el(MUI.Slider, defaultValue=30, sx=jsobj(width=300, color='success.main')),

            # Floating Button
            el(MUI.Fab,
               el(MUIIcons.Add),
               color="primary", **{"aria-label": "add"}
               ),

            e(
                MUI.Box,
                to_jsobj({"sx": {"width": 500}}),
                el(
                    MUI.BottomNavigation,
                    el(MUI.BottomNavigationAction, label="Recents", icon=e(MUIIcons.Restore, None)),
                    el(MUI.BottomNavigationAction, label="Favorites", icon=e(MUIIcons.Favorite, None)),
                    el(MUI.BottomNavigationAction, label="Nearby", icon=e(MUIIcons.LocationOn, None)),
                    showLabels=True,
                    value=value,
                    onChange=onChange,
                )
            )

        ),
    )


# Create a div to contain our component and render our App
domContainer = js.document.createElement('div')
js.document.body.appendChild(domContainer)
root = ReactDOM.createRoot(domContainer)

root.render(e(
    MUI.ThemeProvider,
    jsobj(theme=theme),
    e(MUI.CssBaseline),
    e(App),
))
