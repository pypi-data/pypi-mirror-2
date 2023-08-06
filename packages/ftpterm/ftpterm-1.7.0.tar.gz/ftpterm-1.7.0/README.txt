This Module is FTP client like terminal.

if you start this module, Please input host name, user name, password.

COMMANDS::

   01 : cd <file>                   : move current directory.
   02 : pwd                         : print now directory.
   03 : ls                          : list directory.
   04 : local <cmd>                 : operate local files.
   05 : upload <file>               : upload file.
   06 : download <file>             : download file
   07 : rm<file>                    : delete file.
   08 : mkdir <dir>                 : make directory.
   09 : rmdir <dir>                 : delete directory. (empty dir only.)
   10 : rm -r <dir>                 : delete directory.(not only empty dir.)
   11 : rename <fromname> <toname>  : rename file name.
   12 : find <filename>             : find file name.
   13 : read <file>                 : read file. like cat command.
   14 : status                      : show connect status.
   15 : showip                      : show ip address of user.
   16 : showuser                    : show user name.
   17 : access <file>               : show access authority of file.


In version 1.3, has mode feature.
if you call "useconf" mode,
this module read config file, and login ftp term.

How to write config file::
<host name>
<use name>
<password>
 

there are two mode below.

   01 : nomal -- Please input host, user and passwd. and login.
   02 : useconf <file> -- read config file, and login.
   03 : upload <file> <*config file> <*path> -- upload file.


WARNING!!
Please enter the following command, if you want to upload without specify a configuration file.

    $ python ftpterm.py upload xxxxxxx "" /path/

Please enter "" to third argument.





**HISTORY:
------------------
version 1.7 : add a new commands.
version 1.5 : implement error handling.
version 1.4 : upload mode
version 1.3 : add mode features.
