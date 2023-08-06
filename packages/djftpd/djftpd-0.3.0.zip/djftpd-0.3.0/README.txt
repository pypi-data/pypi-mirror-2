================================
Django Authenticating FTP Server
================================

Version : 0.3.0
Author : Thomas Weholt <thomas@weholt.org>
License : GPL v3.0
Status : Beta
Url : http://bitbucket.org/weholt/djftpd/

About
=====

Djftpd is a ftpserver based on pyftpdlib using the user management in django for authentication.
Handy for giving easy access ftp-accounts to let users upload static content etc.

Installation
============

python setup.py install

Required in settings.py:

0. Add djftpd to your installed apps.    

Optional in settings.py:
    
1. get_ftp_home_dir: A method which takes an username as parameter and 
   returns a complete folder to use as homefolder for the given user.

2. FTP_PORT : If you want to use another port than 21.

3. FTP_ADDRESS : If you want to use a specific address, defaults to '127.0.0.1'.

4. read_perms/write_perms: By default the user has full access the directory returned by the get_ftp_home_dir,
   but you can override the read/write-permissions by setting custom permissions. For
   more information about this read the pyftpdlib source and look for read_perms and write_perms.
   
5. ftp_handler: You can also specify a custom ftp_handler to process actions like user_login, user_logout,
   downloads and uploads etc, for logging purposes for instance. Read more about how to
   create your own handler here http://code.google.com/p/pyftpdlib/wiki/Tutorial#3.8_-_Event_callbacks

6. FTP_WELCOME_MSG: the welcome message to display when users log on.   

Usage
=====

Djftpd comes with a django management command called startftpserver. It will start the ftp server in
blocking mode. If you want to use it in a stand-alone script, perhaps daemonize/fork it, on linux do
something (untested code follows) like::

    import os
    import sys
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' # points to your settings.py file

    from djftpd import create_django_ftpserver

    ## {{{ http://code.activestate.com/recipes/66012/ (r1)
    def do_fork(method_to_deamonize):
        # do the UNIX double-fork magic, see Stevens' "Advanced 
        # Programming in the UNIX Environment" for details (ISBN 0201563177)
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError, e: 
            print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 

        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent, print eventual PID before
                print "Daemon PID %d" % pid 
                sys.exit(0) 
        except OSError, e: 
            print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
            sys.exit(1) 

        # start the daemon main loop
        method_to_deamonize()
        ## end of http://code.activestate.com/recipes/66012/ }}}

    def start_server():
        ftpd = create_django_ftpserver()
        ftpd.serve_forever()

    do_fork(start_server)

Requirements
============

* pyftpdlib
* django

References
==========

[1] : http://www.djangoproject.com
[2] : http://pypi.python.org/pypi/pyftpdlib/