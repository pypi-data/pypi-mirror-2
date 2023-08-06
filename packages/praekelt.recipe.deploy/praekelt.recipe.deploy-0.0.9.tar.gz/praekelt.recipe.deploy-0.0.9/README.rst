praekelt.recipe.deploy
======================
**Buildout recipe making versioned remote deploys trivial.**
   
Creates a ``bin/`` script with which you can easily deploy buildouts to remote servers. Uses `Fabric <http://fabfile.org>`_ to communicate and run commands on remote servers.

**NOTE: This recipe is under active development and has not been fully tested in a production environment. Use at your own risk.**
    
The deploy process proceeds as follows:

#. The remote host as specified in ``host`` is accessed.
#. A new release path structure is created using this pattern: ``<root_path>/releases/<release_timestamp>``.
#. The git repo as specified in ``git_url`` is cloned.
#. The newly cloned repo's branch is switched to the branch as specified in ``git_branch``. If ``git_branch`` is not specified no switch occurs.
#. A Puppet manifest as specified in ``puppet_manifest`` is applied if provided.
#. Shared resources as specified in ``shared_resources`` are copied from the current release(if present) to the newly created release.
#. The Buildout's ``boostrap.py`` is run using the python executable as specified in ``python_exec`` and a Buildout configuration file as specified in ``conf_file``. ``python`` is used by default if ``python_exec`` is not specified, ``buildout.cfg`` is used by default if ``conf_file`` is not specified.
#. The Buildout is run using a Buildout configuration file as specified in ``conf_file``. ``buildout.cfg`` is used by default if ``conf_file`` is not specified.
#. The ``<root_path>/current`` symlink is updated to point to newly created release.
#. Supervisor is updated(``$ supervisorctl update``) if ``update_supervisor`` is specified as ``True``.
#. Each command specified in ``initd_commands`` is run in order.

Usage
-----

Add a part in ``buildout.cfg`` like so::

    [buildout]
    parts = deploy
    
    [deploy]
    recipe = praekelt.recipe.deploy
    git_url = git@github.com:me/projectx.git
    host = www.protectx.com
    root_path = /var/www/projectx

Running the buildout will add a deploy script with the same name as your deploy part in the ``bin/`` directory. In this case ``bin/deploy``. The resulting script will deploy ``git@github.com:me/projectx.git`` to ``www.projectx.com``'s ``/var/www/projectx`` path.

Options
-------
**as_user**
    User as which to perform the deploy. Used to setup permissions appropriately and to clone from github. **Defaults to 'www-data'.**
**conf_file**
    Buildout cfg file with which to run boostrap and buildout. **Defaults to 'buildout.cfg'.**
**cron_commands**
    Commands to add to the ``as_users`` user's crontab.
**deploy_key_path**
    Path on host to key to use when cloning the repo.
**git_branch**
    Git repo branch with which to perform the deploy.
**git_url**
    Git repo with which to perform the deploy. **Required.**
**host**
    Hostname on which to perform deploy. **Required.**
**initd_commands**
    init.d commands to run after a completed deploy. i.e. ``nginx restart``.
**puppet_mainfest**
    Puppet manifest file to apply prior to buildout. This will be applied using ``puppet apply <manifest>``.
**python_exec**
    Python command with which to boostrap Buildout. **Defaults to 'python'.**
**root_path**
    Root path in which to perform the deploy. current/release path structure will be created within this path. **Required.**
**shared_resources**
    Resource paths to copy accross from the current release to the new release on each deploy.
**update_supervisor**
    Whether or not to update supervisor. **Defaults to 'False'.**

Full Example
------------

The following example illustrates all available options::

    [buildout]
    parts = deploy

    [deploy]
    recipe = praekelt.recipe.deploy
    as_user = www-data
    conf_file = production.cfg
    deploy_key_path = /var/www/.ssh/projectx_deploy_key
    git_branch = production
    git_url = git@github.com:me/projectx.git
    host = www.protectx.com
    initd_commands = nginx restart
    puppet_manifest = provision.pp
    python_exec = python2.5
    root_path = /var/www/projectx
    shared_resources = 
        eggs
        downloads
        log
        media
    update_supervisor = True
    cron_commands = * * * * * echo foobar
    
The resulting script will deploy ``git@github.com:me/projectx.git``'s ``production`` branch  to ``www.projectx.com``'s ``/var/www/projectx`` path as user ``www-data``. The git repo will be cloned using ``/var/www/.ssh/projectx_deploy_key`` as ssh key. The Puppet manifest ``provision.pp`` will be applied. The ``eggs``, ``downloads``, ``log`` and ``media`` paths will be copied from the current release to this new release. The buildout environment will be created using ``python2.5`` and run using ``production.cfg`` as configuration file. After the buildout completes supervisor will be updated and ``/etc/init.d/nginx restart`` will be run. ``* * * * * echo foobar`` will be added to ``www-data`` user's crontab.

