from __future__ import absolute_import
from lektor.publisher import Command
from lektor_git import GitPublisher, GitPlugin


class TestGitPublisher(object):
    def test_normal_path(self, tmpdir, monkeypatch, mocker):
        # Make origin repository
        origin = tmpdir.mkdir('origin')
        monkeypatch.chdir(origin)
        Command(['git', 'init']).wait()

        origin.join('testfile.txt').write('This is Test A.')
        Command(['git', 'add', '.']).wait()
        Command(['git', 'commit', '-m', 'Initial commit']).wait()
        assert origin.join('testfile.txt').read() == 'This is Test A.'

        # Before we leave the parent repository,
        # Set it to allow pushes to branches it has checked out.
        Command(['git', 'config', 'receive.denyCurrentBranch', 'ignore'])

        # Make clone repository
        monkeypatch.chdir(tmpdir)
        Command(['git', 'clone', 'origin', 'clone']).wait()

        # Make a change
        clone = tmpdir.join('clone')
        monkeypatch.chdir(clone)
        clone.join('testfile.txt').write('This is Test B.')

        # At this point the clone repository should be dirty,
        # with changes ready to be committed and pushed.
        env, output_path = mocker.Mock(), 'output_path.txt'
        list(GitPublisher(env, output_path).publish())

        # Check that the file has changed as expected in origin.
        # Reset the working directory, then check the file.
        monkeypatch.chdir(origin)
        Command(['git', 'reset', '--hard']).wait()
        assert origin.join('testfile.txt').read() == 'This is Test B.'

    def test_no_change(self, tmpdir, monkeypatch, mocker):
        # Make origin repository
        origin = tmpdir.mkdir('origin')
        monkeypatch.chdir(origin)
        Command(['git', 'init']).wait()

        origin.join('testfile.txt').write('This is Test A.')
        Command(['git', 'add', '.']).wait()
        Command(['git', 'commit', '-m', 'Initial commit']).wait()
        assert origin.join('testfile.txt').read() == 'This is Test A.'

        # Before we leave the parent repository,
        # Set it to allow pushes to branches it has checked out.
        Command(['git', 'config', 'receive.denyCurrentBranch', 'ignore'])

        # Make clone repository
        monkeypatch.chdir(tmpdir)
        Command(['git', 'clone', 'origin', 'clone']).wait()

        # At this point the clone repository should still be clean,
        # as no changes were made. The push will still happen.
        env, output_path = mocker.Mock(), 'output_path.txt'
        list(GitPublisher(env, output_path).publish())

        # Check that the file has not changed as expected in origin.
        # Reset the working directory, then check the file.
        monkeypatch.chdir(origin)
        Command(['git', 'reset', '--hard']).wait()
        assert origin.join('testfile.txt').read() == 'This is Test A.'


class TestGitPlugin(object):
    def test_on_setup_env(self, mocker):
        env = mocker.Mock()
        plugin = GitPlugin(env, 'id')
        plugin.on_setup_env()
        env.add_publisher.assert_called_once_with('git', GitPublisher)
