# encoding:utf-8
from os import environ
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import cd
from fabric.contrib.files import sed
import urllib

"""
 Fabric file to upload public/private keys to remote servers
 and set up non-root users. Also prevents SSH-ing in with the
 root user. Fill in the following blank fields then run this
 Fabric script with "fab bootstrap".
"""

# # run the bootstrap process as root before it is locked down
# env.user = 'root'
#
# # the remote server's root password
# env.password = ''
#
# # all IP address or hostnames of the servers you want to put your SSH keys and authorized_host files on, ex: 192.168.1.1
# env.hosts = ['192.168.1.1']
#
# # your full name for the new non-root user
# env.new_user_full_name = 'Wang'
#
# # username for the new non-root user to be created
# env.new_user = 'ubuntu'
#
# env.use_ssh_config = True
# env.key_filename = "~/.ssh/config"
# env.hosts = '115.159.150.106'
# env.user = "root"
# env.key_filen

mhl = "106.15.177.204"
test = "115.159.72.179"
zch1 = "182.254.242.148"
zch2 = "123.206.105.73"
zch3 = "115.159.150.106"
env.user = "root"
env.hosts = [test, zch1, zch2, zch3]
env.key_filename="/Users/ksy-walry/.ssh/id_rsa"
env.use_ssh_config = True
SERVER_ZHAOCAIHUO_PROJECT_DIR = '/exdata/website/zhaocaihuo'
LOCAL_ZHAOCAIHUO_PROJECT_DIR = '/Users/ksy-walry/tianlian/ksy/zhaocaihuo'
SERVER_BEAUTY_PROJECT_DIR = '/exdata/website/Beauty'
LOCAL_BEAUTY_PROJECT_DIR = '/Users/ksy-walry/tianlian/Beauty'


@hosts([zch1, zch2, zch3])
def zhaocaihuo_production_deployment():
    with lcd(LOCAL_ZHAOCAIHUO_PROJECT_DIR):
        local('git pull')
        local('git push')
    with cd(SERVER_ZHAOCAIHUO_PROJECT_DIR):
        run('git pull')
        run('python manage.py check')
        run('/root/.pyenv/versions/2.7.10/bin/supervisorctl restart zhaocaihuo')


@hosts([test])
def zhaocaihuo_testing_deployment():
    with lcd(LOCAL_ZHAOCAIHUO_PROJECT_DIR):
        local('git pull')
        local('git push')
    with cd(SERVER_ZHAOCAIHUO_PROJECT_DIR):
        run('git pull')
        run('python manage.py check')
        run('/root/.pyenv/versions/2.7.10/bin/supervisorctl restart zhaocaihuo')

@hosts([mhl])
def beauty_production_deployment():
    with lcd(LOCAL_BEAUTY_PROJECT_DIR):
        local('git pull')
        local('git push')
    with cd(SERVER_BEAUTY_PROJECT_DIR):
        run('git pull')
        run('python manage.py check')
        run('/usr/bin/supervisorctl restart beauty') # supervisorctl的路径


@hosts([test])
def foo():
    run("ls /")

def local_update():
    local('brew update')
    local('brew upgrade')


def hello(name="world"):
    print("Hello {}!".format(name)) # 不带颜色的输出
    print(green("Hello {}!".format(name))) # 带颜色的输出


@hosts([test])
def foo():
    run("ls /")

def host_type():
    run('uname -s')


def diskspace():
    run('df')


def check():
    # check host type
    host_type()

    # Check diskspace
    diskspace()


def test():
    local("python manage.py test activation_code")


# @hosts('server1')
# def foo():
#     with cd('/exdata/website/'):
#         result = run('ls /sfdjsdf')
#         print result
#
#
# @task(alias='b')
# def bar(name="world"):
#     print("Hello {}!".format(name))


def webservice_read():
    objects = urllib.urlopen('http://my/web/service/?foo=bar').read().split()
    print(objects)


from fabric.context_managers import remote_tunnel
from fabric.network import ssh_config
