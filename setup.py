from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import os


def _post_install(libname, libpath):
    from js9 import j

    # add this plugin to the config
    c = j.core.state.configGet('plugins', defval={})
    c[libname] = libpath
    j.core.state.configSet('plugins', c)

    j.tools.jsloader.generate()
    j.tools.jsloader.copyPyLibs()


class install(_install):

    def run(self):
        _install.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath), msg="Running post install task")


class develop(_develop):

    def run(self):
        _develop.run(self)
        libname = self.config_vars['dist_name']
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), libname)
        self.execute(_post_install, (libname, libpath), msg="Running post install task")


setup(
    name='JumpScale9Prefab',
    version='9.0.0',
    description='Automation framework for cloud workloads remote sal, sal= system abstraction layer',
    url='https://github.com/Jumpscaler/prefab9',
    author='GreenItGlobe',
    author_email='info@gig.tech',
    license='Apache',
    packages=['JumpScale9Prefab'],
    install_requires=[
        'JumpScale9>=9.0.0',
        'paramiko>=2.1.2',
        'asyncssh>=1.9.0',
        'pymongo>=3.4.0',
    ],
    cmdclass={
        'install': install,
        'develop': develop,
        'developement': develop
    },
)
