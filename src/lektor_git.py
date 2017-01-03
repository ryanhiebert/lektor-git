# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from lektor.pluginsystem import Plugin
from lektor.publisher import Publisher, Command


class GitPublisher(Publisher):
    def publish(self, **extra):
        yield 'Adding files'
        for line in Command(['git', 'add', '.']):
            yield line

        yield 'Creating new commit'
        msg = 'Git Publisher commit on {}'.format(
            datetime.utcnow().isoformat())
        for line in Command(['git', 'commit', '-m', msg]):
            yield line

        yield 'Pushing changes'
        for line in Command(['git', 'push']):
            yield line


class GitPlugin(Plugin):
    name = 'Git'
    description = 'Publish your Lektor site with a Git Push.'

    def on_setup_env(self, **extra):
        self.env.add_publisher('git', GitPublisher)
