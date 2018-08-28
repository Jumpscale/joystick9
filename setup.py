from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import os


def _post_install(libname, libpath):
    from js9 import j

    # add this plugin to the config
    c = j.core.state.configGet('plugins', defval={})
    c[libname] = "%s/github/jumpscale/prefab9/JumpScale9Prefab" % j.dirs.CODEDIR
    j.core.state.configSet('plugins', c)
    j.tools.jsloader.generate()


class install(_install):

    def run(self):
        _install.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath),
                     msg="Running post install task")


class develop(_develop):

    def run(self):
        _develop.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath),
                     msg="Running post install task")


long_description = ""
try:
    from pypandoc import convert
    long_description = convert("README.md", 'rst')
except ImportError:
    long_description = ""


setup(
    name='JumpScale9Prefab',
    version='development,
    description='Automation framework for cloud workloads remote sal, sal= system abstraction layer',
    long_description=long_description,
    url='https://github.com/Jumpscaler/prefab9',
    author='GreenItGlobe',
    author_email='info@gig.tech',
    license='Apache',
    packages=find_packages(),
    install_requires=[
        'JumpScale9>=9.4.0',
        'paramiko>=2.2.3',  # for parallel-ssh
        'asyncssh>=1.9.0',
        'pymongo>=3.4.0',
    ],
    cmdclass={
        'install': install,
        'develop': develop,
        'developement': develop
    },
)
