"""
Contains all the functionality which renders the jinja2 templates.
"""

import functools

import htmlmin

RENDERERS = []
MINIFY = True

def getRegisteredRenderers():
    """
    Returns the list of registered renderers.
    """
    return RENDERERS

def setMinify(val):
    """
    Set to True to minify html.
    """
    global MINIFY
    MINIFY = val

def registerRenderer(func):
    """
    Adds a renderer function to the list
    """
    RENDERERS.append(func)

def outputToFile(fileName):
    """
    Minifies the HTML and outputs it to a file.
    """
    def decorator_outputToFile(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            renderedHtml = func(*args, **kwargs)

            if MINIFY:
                renderedHtml = htmlmin.minify(renderedHtml,
                                              remove_comments=True,
                                              remove_empty_space=True)

            with open(fileName, "w") as fileOut:
                fileOut.write(renderedHtml)

            print(f"Built file {fileName}")

        return wrapper
    return decorator_outputToFile
