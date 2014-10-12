import os

# import taglib

from ytsync.executor import Executor


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
            song_full_path = '/'.join([self._target_dir,
                                      stream.title+'.'+stream.extension])

            # if os.path.exists(song_full_path):
            #     print("Skipping {}".format(stream.title))
            #     continue

            print("\n Downloading {}...".format(stream.title))
            stream.download(self._target_dir)

            self.remux(song_full_path)
            # self.add_url_tag(song_full_path, stream.url)

    def remux(self, song_full_path):
        file_extension = song_full_path.rsplit('.', 1)[-1]
        file_path_without_extension = song_full_path.rsplit('.', 1)[0]

        print('\nRemuxing "{}"'.format(song_full_path))

        output_file_name =\
            file_path_without_extension + ".REMUXED." + file_extension
        Executor.execute(["avconv", "-i", song_full_path, "-acodec",
                         "copy", "-vn", output_file_name])

        Executor.execute(["rm", song_full_path])
        os.rename(output_file_name, song_full_path)

    def add_url_tag(self, song_full_path, url_tag_value):
        tag_obj = taglib.File(song_full_path)
        tag_obj.tags['URL'] = url_tag_value
        # Replace URL with ID of the video.
        # The ID is extracted from the value of "_parent" key.
        tag_obj.save()
