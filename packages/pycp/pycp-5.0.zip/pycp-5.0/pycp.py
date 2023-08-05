#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright (c) 2010 Dimitri Merejkowsky                                       #
#                                                                              #
# Permission is hereby granted, free of charge, to any person obtaining a copy #
# of this software and associated documentation files (the "Software"), to deal#
# in the Software without restriction, including without limitation the rights #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    #
# copies of the Software, and to permit persons to whom the Software is        #
# furnished to do so, subject to the following conditions:                     #
#                                                                              #
# The above copyright notice and this permission notice shall be included in   #
# all copies or substantial portions of the Software.                          #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,#
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN    #
# THE SOFTWARE.                                                                #
################################################################################


"""Little script to display progress bars
while transferring files from command line
"""

__author__ = "Yannick LM"
__author_email__  = "yannicklm1337 AT gmail DOT com"
__version__ = "5.0"


import os
import sys
import stat

from optparse import OptionParser

from progressbar import ProgressBar
from progressbar import Percentage
from progressbar import FileTransferSpeed
from progressbar import ETA
from progressbar import Bar

####
# Utilities functions:

def die(message):
    """An error occured.
    Write it to stderr and exit with error code 1

    """
    sys.stderr.write(str(message) + "\n")
    sys.exit(1)

def debug(message):
    """Useful for debug
    Messages will only be written if DEBUG env var is true

    """
    if os.environ.get("DEBUG"):
        print message

def samefile(src, dest):
    """Check if two files are the same in a
    crossplatform way

    """
    # If os.path.samefile exists, use it:
    if hasattr(os.path,'samefile'):
        try:
            return os.path.samefile(src, dest)
        except OSError:
            return False

    # All other platforms: check for same pathname.
    def normalise(path):
        """trying to be sure two paths are *really*
        equivalents

        """
        res = os.path.normcase(os.path.normpath(os.path.abspath(path)))
        return res

    return normalise(src) == normalise(dest)


def pprint_transfer(src, dest):
    """
    Directly borrowed from git's diff.c file.

    pprint_rename("/path/to/foo", "/path/to/bar")
    >>> /path/to/{foo => bar}
    """
    len_src = len(src)
    len_dest = len(dest)

    # Find common prefix
    pfx_length = 0
    i = 0
    j = 0
    while (i < len_src and j < len_dest and src[i] == dest[j]):
        if src[i] == os.path.sep:
            pfx_length = i + 1
        i += 1
        j += 1

    # Find common suffix
    sfx_length = 0
    i  = len_src - 1
    j = len_dest - 1
    while (i > 0 and j > 0 and src[i] == dest[j]):
        if src[i] == os.path.sep:
            sfx_length = len_src - i
        i -= 1
        j -= 1

    src_midlen  = len_src  - pfx_length - sfx_length
    dest_midlen = len_dest - pfx_length - sfx_length

    pfx   = src[:pfx_length]
    sfx   = dest[len_dest - sfx_length:]
    src_mid  = src [pfx_length:pfx_length + src_midlen ]
    dest_mid = dest[pfx_length:pfx_length + dest_midlen]

    if pfx == os.path.sep:
        # The common prefix is / ,
        # avoid print /{etc => tmp}/foo, and
        # print {/etc => /tmp}/foo
        pfx = ""
        src_mid  = os.path.sep + src_mid
        dest_mid = os.path.sep + dest_mid

    if not pfx and not sfx:
        return "%s => %s" % (src, dest)

    res = "%s{%s => %s}%s" % (pfx, src_mid, dest_mid, sfx)
    return res

class TransferError(Exception):
    """Custom exception: wraps IOError

    """
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


def transfer_file(options, src, dest, callback):
    """Transfer src to dest, calling
    callback(done, total) while doing so.

    src and dest must be two valid file paths.

    If "move" option is True, remove src when done.
    """
    if samefile(src, dest):
        die("%s and %s are the same file!" % (src, dest))
    try:
        src_file = open(src, "rb")
    except IOError:
        raise TransferError("Could not open %s for reading" % src)
    try:
        dest_file = open(dest, "wb")
    except IOError:
        raise TransferError("Could not open %s for writing" % dest)

    buff_size = 18 * 1024
    done = 0
    total = os.path.getsize(src)

    try:
        while True:
            data = src_file.read(buff_size)
            if not data:
                break
            done += len(data)
            callback(done, total)
            dest_file.write(data)
    except IOError, err:
        mess  = "Problem when transferring %s to %s\n" % (src, dest)
        mess += "Error was: %s" % err
        raise TransferError(mess)
    finally:
        src_file.close()
        dest_file.close()

    try:
        post_transfer(options, src, dest)
    except OSError, err:
        print "Warning: failed to finalize tranfer of %s: %s" % (dest, err)

    if options.move:
        try:
            debug("removing %s" % src)
            os.remove(src)
        except OSError:
            print "Warning: could not remove %s" % src


def post_transfer(options, src, dest):
    """Handle stat of transferred file

    By default, preserve only permissions.
    If "preserve" option was given, preserve also
    utime and flags.

    """
    src_st = os.stat(src)
    if hasattr(os, 'chmod'):
        mode = stat.S_IMODE(src_st.st_mode)
        os.chmod(dest, mode)
    if not options.preserve:
        return
    if hasattr(os, 'utime'):
        os.utime(dest, (src_st.st_atime, src_st.st_mtime))


