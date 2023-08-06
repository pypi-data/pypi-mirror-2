Installation instructions
=========================

Install virtualenv
---------------------

projectenv depends on virtualenv, so make sure you have virtualenv installed.

    $ easy_install virtualenv

Install projectenv
----------------------------

    $ pip install projectenv

_pip comes with virtualenv and is the preferred package manager to use
with virtualenv_

Edit your shell's configuration file
---------------------------------------

If your shell is Bourne shell compatible (bash, ksh, zsh, etc.), then add the
following lines to your config file:

    export PROJECTENV_HOME=$HOME/.projectenv
    source $PROJECTENV_HOME/bin/projectenv.sh

If your shell is C shell compatible (csh, tcsh, etc.), then add the following
lines to your config file:

    setenv PROJECTENV_HOME $HOME/.projectenv
    alias projectenv 'source $PROJECTENV_HOME/bin/projectenv.csh \!*'

Source your shell's configuration file
--------------------------------------

Finally, you need to source your shell's configuration file to make the
changes take effect. The name of this file varies depending on the shell
you are using, so consult your shell's documentation if you are unsure
where it is.

    $ source ~/.bashrc # (or ~/.tcshrc, ~/.profile, etc.)

You're done!
---------------

Go have fun creating virtual environments for your project with projectenv.
See the
[README](https://github.com/teaminsight/projectenv/blob/master/README.markdown)
file for usage instructions.

Updating
--------

projectenv is an active development, so be sure to check back from time
to time and install the latest updates.

    $ projectenv off # upgrade should be done outside of any active virtualenvs
    $ pip install --upgrade projectenv
    $ source ~/.bashrc # (or ~/.tcshrc, ~/.profile, etc.)
