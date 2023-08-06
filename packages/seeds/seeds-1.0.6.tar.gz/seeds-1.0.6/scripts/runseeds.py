#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to perform a SEEDS experiment.  For more information, run with the
--help argument.  Plugin directories can be specified in the configuration as
well as in the $SEEDSPLUGINPATH environment variable, which allows for a user-
or system-wide repository of plugins.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.6"
__credits__ = "Brian Connelly"

import seeds as S
from optparse import OptionParser

import os
import re
import sys

class ProgressBar:
    def __init__(self, min_value = 0, max_value = 0, width=60):
        self.bar = ''
        self.min = min_value
        self.max = max_value
        self.width = width
        self.amount = 0       # When amount == max, we are 100% done
        self.update_amount(0)

    def update_amount(self, new_amount = None):
        """
        Update self.amount with 'new_amount', and then rebuild the bar
        string.
        """
        if not new_amount: new_amount = self.amount
        if new_amount < self.min: new_amount = self.min
        if new_amount > self.max: new_amount = self.max
        self.amount = new_amount
        self.build_bar()

    def build_bar(self):
        """
        Figure new percent complete, and rebuild the bar string base on
        self.amount.
        """
        diff = float(self.amount - self.min)
        span = self.max - self.min
        percent_done = int(round((diff / float(span)) * 100.0))

        # figure the proper number of 'character' make up the bar
        all_full = self.width - 2
        num_hashes = int(round((percent_done * all_full) / 100))

        # build a progress bar with self.char and spaces (to create a
        # fixed bar (the percent string doesn't move)
        percent_str = "epoch: " + str(self.amount)
        self.bar = '#' * num_hashes + ' ' * (all_full-num_hashes)
        self.bar = '[' + self.bar + '] ' + percent_str

    def __str__(self):
        return str(self.bar)


def main():

    parser = OptionParser('usage: %prog [options] arg')
    parser.add_option("-c", "--config", dest="configfile", type="string", default="seeds.cfg",
                      help="read config file (default: seeds.cfg)")
    parser.add_option("-C", "--genconfig", action="store_true", dest="genconfig", help="write config file used (experiment.cfg)")
    parser.add_option("-d", "--data_dir", dest="datadir", type="string", default="data",
                      help="write data to this directory (default: data)")
    parser.add_option("-p", "--param", dest="params", type="string", help="Set config values.  Semicolon-separated list of section.param=val")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", help="suppress all output messages")
    parser.add_option("-r", "--resume", dest="snapfile", type="string", help="resume experiment from the provided snapshot file")
    parser.add_option("-s", "--seed", dest="seed", type=int, default=0,
                      help="set random seed (default: use clock)")
    parser.add_option("-S", "--snapshot", action="store_true", dest="snapshot", help="write snapshot file at end of experiment")
    parser.add_option("-v", "--version", action="store_true", dest="version", help="display version information and quit")

    (cmd_options, cmd_args) = parser.parse_args()

    if cmd_options.seed > 0:
        random_seed = cmd_options.seed
    else:
        random_seed=-1

    if cmd_options.version:
        print "%s (SEEDS Version %s)" % (__version__, S.__version__)
        sys.exit(0)

    # Create the world...
    # TODO: what if data_dir is set in config file?
    world = S.World(configfile=cmd_options.configfile, seed=random_seed)
    world.config.set('Experiment', 'data_dir', cmd_options.datadir)


    # Load the state of the world from a snapshot
    if cmd_options.snapfile:
        if not os.path.exists(cmd_options.snapfile):
            print "Error: Snapshot file does not exist"
            sys.exit(1)
        world.load_snapshot(cmd_options.snapfile)


    # Add command-line config options
    if cmd_options.params != None:
        options = re.split("\s*;\s*", cmd_options.params)
        for opt in options:
            # This is perhaps not the best regexp for comma-separated lists as values... need spaces.
            m = re.match(r"(?P<section>[A-Za-z0-9:_]+)\.(?P<parameter>[A-Za-z0-9:_]+)\s*=\s*(?P<value>-?[A-Za-z0-9_\.\,]+)", opt)
            if m != None:
                #print "Setting [%s]%s=%s" % (m.group("section"), m.group("parameter"), m.group("value"))
                world.config.set(m.group("section"), m.group("parameter"), m.group("value"))
            else:
                print "Error: Could not parse parameter setting", opt


    # Get the current configured list of plugin directories
    cfg_plugindirs = world.config.get(section="Experiment", name="plugin_dirs",
                                      default="")
    if len(cfg_plugindirs) > 0:
        plugindirs = world.config.get(section="Experiment", name="plugin_dirs").split(",")
    else:
        plugindirs = []

    # Add any plugin paths specified in the environment via $SEEDSPLUGINPATH
    seedspluginpath = os.environ.get("SEEDSPLUGINPATH")
    if seedspluginpath != None and len(seedspluginpath) > 0:
        for p in seedspluginpath.rsplit(":"):
            pdir = os.path.expanduser(p)
            plugindirs.append(pdir)

    if len(plugindirs) > 0:
        pdirs = ",".join(plugindirs)
        world.config.set(section="Experiment", name="plugin_dirs", value=pdirs)

    # Do the experiment...
    prog = ProgressBar(0, world.config.getint('Experiment', 'epochs'))
    oldprog = str(prog)

    while world.proceed:
        prog.update_amount(world.epoch)
        if not cmd_options.quiet and oldprog != str(prog):
            print prog, "\r",
            sys.stdout.flush()
            oldprog=str(prog)

        world.update()

    # Write a config file
    if cmd_options.genconfig:
        world.config.write(filename='experiment.cfg')

    # Write a snapshot at the end
    if cmd_options.snapshot:
        snap = world.get_snapshot()
        snap.write()

    if not cmd_options.quiet:
        print

if __name__ == "__main__":
    main()

