import os
import os.path
from fabric import api


def bootstrap():
    hostout = api.env.get('hostout')
    #Install and Update Dependencies

    #http://wiki.linuxquestions.org/wiki/Find_out_which_linux_distribution_a_system_belongs_to
    d = api.run(
    #    "[ -e /etc/SuSE-release ] && echo SuSE "
                "[ -e /etc/redhat-release ] && echo redhat"
    #            "[ -e /etc/fedora-release ] && echo fedora || "
    #            "lsb_release -rd "
    #            "[ -e /etc/debian-version ] && echo debian or ubuntu || "
    #            "[ -e /etc/slackware-version ] && echo slackware"
               )
    print d
    api.run('uname -rs')

    # do we really want to upgrade to latest packages? We lose repeatability if we do it!
    # api.sudo('apt-get -y update')
    # api.sudo('apt-get -y upgrade ')    
    
    version = api.env['python-version']
    major = '.'.join(version.split('.')[:2])
    

    # enable EPEL repositories (we need them for installing python2.6, nginx, munin, etc.)
    api.sudo('rpm -Uvh http://download.fedora.redhat.com/pub/epel/5Server/x86_64/epel-release-5-3.noarch.rpm')
    
    # install bunch of stuff we need
    api.sudo('yum -y install '
             # tools
             'vim-enhanced '
             'curl '
             'lynx '
             'rsync '
             'which '
             'gcc-c++ '
             'make '
             
             # pretty fonts
             'xorg-x11-fonts-truetype.noarch '
             'freetype-devel '
             
             # image formats
             'libpng-devel '
             'libjpeg-devel '
             
             # other libs
             'zlib-devel '
             'pcre-devel '
             
             # python
             'python26 '
             'python26-devel '
             # 'python-imaging '
             # 'python-setuptools '
             # 'python-elementtree '
             # 'python-celementtree '
             
             # system monitoring
             'munin '
             
             % locals())
    
    # Install setuptools for python2.6
    api.sudo('wget http://peak.telecommunity.com/dist/ez_setup.py')
    api.sudo('python%(major)s ez_setup.py' % locals())

    # Plone needs PIL installed
    api.sudo('easy_install-2.6 --find-links http://download.zope.org/distribution PILwoTK')

        #if its ok you will see something like this:
        #--------------------------------------------------------------------

        #*** TKINTER support not available

        #--- JPEG support ok

        #--- ZLIB (PNG/ZIP) support ok

        #--- FREETYPE2 support ok

        #--------------------------------------------------------------------

    # NGINX or APACHE?
    # install
    api.sudo('yum -y install nginx')
    
    # start
    api.sudo('sudo /etc/init.d/nginx start')
    
    # start at boot-up
    api.sudo('/sbin/chkconfig nginx on')

    # During its normal use yum creates a cache of metadata and packages. 
    # This cache can take up a lot of space. The yum clean command allows you 
    # to clean up these files. All the files yum clean will act on are 
    # normally stored in /var/cache/yum.
    api.sudo('yum clean all')

    # Add plone user:
    owner = api.env['buildout-user']
    effective = api.env['effective-user']
    buildoutgroup = api.env['buildout-group']
    api.sudo('groupadd -f %(buildoutgroup)s' % locals())
    if owner:
        api.sudo('grep %(owner)s /etc/passwd || adduser %(owner)s ' % locals())
        api.sudo('gpasswd -a %(owner)s %(buildoutgroup)s' % locals())
    if effective:
        api.sudo('grep %(effective)s /etc/passwd || adduser %(effective)s' % locals())
        api.sudo('gpasswd -a %(effective)s %(buildoutgroup)s' % locals())

    # Set access permissions for plone user
    hostout.setaccess()
    path = api.env.path
    api.sudo('mkdir -p %(path)s' % locals())
    hostout.setowners()
    
    #install buildout
#    api.sudo('easy_install-%(major)s zc.buildout' % locals())
    api.env.cwd = api.env.path
    api.sudo('wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py')
    api.sudo('echo "[buildout]" > buildout.cfg')
    api.sudo('python%(major)s bootstrap.py' % locals())

#    api.sudo('easy_install-%(major)s zc.buildout' % locals())
#    api.env.cwd = api.env.path
#    api.run('buildout init')
#    api.run('cd /%(path)s && bin/buildout install lxml' % locals())
#    api.run('cd /%(path)s && bin/buildout' % locals())



def predeploy():
    path = api.env.path
    api.env.cwd = ''

    # if buildout folder is already present, then we don't need to bootstrap the whole server
    if api.sudo("ls  %(path)s/bin/buildout || echo 'bootstrap' " % locals()) == 'bootstrap':
        bootstrap()
    #bootstrap()


