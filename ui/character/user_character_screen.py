from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App

from ui.common import HeaderBar, StyledButton

Builder.load_string('''
<UserCharacterScreen>:
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['bg'])
            Rectangle:
                pos: self.pos
                size: self.size

        HeaderBar:
            id: header
            title: '用户角色'

        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)

                Label:
                    text: '用户角色设定'
                    font_size: sp(16)
                    bold: True
                    size_hint_y: None
                    height: dp(30)
                    halign: 'left'
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                    text_size: self.size

                Label:
                    text: '在此输入你自己角色的详细信息，包括名字、年龄、性格等。这些信息将作为AI理解你角色的依据。'
                    font_size: sp(12)
                    size_hint_y: None
                    height: dp(50)
                    halign: 'left'
                    valign: 'top'
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                Label:
                    text: '角色提示词'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: user_prompt
                    hint_text: '输入你的角色设定... 例如：我叫小明，18岁，性格开朗...'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(200)
                    multiline: True

                StyledButton:
                    text: '保存'
                    font_size: sp(16)
                    size_hint_y: None
                    height: dp(52)
                    on_release: root.save_user_character()
''')


class UserCharacterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_data(self, **kwargs):
        self._load_data()

    def on_enter(self, *args):
        header = self.ids.get('header')
        if header:
            header.set_back_callback(lambda: self._go_back())
        self._load_data()

    def _go_back(self):
        App.get_running_app().sm.current = 'character_list'

    def _load_data(self):
        app = App.get_running_app()
        user_char = app.data_manager.user_character
        prompt_input = self.ids.get('user_prompt')
        if prompt_input and user_char:
            prompt_input.text = user_char.get('prompt', '')

    def save_user_character(self):
        app = App.get_running_app()
        prompt = self.ids.user_prompt.text.strip()
        app.data_manager.save_user_character({'prompt': prompt})
        self._go_back()
