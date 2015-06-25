import os
import glob
from .executor import Executor


class Downloader:

    def __init__(self, streams, target_dir):
        self.streams = streams
        self.target_dir = target_dir
        self.playlist_name = target_dir.rsplit(os.sep)[-1]

    @property
    def streams(self):
        return self.streams

    @property
    def target_dir(self):
        return self.target_dir

    def process_download(self):
        print('\nSyncing playlist "{}":\n'.format(self.playlist_name))
        if not os.path.exists(self.target_dir):
            os.mkdir(self.target_dir)

        os.chdir(self.target_dir)
        songs_in_dir = glob.glob("*")
        for index, stream in enumerate(self.streams):
            if (stream.title.encode("ascii", "ignore")+".mp3") in songs_in_dir:
                message = u"Skipping {}".format(stream.title)
                Executor.print_utf(message)
                continue

            message = u"Downloading {} ...".format(stream.title)
            Executor.print_utf(message)
            stream.download(self.target_dir, meta=True,
                            remux_audio=True, quiet=True)
