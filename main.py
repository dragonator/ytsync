#!/usr/bin/env python
import os
import sys
import time
from functools import partial

import kivy
kivy.require('1.7.2')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
__version__ = '1.0'


class TestApp(App):

    def build(self):
        self.visible_layout = FloatLayout()
        sync_button = Button(text='SYNC PLAYLISTS LIST')

        edit_button = Button(text='EDIT SYNC LIST')
        edit_button.bind(on_press=self.open_sync_list_to_edit)

        url_label = Label(text='Playlist URL:')
        url_input = TextInput()

        target_dir_label = Label(text='Download in:')
        target_dir_input = TextInput()

        download_button = Button(text='DOWNLOAD PLAYLIST')

        self.major_layout = BoxLayout(orientation='vertical')
        self.major_layout.add_widget(sync_button)
        self.major_layout.add_widget(edit_button)
        self.major_layout.add_widget(url_label)
        self.major_layout.add_widget(url_input)
        self.major_layout.add_widget(target_dir_label)
        self.major_layout.add_widget(target_dir_input)
        self.major_layout.add_widget(download_button)

        self.visible_layout.add_widget(self.major_layout)
        return self.visible_layout

    def open_sync_list_to_edit(self, value):
        self.sync_list_layout = BoxLayout(orientation='vertical')

        content_textinput = TextInput(text=self.get_sync_list_content())

        buttons_layout = BoxLayout()
        save_button = Button(text='Save')
        save_button.bind(on_release=partial(self.switch_to, self.major_layout))
        buttons_layout.add_widget(save_button)
        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_release=partial(self.switch_to, self.major_layout))
        buttons_layout.add_widget(cancel_button)

        self.sync_list_layout.add_widget(content_textinput)
        self.sync_list_layout.add_widget(buttons_layout)

        self.visible_layout.add_widget(self.sync_list_layout)

    def switch_to(self, widget, _):
        self.visible_layout.clear_widgets()
        self.visible_layout.add_widget(widget)

    def save_sync_list_content(self, content):
        sync_list_path = \
            os.sep.join([self.user_data_dir, 'settings', 'sync_list.txt'])
        with open(sync_list_path, 'w') as sync_file:
            sync_file.write(content)

    def remove_childrens(self, widget, _):
        widget.clear_widgets()

    def get_sync_list_content(self):
        sync_list_path = \
            os.sep.join([self.user_data_dir, 'settings', 'sync_list.txt'])
        if os.path.exists(sync_list_path):
            with open(sync_list_path, 'r') as sync_list_file:
                return sync_list_file.read()
        else:
            os.makedirs(sync_list_path.rsplit(os.sep, 1)[0])
            open(sync_list_path, 'w').close()
            return ''


if __name__ == '__main__':
    TestApp().run()
