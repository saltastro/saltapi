###############
### imports ###
###############

import os
from fabric.api import cd, env, lcd, put, prompt, local, sudo, run
from fabric.contrib.files import exists
import time


##############
### config ###
##############

local_app_dir = './'
local_config_dir = './config'

remote_app_dir = '/home/tacweb'
remote_git_dir = '/home/tacweb/git'
remote_flask_dir = remote_app_dir
remote_nginx_dir = '/etc/nginx/sites-enabled'
# remote_supervisor_dir = '/etc/supervisor/conf.d'
git_repository = 'git@github.com:Eb-Zeero/tacapi.git'
# timestamp = 'release_{date}'.format(date=int(time.time()*1000))

env.user_ssh_config = True
env.hosts = ['{host}'.format(host=os.environ["TAC_API_HOST"])]
env.user = '{user}'.format(user=os.environ["TAC_API_HOST_USER"])
env.password = '{password}'.format(password=os.environ["TAC_API_HOST_PASSWORD"])


#############
### tasks ###
#############

def commit_and_push():
    with lcd(local_app_dir):
        local('git add -A')
        commit_message = prompt("Commit message?")
        local('git commit -am "{0}"'.format(commit_message))
        local('git push')


def install_requirements():
    """ Install required packages. """
    # Python3
    sudo('apt-get update')
    sudo('apt-get install -y python3')
    sudo('apt-get install -y python3-pip')
    sudo('apt-get install -y python3-dev')
    # sudo('apt-get install -y python3-virtualenv')

    # Web Server
    sudo('apt-get install -y nginx')

    # Supervisor
    sudo('apt-get install -y supervisor')

    # Git
    sudo('apt-get install -y git')

    # MySQL
    sudo('apt-get install -y mysql-client')
    sudo('apt-get install -y libmysqlclient-dev')

    sudo('sudo pip3 install virtualenv')
    commit_and_push()
    if exists(remote_app_dir + '/tacapi') is False:
        run("git clone https://github.com/Eb-Zeero/tacapi.git")
        print("\n\n\n !!!!!!!!!!repo cloned!!!!!!!!!!!!!!\n\n\n")

    with cd(remote_app_dir + '/tacapi'):
        run('virtualenv tacapivenv')
        run('source tacapivenv/bin/activate')
        run('pip install -r requirements.txt')

'''
def install_flask():
    """
    1. Create project directories
    2. Create and activate a virtualenv
    3. Copy Flask files to remote host
    """
    if exists(remote_app_dir) is False:
        sudo('mkdir ' + remote_app_dir)
    if exists(remote_flask_dir) is False:
        sudo('mkdir ' + remote_flask_dir)
    with lcd(local_app_dir):
        with cd(remote_app_dir):
            sudo('pip install --upgrade virtualenv')
            sudo('virtualenv -p python3 tacapivenv')
            sudo('source tacapivenv/bin/activate')
            sudo('pip install Flask==0.12.2')
            sudo('pip install uwsgi')
        with cd(remote_flask_dir):
            put('*', './', use_sudo=True)
'''

def configure_nginx():
    """
    1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    sudo('/etc/init.d/nginx start')
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    if exists('/etc/nginx/sites-enabled/tacapi') is False:
        sudo('touch /etc/nginx/sites-available/tacapi')
        sudo('ln -s /etc/nginx/sites-available/tacapi' +
             ' /etc/nginx/sites-enabled')
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put('./tacapi', './', use_sudo=True)
    sudo('/etc/init.d/nginx restart')

    # Seen /etc/systemd/system/tacapi.service I created it manually

    sudo('systemctl start tacapi')
    sudo('systemctl enable tacapi')

    # test Nginx
    print("\n\n\n!!!!!!!!!!!! Testing Nginx !!!!!!!!!!!!!!!\n\n\n")
    sudo('nginx -t')
    print("\n\n\n!!!!!!!!!!!! Restarting Nginx !!!!!!!!!!!!!!!\n\n\n")
    sudo('systemctl restart nginx')
    sudo('ufw delete allow 5000')
    sudo("sudo ufw allow 'Nginx Full'")



'''
def configure_supervisor():
    """
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """
    if exists('/etc/supervisor/conf.d/tacapi.conf') is False:
    if exists('/etc/systemd/system/tacapi.service') is False:
        with lcd(local_config_dir):
            with cd(remote_supervisor_dir):
                put('./tacapi.conf', './', use_sudo=True)
                sudo('supervisorctl reread')
                sudo('supervisorctl update')

'''


def configure_git():
    """
    1. Setup bare Git repo
    2. Create post-receive hook
    """
    if exists(remote_git_dir) is False:
        sudo('mkdir ' + remote_git_dir)
        with cd(remote_git_dir):
            sudo('mkdir tacapi.git')
            with cd('tacapi.git'):
                sudo('git init --bare')
                with lcd(local_config_dir):
                    with cd('hooks'):
                        put('./post-receive', './', use_sudo=True)
                        sudo('chmod +x post-receive')


def run_app():
    """ Run the app! """
    with cd(remote_flask_dir):
        sudo('supervisorctl start tacapi')


def deploy():
    """
    1. Copy new Flask files
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git add -A')
        commit_message = prompt("Commit message?")
        local('git commit -am "{0}"'.format(commit_message))
        local('git push')
        sudo('supervisorctl restart tacapi')


def rollback():
    """
    1. Quick rollback in case of error
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git revert master  --no-edit')
        local('git push')
        sudo('supervisorctl restart tacapi')


def status():
    """ Is our app live? """
    sudo('supervisorctl status')


def setup():
    install_requirements()
    configure_nginx()
    configure_git()
