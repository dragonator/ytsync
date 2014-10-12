import os

import taglib

from ytsync.executor import Executor


class Downloader:

    def __init__(self, streams, target_dir):
        self._streams = streams
        self._target_dir = target_dir

    @property
    def streams(self):
        return self._streams

    @property
    def target_dir(self):
        return self._target_dir

    def process_download(self):
        for stream in self._streams:
            message = "\nDownloading {}...".format(stream.title)
            print(message)
            stream.download(self.target_dir)

            song_full_path = '/'.join([self.target_dir,
                                      stream.title+'.'+stream.extension])

            self.remux(song_full_path)
            self.add_url_tag(song_full_path, stream.url)

    def remux(self, song_full_path):
        file_extension = song_full_path.rsplit('.', 1)[-1]
        file_path_without_extension = song_full_path.rsplit('.', 1)[0]

        print('\nRemuxing "{}"'.format(song_full_path))

        output_file_name =\
            file_path_without_extension + ".REMUXED." + file_extension
        Executor.execute(["ffmpeg", "-i", song_full_path, "-acodec",
                         "copy", "-vn", output_file_name])

        Executor.execute(["rm", song_full_path])
        os.rename(output_file_name, song_full_path)

    def add_url_tag(self, song_full_path, url_tag_value):
        tag_obj = taglib.File(song_full_path)
        tag_obj.tags['URL'] = url_tag_value
        # Replace URL with ID of the video.
        # The ID is extracted from the value of "_parent" key.
        tag_obj.save()
