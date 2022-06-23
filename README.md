# csvconcat
Python recursive csv concatenator - built to serve a specific need but maybe someone else will find it useful too.

This is a super simple project that takes a path where csv files can be found, potentially deeply nested and concatenates them into a new file.

Headers are assumed to be the same across each file. There's not much in the way of error handling and the command line option parsing is exceptionally basic.

Might package it if there's ever any call for it.

Usage:
python3 csvconcat.py path-to-source-directory target-file-name
