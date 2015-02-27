#!/usr/bin/env python
import os
import sys
from threading import Thread
from functools import partial

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.garden.filebrowser import FileBrowser
import logging
from kivy.logger import Logger
from kivy.lang import Builder
kivy.require('1.7.2')
__version__ = '1.0'

from src.ytsync import process_sync_list, process_playlist_sync


Builder.load_string('''
<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
''')

Logger.setLevel(logging.ERROR)


class ScrollableLabel(ScrollView):
    text = StringProperty('')

    def write(self, to_print):
        current_text = self.text
        new_text = current_text + str(to_print)
        self.text = new_text


class TestApp(App):

    def __init__(self, **kwargs):
        self.threads = []
        super(TestApp, self).__init__(on_stop=self.on_stop, **kwargs)

    def process_sync_list_wrapper(self,  _):
        sync_list_path = self.get_sync_list_fullpath()
        thread_func = partial(process_sync_list, sync_list_path)
        sync_thread = Thread(target=thread_func)
        self.threads.append(sync_thread)
        sync_thread.start()

    def process_playlist_sync_wrapper(self, _):
        url = self.get_textinput_content(self.url_input)
        target_dir = self.get_textinput_content(self.target_dir_input)
        thread_func = partial(process_playlist_sync, url, target_dir)
        sync_thread = Thread(target=thread_func)
        self.threads.append(sync_thread)
        sync_thread.start()

    def build(self):
        self.visible_layout = BoxLayout(oriantation='vertical')
        sync_button = Button(text='SYNC PLAYLISTS LIST')
        sync_button.bind(on_release=partial(self.process_sync_list_wrapper))
        edit_button = Button(text='EDIT SYNC LIST')
        edit_button.bind(on_press=self.open_sync_list_to_edit)
        sync_layout = BoxLayout()
        sync_layout.add_widget(sync_button)
        sync_layout.add_widget(edit_button)

        url_label = Label(text='Playlist URL:')
        self.url_input = TextInput(multiline=False)

        target_dir_label = Label(text='Download in:')
        self.target_dir_input = TextInput(multiline=False)
        target_dir_browse = Button(text='Browse')
        target_dir_browse.bind(on_release=partial(self.open_dir_browser))
        label_layout = BoxLayout()
        label_layout.add_widget(target_dir_label)
        label_layout.add_widget(target_dir_browse)

        download_button = Button(text='DOWNLOAD PLAYLIST')
        download_button.bind(on_release=self.process_playlist_sync_wrapper)

        output_label = ScrollableLabel()
        sys.stdout = output_label

        self.major_layout = BoxLayout(orientation='vertical',
                                      pos_hint={'top': 1})
        self.major_layout.add_widget(sync_layout)
        self.major_layout.add_widget(url_label)
        self.major_layout.add_widget(self.url_input)
        self.major_layout.add_widget(label_layout)
        self.major_layout.add_widget(self.target_dir_input)
        self.major_layout.add_widget(download_button)

        output_layout = BoxLayout(size_hint_y=6, padding=[5, 5, 5, 5])
        output_layout.add_widget(output_label)
        self.major_layout.add_widget(output_layout)
        self.visible_layout.add_widget(self.major_layout)

        return self.visible_layout

    def open_dir_browser(self, _):
        browser = FileBrowser(select_string='Select Dir')
        browser.dirselect = BooleanProperty(True)
        browser.bind(on_success=partial(self.select_dir),
                     on_canceled=partial(self.switch_to, self.major_layout),
                     on_submit=partial(self.select_dir))
        self.switch_to(browser, '')

    def select_dir(self, browser_instance):
        selection = str(browser_instance.selection)[3:-2]
        if not os.path.isdir(selection):
            selection = selection.rsplit(os.sep, 1)[0]

        print(selection)
        self.target_dir_input.setter('text')('', selection)
        self.switch_to(self.major_layout, '')

    def open_sync_list_to_edit(self, value):
        self.sync_list_layout = BoxLayout(orientation='vertical')

        content_textinput = TextInput(text=self.get_sync_list_content())

        buttons_layout = BoxLayout()
        buttons_layout.size_hint = (1, 0.1)
        save_button = Button(text='Save')
        save_button.bind(on_release=partial(self.save_sync_list_content,
                                            content_textinput))
        buttons_layout.add_widget(save_button)
        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_release=partial(self.switch_to,
                                              self.major_layout))
        buttons_layout.add_widget(cancel_button)

        self.sync_list_layout.add_widget(content_textinput)
        self.sync_list_layout.add_widget(buttons_layout)

        self.switch_to(self.sync_list_layout, '')

    def switch_to(self, widget, _):
        self.visible_layout.clear_widgets()
        self.visible_layout.add_widget(widget)

    def remove_childrens(self, widget, _):
        widget.clear_widgets()

    def get_textinput_content(self, textinput_widget):
        textinput_widget.select_all()
        return textinput_widget.selection_text

    def save_sync_list_content(self, textinput_widget, _):
        content = self.get_textinput_content(textinput_widget)
        sync_list_path = self.get_sync_list_fullpath()
        with open(sync_list_path, 'w') as sync_file:
            sync_file.write(content)

        self.switch_to(self.major_layout, '')

    def get_sync_list_fullpath(self):
        return os.sep.join([self.user_data_dir, 'settings', 'sync_list.txt'])

    def get_sync_list_content(self):
        sync_list_path = self.get_sync_list_fullpath()
        if os.path.exists(sync_list_path):
            with open(sync_list_path, 'r') as sync_list_file:
                return sync_list_file.read()
        else:
            os.makedirs(sync_list_path.rsplit(os.sep, 1)[0])
            open(sync_list_path, 'w').close()
            return ''

    def on_stop(self):
        for thread in self.threads:
            thread.kill()
        print("fffffffffffffffffffffff")
        return True

if __name__ == '__main__':
    app = TestApp()
    app.run()
