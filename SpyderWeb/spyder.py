"""
The entry point for spyderweb.
"""

import argparse
import subprocess
import shutil

from jinja2 import Environment, PackageLoader, select_autoescape

from spyderweb.rendering import setMinify, getRegisteredRenderers

def build(jinjaPackage, minifyPath, jsPath):
    """
    Runs the build.
    """
    # Setup inputs
    parser = argparse.ArgumentParser(description="Build HTML and JS sources")
    parser.add_argument("-m", nargs='+',
                        default=["html", "js"],
                        choices=["html", "js"],
                        dest="minify")
    args = parser.parse_args()

    # Create the jinja environment
    env = Environment(loader=PackageLoader(jinjaPackage),
                      autoescape=select_autoescape(["html", "xml"]))

    # Render all pages
    setMinify("html" in args.minify)

    for renderer in getRegisteredRenderers():
        renderer(env)

    # Minify or copy js
    if "js" in args.minify:

        subprocess.run([minifyPath, jsPath, "-d", "js"])
    else:
        shutil.rmtree("js", ignore_errors=True)
        shutil.copytree(jsPath, "js")
