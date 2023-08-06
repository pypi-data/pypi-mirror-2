praekelt.recipe.backup
======================
**Filesystem and database backup Buildout recipe.**

Creates a ``bin/`` script with which you can easily create backups of any path and/or database. Uses rsync to create incrementally complete backups, see: `Do-It-Yourself Backup System Using Rsync <http://www.sanitarium.net/golug/rsync_backups_2010.html>`_.  

**NOTE: This recipe is under active development and has not been fully tested in a production environment. Use at your own risk.**

Usage
-----

Add a part in ``buildout.cfg`` like so::

    [buildout]
    parts = backup
    
    [backup]
    recipe = praekelt.recipe.backup
    prefix = foobar
    local_storage_path = /var/backups

Running the buildout will add a backup script with the same name as your backup part in the ``bin/`` directory. In this case ``bin/backup``. The resulting script will create timestamped backups of the buildout path prefixed with the string ``foobar`` locally in ``/var/backups``.

Options
-------
**prefix**
    String prefixed to backup directory names. **Required.**
**source_path**
    Path to recursively backup. **Defaults to the buildout directory.**
**database_engine**
    Type of database to backup. **Supported options: mysql or postgres.**
**database_name**
    Name of the database to backup.
**database_username**
    Username of the database to backup.
**database_password**
    Password of the database to backup.
**local_count**
    Number of backups to keep locally. As new backups are created older backups are deleted. **Defaults to 3.**
**local_storage_path**
    Local path in which to store backups. Make sure the user running the backup script has appropriate rights to this path. **Required.**
**remote_host**
    Hostname of remote host on which to mirror local backups.
**remote_storage_path**
    Remote path in which to store backups. Make sure the user running the backup script has appropriate rights to this path (via rsync).

**Note: rsync functionality is limited to key based authentication. Make sure to setup your keys appropriately for passwordless remote authentication.**

Full Example
------------

The following example illustrates all available options::

    [buildout]
    parts = backup

    [backup]
    recipe = praekelt.recipe.backup
    prefix = foobar
    local_count = 2
    local_storage_path = /var/backups
    source_path = /var/foobar

    remote_host = www.my-backup-server.com
    remote_storage_path = /var/backups/foobar

    database_engine = postgres
    database_name = foobar_db
    database_username = db_username
    database_password = db_password
    
The resulting script will create timestamped backup folders prefixed with the string ``foobar`` locally in ``/var/backups``. The backup will contain all the files found in ``/var/foobar`` as well as a database dump of the postgres database named ``foobar_db``. A copy of each created backup will be sent to ``www.my-backup-server.com`` via rsync and stored in the ``/var/backups/foobar`` path. Only the latest 2 backups will be retained locally. Older backups will be deleted automatically.

