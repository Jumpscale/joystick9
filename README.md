# ACTIVE DEVELOPMENT CONTINUES IN: 
# https://github.com/threefoldtech

![travis](https://travis-ci.org/Jumpscale/prefab9.svg?branch=master)

# Prefab

Prefab is a tool to automate installations and configurations on a remote or local machine using [Jumpscale executor](https://github.com/Jumpscale/core9/tree/master/docs)


Prefab makes it easy to automate server installations and create configuration recipes by wrapping common administrative tasks, such as installing packages and creating users and groups, writing files, upload, download files, etc. in Python functions.

Prefab also contains [Modules](docs/README.md) to install complete services with all its dependencies

## Terminology
In the following sections **agent machine** will be used to refer to the machine on which there exists a prefab installation, while **target machine** will be used to refer to the targeted machine on which we want to perform any of the operations mentioned above, note that in case of local prefab the **target machine** is the same as **agent machine**.

## Prerequisites
- on Agent machine
    - [Jumpscale](https://github.com/Jumpscale/core9)
- on Target machine
    - bash
    - openssh-sftp-server
    - openssl-util
    - coreutils-base64  
    normally these packages are already installed on most of OSs


## Installation

Normally Prefab is installed with jumpscale, However you can install it using pip like this

```
pip3 install git+https://github.com/Jumpscale/prefab9@master
```
## Usage

Prefab takes an `executor` object as an argument, through which you connect locally or remotely.

### Local

```python
executor = j.tools.executorLocal
prefab = j.tools.prefab.get(executor)
# or simply prefab = j.tools.prefab.local
prefab.core.run('hostname')
# this will return the host name of your target machine
# which is the same as the agent machine
```

### Remote

```python

executor = j.tools.executor.ssh_get(sshclient)
prefab = j.tools.prefab.get(executor)
prefab.core.run('hostname')
# this will return the host name of the target machine
```

# Modules
Please visit [Modules](docs/README.md) page to overview the available modules and also learn [How to add new modules](modules/README.md)
