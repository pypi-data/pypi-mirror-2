.. _readme:

GOZERBOT 0.9.2 README
=====================

welcome to GOZERBOT ;] see http://gozerbot.googlecode.com

0.9.2 Requirements 
~~~~~~~~~~~~~~~~~~

    * a shell
    * python 2.5 or python 2.6

quick run
~~~~~~~~~

    !! make a separate user and group for the bot !!

    * wget the latest code from http://gozerbot.googlecode.com/
    * untar it
    * cd into the bot dir and run the following:

      * IRC

      ::

        ./bin/gozerbot -o <userhost of the owner> -s <server> -c <\#channel>

      notice the \ thats for escaping the # in the channel name

      * Jabber / XMPP

      ::

        ./bin/gozerbot -t xmpp -o <JID of the owner> -u <bot JID> -p <pass>

    * this creates the necesary directories and config files .. after
      checking if the bot runs fine you can run the bot in daemon mode with
      ::

        ./bin/gozerbot >> logfile 2>&1 &

      gozerbot-start is for bots running from ~/.gozerbot (debian and freebsd)

    * you can also edit the gozerdata/mainconfig and gozerdata/fleet/default/config files

upgrading
~~~~~~~~~

    * to upgrade the bot run:

      ::

        ./bin/gozerbot-upgrade <oldbotdir> <newbotdir>

      use the -l option to copy over the logfiles if needed

    * 0.7 upgrading is not supported yet.

next
~~~~

    * you can /msg the bot !join #channel to let the bot join channels, the 
      bot wil remember channels it has joined
    * you can use the "meet <nick>" command to add other users to the bot, if 
      you are not in a channel or conference use:
      ::

          !user-add <username> <host or JID>

    * gozerplugs plugins will not be loaded on default. use !reload <plugin> 
      to enable a plugin. see the !available command to see what plugins can 
      be reloaded
    * when using commands in a /msg use --chan <channel> to let the command
      operate on a channel .. default channel in a /msg is the users nick
    
plugin configuration
~~~~~~~~~~~~~~~~~~~~

    * plugin config can be done with the <plugname>-cfg command
      usage:
      ::

        !<plugname>-cfg                   ->      shows list of all config
        !<plugname>-cfg key value         ->      sets value to key
        !<plugname>-cfg key               ->      shows list of key
        !<plugname>-cfg key add value     ->      adds value to list
        !<plugname>-cfg key remove value  ->      removes value from list
        !<plugname>-cfg key clear         ->      clears entire list
        !<plugname>-cfgsave               ->      save configuration to disk

    * or edit gozerdata/plugs/<plugname>/config

notes
~~~~~

    * we are on #dunkbots IRCnet

    * MAKE REGULAR BACKUPS OF YOUR BOT DIRECTORY

    * see http://gozerbot.googlecode.com for the bot's documentation

    * if you want to email me use bthate@gmail.com

links
~~~~~
::

    main site - http://gozerbot.googlecode.com
    blog - http://blog.gozerbot.org
    docs - http://gozerbot.googlecode.com
    source - http://gozerbot.googlecode.com/hg

LAST NOTE
~~~~~~~~~

check http://blog.gozerbot.org for security "need to upgrade" notices.
put a rss watcher on it ;]
