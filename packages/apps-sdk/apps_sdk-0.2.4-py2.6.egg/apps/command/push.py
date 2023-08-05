#
# Copyright (c) 2010 BitTorrent Inc.
#

import boto.s3
import logging
import os
import urllib

import apps.command.base

class push(apps.command.base.Command):

    help = 'Push the packaged project to a remote resource.'
    user_options = [
        ('aws-secret=', None, 'aws secret for S3 upload', None),
        ('aws-key=', None, 'aws key for S3 upload', None),
        ('url=', None, 'url to upload to', None)
        ]
    default_options = { 'path': '' }
    pre_commands = [ 'package' ]

    def run(self):
        if not 'url' in self.options:
            logging.error('Must include an url to upload to. ' \
                              '(ex. s3://apps.bittorrent.com/foo/bar.btapp')
            return
        protocol = self.options['url'].split(':')[0]
        try:
            getattr(self, 'push_%s' % (protocol,))()
        except AttributeError:
            logging.error('The <%s> protocol is not supported. ' \
                              'Supported protocols are %s' % (
                    protocol, ','.join([x.split('_')[-1] for x in
                                        filter(lambda x: x.startswith('push_'),
                                               dir(self))])))
            return

    def package_name(self):
        extension = 'pkg' if self.project.metadata.get(
            'bt:package', False) else 'btapp'
        return os.path.join('dist', '%s.%s' % (self.project.metadata['name'],
                                               extension))

    def push_s3(self):
        base_url = self.options['url'][5:]
        bucket, fname = base_url.split('/', 1)
        if not 'aws-secret' in self.options:
            logging.error('Must include your aws secret. (--aws-secret)')
            return
        if not 'aws-key' in self.options:
            logging.error('Must include your aws key. (--aws-key)')
            return
        conn = boto.connect_s3(self.options['aws-key'],
                               self.options['aws-secret'])
        try:
            bucket = conn.get_bucket(bucket)
        except:
            bucket = conn.create_bucket(bucket)
        key = bucket.new_key(fname)
        acl = key.get_acl() if key.exists() else None
        key.set_contents_from_filename(self.package_name(), replace=True)
        if acl:
            key.set_acl(acl)
