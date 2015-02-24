__version__ = '1.0'
import sys

from kivy.app import App
from kivy.lang import Builder

kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'SYNC PLAYLISTS LIST'
        on_press: sys.exit()
        size_hint_y: None
        height: '55dp'
    Button:
        text: 'EDIT SYNC LIST'
        on_press: sys.exit()
        size_hint_y: None
        height: '55dp'
    TextInput:
        height: '55dp'
    Button:
        text: 'DOWNLOAD PLAYLIST'
        on_press: sys.exit()
        size_hint_y: None
        height: '55dp'
'''


class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    TestApp().run()
