from paver.easy import *
from paver.path import path
from paver.setuputils import setup


setup(
    name="greenhouse",
    description="An I/O parallelism library making use of coroutines",
    packages=["greenhouse", "greenhouse.io"],
    version="0.5.1",
    author="Travis Parker",
    author_email="travis.parker@gmail.com",
    url="http://github.com/teepark/greenhouse",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
    ],
    install_requires=['greenlet'],
)

MANIFEST = (
    "setup.py",
    "paver-minilib.zip",
)

@task
def manifest():
    path('MANIFEST.in').write_lines('include %s' % x for x in MANIFEST)

@task
@needs('generate_setup', 'minilib', 'manifest', 'setuptools.command.sdist')
def sdist():
    pass

@task
def clean():
    for p in map(path, (
        'greenhouse.egg-info', 'dist', 'build', 'MANIFEST.in', 'docs/build')):
        if p.exists():
            if p.isdir():
                p.rmtree()
            else:
                p.remove()
    for p in path(__file__).abspath().parent.walkfiles():
        if p.endswith(".pyc") or p.endswith(".pyo"):
            p.remove()

@task
def docs():
    sh("cd docs; make html")

@task
def test():
    sh("nosetests --processes=8")
