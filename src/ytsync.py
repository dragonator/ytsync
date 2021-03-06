#!/usr/bin/env python
import os
import sys
from argparse import ArgumentParser

script_abs_path = os.path.dirname(os.path.abspath(__file__))
script_parent_dir = script_abs_path.rsplit(os.sep, 1)[0]
sys.path.append(script_parent_dir)

from playlist_data import PlaylistData
from downloader import Downloader
# from converter import Converter


def parse_arguments():
    """
    Parsing command line arguments in suitable and easy to use format.
    """
    script_description = """
    If you use the script without any options it will
    use the "sync_lis" file.
    """
    args_parser = ArgumentParser(description=(script_description))
    args_parser.add_argument('-u', '--url',
                             help=('Url to the playlist '
                                   'which to be downloaded.'))
    args_parser.add_argument('-t', '--target-dir',
                             help=('Target directory for '
                                   'downloading files.'))
    args_parser.add_argument('-c', '--convert_to',
                             help=('When files have been downloaded '
                                   'they will be converted to the given '
                                   'file format.'))
    args_parser.add_argument('-q', '--quite',
                             help=('Normal quite mode - no outut will be '
                                   'printed out.'))

    return vars(args_parser.parse_args())


def process_playlist_sync(url, target_dir):
    if not os.path.exists(target_dir):
        print('Directory "{}" does not exists !'.format(target_dir))
        return

    playlist_data = PlaylistData(url)
    streams_to_download = playlist_data.best_streams
    streams_to_download = playlist_data.normalize_names(streams_to_download)

    playlist_title = playlist_data._pafy_data['title']
    playlist_dir = '{}{}{}'.format(target_dir, os.sep, playlist_title)

    downloader = Downloader(streams_to_download, playlist_dir)
    downloader.process_download()

    print("\nSkipping converting.")
    # converter = Converter(playlist_dir)
    # converter.process_conversion()

    print('Syncing of playlist "{}" has completed.'.format(playlist_title))


def process_sync_list(sync_list_abs_path=os.sep.join([script_abs_path,
                                                      'settings',
                                                      'sync_list.txt'])):
    if not os.path.exists(sync_list_abs_path) or\
       os.stat(sync_list_abs_path).st_size == 0:
        print("Sync list is empty.")
        return

    with open(sync_list_abs_path, 'r') as sync_list_file:
        records = sync_list_file.read().split('\n\n')
        sync_list = []
        for record in records:
            splitted = record.split('\n')
            sync_list.append({'url': splitted[0], 'target_dir': splitted[1]})

    if sync_list is not None:
        for playlist_data in sync_list:
            process_playlist_sync(playlist_data['url'],
                                  playlist_data['target_dir'])


def main():
    given_args = parse_arguments()
    url = given_args['url']
    target_dir = given_args['target_dir']

    if url is not None and target_dir is not None:
        process_playlist_sync(url, target_dir)
    else:
        process_sync_list()

if __name__ == '__main__':
    main()
