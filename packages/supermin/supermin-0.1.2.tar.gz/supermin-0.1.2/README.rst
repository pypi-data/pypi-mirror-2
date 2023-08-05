########
supermin
########

Compresses javascript with different compressors and choses the smallest one.

*****
Usage
*****

After installation use supermin from the shell of your choice::

    supermin myfile.js
    
*************
Configuration
*************

You can enable new engines which have templates installed using the
'-add-engine' option. Please provide the name of the engine (eg. 'google',
'yui', ...) and the path to the binary.
    
*********
Extending
*********

To support a new compressing engine, you need to add a command template for it.
Have a look at the existing ones for help.