bp.convert.movie provides a simple command line wrapper for HandBrakeCLI (which already is a command line application). It is not particulary useful yet, bit is intended to become a conversion queue manager for automatic batch conversion of your (various codec) movie library to formats that are supported out-of-the-box by common media players.

Requirements
============

This package requires, that 
`HandBrakeCLI <http://handbrake.fr/downloads2.php>`_ is installed on your system and can be found in $PATH.


Usage
=====

 -  bp_convert_movie COMMAND [ARGS...]
 -  bp_convert_movie help [COMMAND]

Options
*******

    -h, --help  show this help message and exit


Commands
********

    convert (c)
        convert a movie file using the given preset.
        
        Usage
            bp_convert_movie convert [PRESET [PATHS...]]
        
    
    list_presets (p)
        list available conversion presets
        
        Usage
            bp_convert_movie list_presets 
        
        Options
            -h, --help
                show this help message and exit
            -v, --verbose
                include the preset settings in output
            -d, --debug
                print debug information


