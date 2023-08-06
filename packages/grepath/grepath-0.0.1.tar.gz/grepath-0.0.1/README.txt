grepath - find executables in PATH that match PATTERN
=====================================================

``grepath`` utility prints full path to executables that match
given file-pattern or regular expression.

Examples:

  * To print executables that contain 'pdf' anywhere in their name::

        $ grepath pdf
        /usr/bin/ps2pdf12
        /usr/bin/ps2pdf13
        ...[snip]...
        /usr/bin/simpdftex
        /usr/bin/dvipdf
    
  * To find executables that don't have 'e' after 'win' in their name::

         C:\> grepath -e "win[^e]"
         C:\windows\system32\winhlp32.exe
         C:\windows\system32\winver.exe
         C:\windows\winhlp32.exe
         C:\windows\winhelp.exe
    
    If ``*.py`` files are not associated with ``python.exe`` then the
    script can be invoked using::
    
         C:\> python \path\to\grepath.py --help
    
To print all available options, type::

    $ grepath --help

Files are licensed under the MIT License. See the file MIT-LICENSE.txt
for details.

The latest version is at http://gist.github.com/79233
