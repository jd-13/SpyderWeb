"""
Contains all the functionality which renders the HTML jinja2 templates.
"""

import functools
import os

import htmlmin

RENDERERS = []
MINIFY = True
OUTPUT_PATH = os.getcwd()

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

def setOutputPath(val):
    """
    Set the path to output the html files.

    Defaults to current working directory.
    """
    global OUTPUT_PATH
    OUTPUT_PATH = val

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

            with open(os.path.join(OUTPUT_PATH, fileName), "w") as fileOut:
                fileOut.write(renderedHtml)

            print(f"Built file {fileName}")

        return wrapper
    return decorator_outputToFile
