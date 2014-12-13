Mocca
=====

Mocca is a simple meta-checkout tool for managing projects which are split into several different repositories. The tool
was inspired by Google's gclient.


How to use
==========

Clone this repository and add the directory to your PATH environment variable.

`cd` into your project's root directory and run `mocca init`. This will generate an empty .mocca project description file
in your current directory.<br>
All other Mocca commands require an existing and writable `.mocca` file. The tool will search up the directory structure
until it finds a valid `.mocca` or throw an error at you if it doesn't find a suitable project configuration.

mocca add
---------
To add a repository (Mocca calls it dependency) to your configuration simply run `mocca add local-checkout-path repo-url`.<br>
This will add a new entry to your .mocca file.

The `local-checkout-path` is the directory where the repository should be cloned into. Relative paths will be evaluated
relative to the directory of your `.mocca` file.

`repo-url` is simply the URL of the repository to clone.

By default Mocca will assume that the repository uses `git`. To tell Mocca to use `hg` simply add `--vcs=hg` to your
`mocca add` call, like this `mocca add --vcs=hg local-checkout-path repo-url`

You can also specify the branch which you want to clone using `--branch=cool-branch-name`. The tool will assume `master`
for git repositories and `default` for hg repositories by default.

Mocca does also support specifying target OSs for each repository. Simply add `-t target-os-name`.<br>
`mocca add -t=posix path url` for example will make sure the repository is ignored on all platforms but posix.

mocca add-var
-------------
Another nice feature are project variables.

Mocca will replace all occurrences of `{{VARIABLE_NAME}}` with the value of `VARIABLE_NAME`.

This basically allows you to either define shorthands for long expressions or pull in environment variables. `mocca get-var`
takes two arguments. The first one is the name of the variable, the second is the variable's value.<br>
Note: `<(env` is a special value. It tells Mocca to pull the actual value in from the system environment.

mocca dump
----------
`mocca dump` allows you to dump the project configuration. You can set the `--interpolate` (short `-i`) flag to enable
variable interpolation in the output.

mocca sync
----------
This is the command you will probably use most since it does the actual work the tool was designed for. `mocca sync` will
make sure the repositories specified in your project configuration are cloned and up to date. What it basically does is
calling `git/hg clone` if the repository hasn't been cloned yet or `git pull`/`hg pull -u` if the repository exists.


.mocca File Syntax
==================
Mocca stores the project configuration in the JSON format. You can edit the `.mocca` file using whichever text editor you
like. The file format is pretty straight forward and should be self explanatory.


Author, Bugs, Feature Requests
==============================
You can contact me either through github directly or by tweeting [@monofraps](https://twitter.com/monofraps) on Twitter.

Don't mind opening tickets for bugs and features requests. If you think you've made an improvement to Mocca that's worth
sharing send me a pull request.
