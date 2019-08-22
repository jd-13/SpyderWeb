"""
The entry point for spyderweb.
"""

import argparse
import os
import subprocess
import shutil

from jinja2 import Environment, PackageLoader, select_autoescape

from spyderweb.rendering import setMinify, getRegisteredRenderers, setOutputPath

def build(jinjaPackage, minifyPath, outputPath, jsSrcPath=None, cssSrcPath=None):
    """
    Runs the build.
    """
    setOutputPath(outputPath)

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
    if jsSrcPath != None:
        jsOutputPath = os.path.join(outputPath, "js")
        if "js" in args.minify:
            subprocess.run([minifyPath, jsSrcPath, "-d", jsOutputPath])
        else:
            shutil.rmtree(jsOutputPath, ignore_errors=True)
            shutil.copytree(jsSrcPath, jsOutputPath)

    # Copy css (don't minify yet)
    if cssSrcPath != None:
        cssOutputPath = os.path.join(outputPath, "css")

        shutil.rmtree(cssOutputPath, ignore_errors=True)
        shutil.copytree(cssSrcPath, cssOutputPath)



