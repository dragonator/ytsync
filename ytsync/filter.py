import os
# import taglib
import glob


class Filter:

    @classmethod
    def remove_present_streams(cls, streams_list, target_dir):
        present_streams = Filter.get_present_streams_urls(target_dir)
        filtered_streams_list = []
        for stream in streams_list:
            if stream.url not in present_streams:
                filtered_streams_list.append(stream)

        return filtered_streams_list

    @classmethod
    def get_present_streams_urls(cls, target_dir):
        os.chdir(target_dir)
        target_dir_files = glob.glob('*')
        present_streams = []
        for item in target_dir_files:
            try:
                tags_obj = taglib.File(item)
                present_streams.append(tags_obj.tags['URL'])
            except OSError:
                print('Skipping file "{}".The file type is not supported')
            except KeyError:
                import pdb; pdb.set_trace()

        return present_streams