class FileTransferManager():
    """This class contains the progressbar object.

    It also contains an options object, filled by optparse.

    It is initialized with a source and a destination, which
    should be correct files. (No dirs here!)

    """
    def __init__(self, options, src, dest):
        self.options = options
        self.src = src
        self.dest = dest
        self.pbar = None

    def do_transfer(self):
        """Print src->dest in a nice way, initialize progressbar,
        close it when done

        """
        # Handle overwriting of files:
        if os.path.exists(self.dest):
            should_skip = self.handle_overwrite()
            if should_skip:
                return

        print pprint_transfer(self.src, self.dest)
        self.pbar = ProgressBar(
          widgets = [
            Percentage()                          ,
            " "                                   ,
            Bar(marker='#', left='[', right=']' ) ,
            " - "                                 ,
            FileTransferSpeed()                   ,
            " | "                                 ,
            ETA() ])
        try:
            transfer_file(self.options, self.src, self.dest, self.callback)
        except TransferError, err:
            die(err)
        self.pbar.finish()

    def handle_overwrite(self):
        """Return True if we should skip the file.
        Ask user for confirmation if we were called
        with an 'interactive' option.

        """
        # Safe: always skip
        if self.options.safe:
            print "Warning: skipping", self.dest
            return True

        # Not safe and not interactive => overwrite
        if not self.options.interactive:
            return False

        # Interactive
        print "File: '%s' already exists" % self.dest
        print "Overwrite?"
        user_input = raw_input()
        if (user_input == "y"):
            return False
        else:
            return True

    def callback(self, done, total):
        """Called by transfer_file"""
        self.pbar.maxval = total
        self.pbar.update(done)


def recursive_file_transfer(options, sources, destination):
    """Go back to the simple case: copy one file to an other.

    """
    filenames    = [x for x in sources if os.path.isfile(x)]
    directories  = [x for x in sources if os.path.isdir (x)]

    for filename in filenames:
        _transfer_file(options, filename, destination)

    for directory in directories:
        _transfer_dir(options, directory, destination)


def _transfer_file(options, source, destination):
    """Copy a file to a destination.

    a_file, b_dir  => a_file, b_dir/a_file
    a_file, b_file => a_file, b_file
    """
    debug(":: file %s -> %s" % (source, destination))
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))

    tfm = FileTransferManager(options, source, destination)
    debug("=> %s -> %s" % (source, destination))
    tfm.do_transfer()


def _transfer_dir(options, source, destination):
    """Copy a dir to a destination

    """
    debug(":: dir %s -> %s" % (source, destination))
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))
    debug(":: making dir %s" % destination)
    os.mkdir(destination)
    file_names = sorted(os.listdir(source))
    if not options.all:
        file_names = [f for f in file_names if not f.startswith(".")]
    file_names = [os.path.join(source, f) for f in file_names]
    recursive_file_transfer(options, file_names, destination)
    if options.move:
        os.rmdir(source)


def main():
    """Parses command line arguments"""
    if sys.argv[0].endswith("pymv"):
        move = True
        prog_name = "pymv"
        action = "move"
    else:
        move = False
        prog_name = "pycp"
        action = "copy"

    usage = """
    %s [options] SOURCE DESTINATION
    %s [options] SOURCE... DIRECTORY

    %s SOURCE to DESTINATION or mutliple SOURCE(s) to DIRECTORY
    """ % (prog_name, prog_name, action)

    version = "%s version %s" % (prog_name, __version__)

    parser = OptionParser(usage, version=version, prog=prog_name)

    parser.add_option("-i", "--interactive",
            action  = "store_true",
            dest    = "interactive",
            help    = "ask before overwriting existing files")

    parser.add_option("-s", "--safe",
            action  = "store_true",
            dest    = "safe",
            help    = "never overwirte existing files")

    parser.add_option("-f", "--force",
            action  = "store_false",
            dest    = "safe",
            help    = "silently overwirte existing files " + \
                "(this is the default)")

    parser.add_option("-a", "--all",
            action = "store_true",
            dest   = "all",
            help  = "transfer all files (including hidden files")

    parser.add_option("-p", "--preserve",
            action = "store_true",
            dest   = "preserve",
            help   = "preserve time stamps while copying")

    parser.set_defaults(
        safe=False,
        interactive=False,
        all=False)

    (options, args) = parser.parse_args()
    options.move = move # This "option" is set by sys.argv[0]

    if len(args) < 2:
        parser.error("Incorrect number of arguments")

    sources = args[:-1]
    destination = args[-1]

    if len(sources) > 1:
        if not os.path.isdir(destination):
            die("%s is not an existing directory" % destination)

    for source in sources:
        if not os.path.exists(source):
            die("%s does not exist")

    try:
        recursive_file_transfer(options, sources, destination)
    except TransferError, err:
        die(err)
    except KeyboardInterrupt, err:
        die("Interrputed by user")


if __name__ == "__main__":
    main()
