"""Builds the GlowScript package files in package/ from sources in lib/ and shaders/.

Run from the rsWVPRunner directory:
    python build_package.py

Outputs:
    package/glow.<version>.min.js       -- runtime
    package/compiler.<version>.min.js   -- JavaScript compiler
    package/RScompiler.<version>.min.js -- RapydScript compiler
    package/RSrun.<version>.min.js      -- RapydScript runtime (for exported programs)

Also regenerates lib/glow/shaders.gen.js from shaders/*.shader.

Requires node and build-tools/Uglify-ES (copied from Classic GlowScript).
"""

from glob import glob
import re, os, subprocess
import platform

# Regenerate shaders.gen.js from shader sources
shader_file = ["Export({ shaders: {"]
for fn in sorted(glob("shaders/*.shader")):
    name = re.match(r"^shaders[/\\]([^.]+).shader$", fn).group(1)
    f = open(fn, "rt").read()
    shader_file.append( '"' + name + '":' + repr(f) + "," )
shader_file.append("}});")
shader_file = "\n".join(shader_file)
open("lib/glow/shaders.gen.js", "w").write(shader_file)
print('Finished shaders.gen.js\n')

version = "3.2"

glowscript_libraries = {
    "run": [
        "../lib/jquery/2.1/jquery.mousewheel.js",
        "../lib/flot/jquery.flot.js",
        "../lib/flot/jquery.flot.crosshair_GS.js",
        "../lib/plotly.js",
        "../lib/opentype/poly2tri.js",
        "../lib/opentype/opentype.js",
        "../lib/glMatrix.js",
        "../lib/webgl-utils.js",
        "../lib/glow/property.js",
        "../lib/glow/vectors.js",
        "../lib/glow/mesh.js",
        "../lib/glow/canvas.js",
        "../lib/glow/orbital_camera.js",
        "../lib/glow/autoscale.js",
        "../lib/glow/WebGLRenderer.js",
        "../lib/glow/graph.js",
        "../lib/glow/color.js",
        "../lib/glow/shapespaths.js",
        "../lib/glow/primitives.js",
        "../lib/glow/api_misc.js",
        "../lib/glow/extrude.js",
        "../lib/glow/shaders.gen.js",
        ],
    "compile": [
        "../lib/compiling/GScompiler.js",
        "../lib/compiling/acorn.js",
        "../lib/compiling/papercomp.js",
        ],
    "RScompile": [
        "../lib/rapydscript/compiler.js",
        "../lib/compiling/GScompiler.js",
        "../lib/compiling/acorn.js",
        "../lib/compiling/papercomp.js",
        ],
    "RSrun": [
        "../lib/rapydscript/runtime.js",
        ],
    }

def combine(inlibs):
    all = [
        "/*This is a combined, compressed file.  Look at https://github.com/BruceSherwood/glowscript for source code and copyright information.*/",
        ";(function(){})();"
        ]
    for fn in inlibs:
        if fn.startswith("../"): fn = fn[3:]
        all.append( open(fn, "r").read() )
    return "\n".join(all)

env = os.environ.copy()
env["NODE_PATH"] = "build-tools/UglifyJS"

def minify(inlibs, inlibs_nomin, outlib):
    all = combine(inlibs)
    outf = open(outlib, "w")
    if platform.system() == 'Darwin':
        uglify = subprocess.Popen( "node build-tools/Uglify-ES/uglify-es/bin/uglifyjs",
            shell=True,
            stdin=subprocess.PIPE,
            stdout=outf,
            stderr=outf,
            env=env
            )
    else:
        uglify = subprocess.Popen( "build-tools/node.exe build-tools/Uglify-ES/uglify-es/bin/uglifyjs",
            stdin=subprocess.PIPE,
            stdout=outf,
            stderr=outf,
            env=env
            )
    uglify.communicate( all.encode("utf-8") )
    rc = uglify.wait()
    if rc != 0:
        print("Something went wrong")
    outf.write( combine(inlibs_nomin) )
    outf.close()

minify( glowscript_libraries["run"], [], "package/glow." + version + ".min.js" )
print('Finished glow run-time package\n')
minify( glowscript_libraries["compile"], [], "package/compiler." + version + ".min.js" )
print('Finished JavaScript compiler package\n')
minify( glowscript_libraries["RScompile"], [], "package/RScompiler." + version + ".min.js" )
print('Finished RapydScript compiler package\n')
minify( glowscript_libraries["RSrun"], [], "package/RSrun." + version + ".min.js" )
print('Finished RapydScript run-time package')
