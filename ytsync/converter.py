import os
import glob

from ytsync.executor import Executor

script_abs_path = os.path.dirname(os.path.abspath(__file__))


class Converter:

    def __init__(self, target_dir):
        self._target_dir = target_dir
        self._unsupported_formats = None
        self._files_to_convert = None

    @property
    def target_dir(self):
        return self._target_dir

    @property
    def unsupported_formats(self):
        if self._unsupported_formats is None:
            self.get_unsupported_formats()
        return self._unsupported_formats

    @property
    def files_to_convert(self):
        if self._files_to_convert is None:
            self.get_unsupported_files()
        return self._files_to_convert

    def get_unsupported_formats(self):
        self._unsupported_formats = []
        global script_abs_path
        dir = '{}'.format(os.sep)\
            .join([script_abs_path, 'settings', 'unsupported_formats'])
        with open(dir) as unsupported_formats:
            content = unsupported_formats.read()
            self._unsupported_formats = content.split('\n')

    def get_unsupported_files(self):
        self._files_to_convert = []
        os.chdir(self.target_dir)
        for format in self.unsupported_formats:
            self._files_to_convert += glob.glob('*.'+format)

    def process_conversion(self):
        print("\n\n")
        for song in self.files_to_convert:
            current_format = ".{}".format(song.rsplit('.', 1)[-1])

            old_file = '{}{}{}'.format(self.target_dir, os.sep, song)
            new_file = '{}{}{}'.format(self.target_dir, os.sep,
                                       song.replace(current_format, '.mp3'))

            message = "Converting {} to 'mp3' format...".format(old_file)
            print(message)

            Executor.execute(["avconv", "-i", old_file, new_file])
            print('Deleting "{}"'.format(old_file))
            Executor.execute(["rm", old_file])
