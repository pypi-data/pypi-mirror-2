bp.tagging contains a set of convenience wrappers for mutagen
as well as a single command line script for basic ID3 tag manipulation.

Command line usage
==================

 -  bp_tagging COMMAND [ARGS...]
 -  bp_tagging help [COMMAND]

Options
*******

    -h, --help
        show this help message and exit

Commands
********

    help (?)
        give detailed help on a specific sub-command

    info (i)
        print available metadata for files

        Usage
            bp_tagging info [PATHS...]

        Options
            -h, --help
                show this help message and exit
            -v, --verbose
                print extra information
            -d, --debug
                print debug information


    remove_tag (rmt)
        completely remove TAG from files.

        Usage
            bp_tagging remove_tag TAG [PATHS...]

        Options
            -h, --help
                show this help message and exit
            -v, --verbose
                print extra information
            -d, --debug
                print debug information


    remove_tag_with_content (rmtc)
        remove tags with value PATTERN from files.

        Usage
            bp_tagging remove_tag_with_content PATTERN [PATHS...]

        Options
            -h, --help
                show this help message and exit
            -v, --verbose
                print extra information
            -d, --debug
                print debug information


    replace_in_tag (rpt)
        replace PATTERN with REPLACEMENT in TAG on files. Use 'all' for tag to replace in all tags.

        Usage
            bp_tagging replace_in_tag TAG PATTERN REPLACEMENT [PATHS...]

        Options
            -h, --help
                show this help message and exit
            -v, --verbose
                print extra information
            -n, --nosave
                don't save (only print what would be done).
            -d, --debug
                print debug information


    tag (t)
        get/set the VALUE for TAG on files.

        Usage
            bp_tagging tag TAG [VALUE [PATHS...]]

        Options
            -h, --help
                show this help message and exit
            -v, --verbose
                print extra information
            -s, --set
                set the tag value
            -d, --debug
                print debug information



