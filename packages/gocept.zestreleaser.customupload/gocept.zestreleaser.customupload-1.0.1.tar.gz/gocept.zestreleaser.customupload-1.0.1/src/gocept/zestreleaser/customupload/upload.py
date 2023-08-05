# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import ConfigParser
import os
import zest.releaser.utils


def upload(context):
    destination = choose_destination(context['name'], read_configuration())
    if not destination:
        return
    if not zest.releaser.utils.ask('Upload to %s' % destination):
        return

    tarball = '%s-%s.tar.gz' % (context['name'], context['version'])
    src = os.path.join(context['tagdir'], 'dist', tarball)
    os.system(' '.join(['scp', src, destination]))


def read_configuration():
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser('~/.pypirc'))
    return config


def choose_destination(package, config):
    SECTION = 'gocept.zestreleaser.customupload'
    if SECTION not in config.sections():
        return None
    items = sorted(config.items(SECTION), key=lambda x: len(x[0]),
                   reverse=True)
    for prefix, destination in items:
        if package.startswith(prefix):
            return destination
    return None
