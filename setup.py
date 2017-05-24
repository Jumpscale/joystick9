from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import os


def _post_install(libname, libpath):
    from JumpScale9 import j
    j.tools.jsloader.copyPyLibs()

    # ensure plugins section in config
    if 'plugins' not in j.application.config:
        j.application.config['plugins'] = []

    # add this plugin to the config
    c = j.core.state.configGet('plugins', defval=[])
    exists = any([x for x in c if x == libname])
    if not exists:
        c.append({libname: libpath})
        j.core.state.configSet('plugins', c)

    print("****:%s:%s" % (libname, libpath))

    j.tools.jsloader.generatePlugins()
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
    ],
    cmdclass={
        'install': install,
        'develop': develop,
        'developement': develop
    },
)
