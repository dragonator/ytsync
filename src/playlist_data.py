import re

import pafy


class PlaylistData:
    UNSUPPORTED_CHARS = ['\\', '/', '?', '*', '"', ':', '<', '>', '#', '%']

    def __init__(self, url):
        self._url = url
        self._songs_names = None
        self._best_streams = None
        self._pafy_data = None

    @property
    def url(self):
        return self._url

    @property
    def songs_names(self):
        if self._songs_names is None:
            self.get_songs_names()
        return self._songs_names

    @property
    def best_streams(self):
        if self._best_streams is None:
            self.get_best_streams()
        return self._best_streams

    @property
    def pafy_data(self):
        if self._pafy_data is None:
            self.get_pafy_data()
        return self._pafy_data

    def get_pafy_data(self):
        print('Getting playlist information...')
        self._pafy_data = pafy.get_playlist(self.url)

    def get_best_streams(self):
        self._best_streams = []
        for element in self.pafy_data['items']:
            try:
                curr_elem_best_stream = element['pafy'].getbestaudio()
            except (IOError, OSError) as msg:
                video_id = element["pafy"].videoid
                video_title = element["pafy"].title

                msg = re.sub(r"\[{}\]".format(video_id),
                             r"\n[{}]".format(video_title),
                             str(msg))
                print(msg)
            except (KeyError, ValueError):
                continue

            if curr_elem_best_stream is not None:
                self._best_streams.append(curr_elem_best_stream)

    def get_songs_names(self):
        self._songs_names = []
        for stream in self.best_streams:
            self._songs_names.append(stream.title)

    @classmethod
    def normalize_names(cls, streams_list):
        for stream in streams_list:
            for char in cls.UNSUPPORTED_CHARS:
                stream._title = stream.title.replace(char, '')

        return streams_list
