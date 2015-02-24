import os
import glob


class Downloader:

    def __init__(self, streams, target_dir):
        self._streams = streams
        self._target_dir = target_dir
        self._playlist_name = target_dir.rsplit(os.sep)[-1]

    @property
    def streams(self):
        return self._streams

    @property
    def target_dir(self):
        return self._target_dir

    def process_download(self):
        print('\nSyncing playlist "{}":\n'.format(self._playlist_name))
        if not os.path.exists(self._target_dir):
            os.mkdir(self._target_dir)

        for stream in self._streams:
            os.chdir(self._target_dir)
            songs_in_dir = glob.glob("*")

            if (stream.title+".mp3") in songs_in_dir:
                print("Skipping {}".format(stream.title))
                continue

            print("Downloading {} ...".format(stream.title))
            stream.download(self._target_dir)
