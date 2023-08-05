# VCS routines for musdex
#
# Copyright 2010 Max Battcher. Some rights reserved.
# Licensed for use under the Ms-RL. See attached LICENSE file.
from config import BASEDIR, load_index, save_index, save_config
from formatters import get_formatter
from handlers import get_handler
import datetime
import logging
import os
import os.path
import re
import shutil
import time

import vcs

def add(args, config):
    index = load_index(config)

    for archive in args.archive:
        archive = os.path.relpath(archive)
        if 'archives' in config \
        and any(arc['filename'] == archive for arc in config['archives']):
            logging.warn("Archive already configured: %s" % archive)
            continue

        handler = get_handler(args.handler)
        arch = handler(archive, os.path.join(BASEDIR, archive))
        if not arch.check():
            logging.error("Archive not supported by given handler: %s: %s" % (
                args.handler, archive))

        logging.info("Extracting archive for the first time: %s" % archive)
        files = handler.extract(force=True)
        for f, t in files:
            index[f] = t
            vcs.add_file(config, f)

        entry = {'filename': archive}
        if args.handler: entry['handler'] = args.handler
        if 'archives' not in config: config['archives'] = []
        config['archives'].append(entry)

    save_config(args, config)
    save_index(config, index)

def extract(args, config):
    index = load_index(config)
    index_updated = False

    fmts = []
    if 'post_extract' in config:
        logging.debug("Compiling post-extraction regular expressions")
        fmts = [(re.compile(regex), get_formatter(fname)) \
            for regex, fname in config['post_extract']]

    if args.archive: args.archive = map(os.path.relpath, args.archive)

    manifest = vcs.manifest(config)

    for archive in config['archives']:
        arcf = archive['filename']
        arcloc = os.path.join(BASEDIR, arcf)
        if args.archive and arcf not in args.archive:
            continue

        # Check if up to date
        arct = datetime.datetime(*time.localtime(os.path.getmtime(arcf))[:6])
        if not args.force and arcloc in index and arct <= index[arcloc]:
            continue

        arcman = dict((f, index[f] if f in index else None) \
            for f in manifest if f.startswith(arcloc))

        hname = archive['handler'] if 'handler' in archive else None
        handler = get_handler(hname)
        arch = handler(arcf, arcloc, manifest=arcman)
        files = arch.extract(force=args.force or arcloc not in index)
        if files: index_updated = True

        for f, t in files:
            index[f] = t
            for regex, fmt in fmts: # post-extract formatters
                if regex.match(f):
                    logging.debug("Post-extraction: %s(%s)" % (fmt, f))
                    fmt(f)
            if f != arcloc and f not in arcman: vcs.add_file(config, f)
            
    if index_updated: save_index(config, index)

def combine(args, config):
    index = load_index(config)
    index_updated = False

    if args.archive: args.archive = map(os.path.relpath, args.archive)

    manifest = vcs.manifest(config)

    for archive in config['archives']:
        arcf = archive['filename']
        arcloc = os.path.join(BASEDIR, arcf)
        if args.archive and arcf not in args.archive:
            continue

        bakfilename = None
        if 'backup' not in config or config['backup']:
            logging.debug('Backing up %s' % arcf)
            bakfilename = arcf + '.bak~'
            shutil.copyfile(arcf, bakfilename)

        arcman = dict((f, index[f] if f in index else None) \
            for f in manifest if f.startswith(arcloc))

        hname = archive['handler'] if 'handler' in archive else None
        handler = get_handler(hname)
        arch = handler(arcf, arcloc, manifest=arcman)
        files = arch.combine(force=args.force or arcloc not in index)
        if files: index_updated = True

        for f, t in files:
            index[f] = t

        # TODO: Check for deleted files?

        if bakfilename is not None and ('leave_backups' not in config
        or not config['leave_backups']):
            logging.debug('Removing backup %s' % bakfilename)
            os.remove(bakfilename)

    if index_updated: save_index(config, index)

# vim: ai et ts=4 sts=4 sw=4
