import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

from ui.common import HeaderBar, StyledButton

Builder.load_string('''
<CharacterEditScreen>:
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
            title: '角色编辑'

        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(8)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)

                Label:
                    text: '头像'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                Button:
                    id: avatar_btn
                    text: '选择头像图片'
                    font_size: sp(13)
                    size_hint_y: None
                    height: dp(40)
                    background_color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['divider'])
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                    on_release: root.pick_avatar()

                Label:
                    text: '角色名字'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_name
                    hint_text: '输入角色名字'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(44)
                    multiline: False

                Label:
                    text: '年龄'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_age
                    hint_text: '输入年龄'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(44)
                    multiline: False

                Label:
                    text: '种族'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_race
                    hint_text: '输入种族'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(44)
                    multiline: False

                Label:
                    text: '身材'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_body
                    hint_text: '描述身材特征'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(44)
                    multiline: False

                Label:
                    text: '经历'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_experience
                    hint_text: '描述角色经历'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(80)
                    multiline: True

                Label:
                    text: '性格'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_personality
                    hint_text: '描述角色性格'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(80)
                    multiline: True

                Label:
                    text: '言谈风格'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_speech_style
                    hint_text: '描述角色说话风格'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(80)
                    multiline: True

                Label:
                    text: '癖好'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: char_habits
                    hint_text: '描述角色癖好'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(80)
                    multiline: True

                Label:
                    text: '绑定API'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(20)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                Spinner:
                    id: api_spinner
                    text: '选择API'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(44)

                StyledButton:
                    text: '保存角色'
                    font_size: sp(16)
                    size_hint_y: None
                    height: dp(52)
                    on_release: root.save_character()
''')


class CharacterEditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._character_id = None
        self._is_new = True
        self._avatar_source = None
        self._api_list = []

    def load_data(self, **kwargs):
        self._is_new = kwargs.get('is_new', True)
        self._character_id = kwargs.get('character_id', None)
        self._avatar_source = None

        self._load_api_spinner()

        if not self._is_new and self._character_id:
            app = App.get_running_app()
            char = app.data_manager.get_character(self._character_id)
            if char:
                self.ids.char_name.text = char.get('name', '')
                self.ids.char_age.text = char.get('age', '')
                self.ids.char_race.text = char.get('race', '')
                self.ids.char_body.text = char.get('body', '')
                self.ids.char_experience.text = char.get('experience', '')
                self.ids.char_personality.text = char.get('personality', '')
                self.ids.char_speech_style.text = char.get('speech_style', '')
                self.ids.char_habits.text = char.get('habits', '')

                api_id = char.get('api_id', '')
                for i, api in enumerate(self._api_list):
                    if api['id'] == api_id:
                        self.ids.api_spinner.text = api['name']
                        break

                avatar_path = app.data_manager.get_avatar_path(self._character_id)
                if avatar_path:
                    self.ids.avatar_btn.text = '已设置头像（点击更换）'
        else:
            self.ids.char_name.text = ''
            self.ids.char_age.text = ''
            self.ids.char_race.text = ''
            self.ids.char_body.text = ''
            self.ids.char_experience.text = ''
            self.ids.char_personality.text = ''
            self.ids.char_speech_style.text = ''
            self.ids.char_habits.text = ''
            self.ids.api_spinner.text = '选择API'

    def on_enter(self, *args):
        header = self.ids.get('header')
        if header:
            header.set_back_callback(lambda: self._go_back())

    def _go_back(self):
        App.get_running_app().sm.current = 'character_list'

    def _load_api_spinner(self):
        app = App.get_running_app()
        apis = app.data_manager.get_api_list()
        self._api_list = apis
        spinner = self.ids.get('api_spinner')
        if spinner:
            spinner.values = ['选择API'] + [api['name'] for api in apis]

    def pick_avatar(self):
        try:
            from plyer import filechooser
            filechooser.open_file(
                filters=['*.png', '*.jpg', '*.jpeg', '*.webp'],
                on_selection=self._on_avatar_selected
            )
        except ImportError:
            self.ids.avatar_btn.text = '（需要安装plyer）'

    def _on_avatar_selected(self, selection):
        if selection:
            self._avatar_source = selection[0]
            self.ids.avatar_btn.text = f'已选择: {os.path.basename(selection[0])}'

    def save_character(self):
        app = App.get_running_app()

        name = self.ids.char_name.text.strip()
        if not name:
            return

        selected_api_id = ''
        spinner_text = self.ids.api_spinner.text
        for api in self._api_list:
            if api['name'] == spinner_text:
                selected_api_id = api['id']
                break

        character_data = {
            'name': name,
            'age': self.ids.char_age.text.strip(),
            'race': self.ids.char_race.text.strip(),
            'body': self.ids.char_body.text.strip(),
            'experience': self.ids.char_experience.text.strip(),
            'personality': self.ids.char_personality.text.strip(),
            'speech_style': self.ids.char_speech_style.text.strip(),
            'habits': self.ids.char_habits.text.strip(),
            'api_id': selected_api_id,
        }

        if not self._is_new and self._character_id:
            character_data['id'] = self._character_id

        char_id = app.data_manager.save_character(character_data)

        if self._avatar_source:
            app.data_manager.save_avatar(char_id, self._avatar_source)
            saved_char = app.data_manager.get_character(char_id)
            if saved_char:
                saved_char['avatar'] = app.data_manager.get_avatar_path(char_id)
                app.data_manager.save_character(saved_char)

        self._go_back()
