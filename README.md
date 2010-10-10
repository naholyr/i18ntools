Play i18ntools module
=====================

This module will add some tools to ease use of i18n in your Play! projects.

Installation
------------

Install the module : it's not yet in the Play! repository, so you have to copy it somewhere :

    git clone git://github.com/naholyr/i18ntools.git

Then you have to enable it in your `application.conf` :

    module.i18ntools=/path/to/i18ntools

Check that the module is well recognized with the command line :

    play help

You should see `i18n-extract` in the list of available commands :)

Usage
-----

### i18n-extract

"i18n-extract" will parse your application's files to find internationalized strings, and add missing strings to your
messages files.

What it will do :

1. Find all the `*.java` files in your `app` directory, looking for `Messages.get("...")`.
2. Find all the files in your `app/views` directory, looking for `&{'...'` and `messages.get('...')` (double quotes work too, 
   of course).
3. In all your messages files (`conf/messages` + every `conf/messages.LANG` file, depending on your `application.langs` option),
   add all the previously found strings missing, with an empty translation.

What it won't do :

* It won't smartly analyze your code, detect and resolve variables, or things like that.
* It won't auto-translate your strings :)

To use it, launch "i18n-extract" command from your application's directory :

    play i18n-extract

Sample output :

    ~        _            _
    ~  _ __ | | __ _ _  _| |
    ~ | '_ \| |/ _' | || |_|
    ~ |  __/|_|\____|\__ (_)
    ~ |_|            |__/
    ~
    ~ play! 1.1-beta2, http://www.playframework.org
    ~
    ~ Extracting i18n strings from Java files [Messages.get("...")] ...
    ~ Found 10 i18n string(s) in 30 Java file(s)...
    ~ Extracting i18n strings from templates [&{'...'...}] ...
    ~ Found 1 i18n string(s) in 12 view file(s)...
    ~ Found 11 i18n string(s) in your application, now let's fill up your messages files !
    ~ conf\messages : 11 string(s) added
    ~ conf\messages.fr : 0 string(s) added
    ~ conf\messages.en : 0 string(s) added
