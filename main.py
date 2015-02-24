import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
__version__ = '1.0'


class TestApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        sync_button = Button(text='SYNC PLAYLISTS LIST')
        edit_button = Button(text='EDIT SYNC LIST')
        url_input = TextInput()
        download_button = Button(text='DOWNLOAD PLAYLIST')

        layout.add_widget(sync_button)
        layout.add_widget(edit_button)
        layout.add_widget(url_input)
        layout.add_widget(download_button)

        return layout


if __name__ == '__main__':
    TestApp().run()
