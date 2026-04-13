import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.app import App

from ui.common import HeaderBar, StyledButton

Builder.load_string('''
<ChatEditScreen>:
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
            title: '对话设置'

        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)

                Label:
                    text: '对话名称'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(24)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: chat_name
                    hint_text: '输入对话名称'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(44)
                    multiline: False

                Label:
                    text: '参与角色（可多选）'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(24)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                GridLayout:
                    id: character_select
                    cols: 2
                    spacing: dp(6)
                    size_hint_y: None
                    height: self.minimum_height

                Label:
                    text: '宏观提示词（世界背景等）'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(24)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: macro_prompt
                    hint_text: '描述世界背景、整体设定...'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(100)
                    multiline: True

                Label:
                    text: '记忆设定（参考上下文消息数量）'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(24)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: memory_count
                    hint_text: '20'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(44)
                    multiline: False
                    input_filter: 'int'

                Label:
                    text: '前置提示词（高权重）'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(24)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                TextInput:
                    id: prefix_prompt
                    hint_text: '优先级高于普通提示词的内容...'
                    font_size: sp(14)
                    size_hint_y: None
                    height: dp(80)
                    multiline: True

                Label:
                    text: '聊天背景图'
                    font_size: sp(13)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(24)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size

                Button:
                    id: bg_upload_btn
                    text: '选择背景图片'
                    font_size: sp(13)
                    size_hint_y: None
                    height: dp(40)
                    background_color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['divider'])
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                    on_release: root.pick_background()

                StyledButton:
                    text: '保存'
                    font_size: sp(16)
                    size_hint_y: None
                    height: dp(52)
                    on_release: root.save_chat()
''')


class CharacterToggle(Button):
    def __init__(self, char_data, selected=False, **kwargs):
        super().__init__(**kwargs)
        self.char_data = char_data
        self.selected = selected
        self.font_size = sp(12)
        self.size_hint_y = None
        self.height = dp(36)
        self.background_color = (0, 0, 0, 0)
        self._update_style()

    def on_release(self):
        self.selected = not self.selected
        self._update_style()

    def _update_style(self):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            colors = app.theme_manager.get_colors()
            if self.selected:
                self.background_color = app.theme_manager.hex_to_rgba(colors['primary'])
                self.color = (1, 1, 1, 1)
            else:
                self.background_color = app.theme_manager.hex_to_rgba(colors['divider'])
                self.color = app.theme_manager.hex_to_rgba(colors['text'])
        self.text = self.char_data.get('name', '未知')


class ChatEditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._chat_id = None
        self._is_new = True
        self._selected_characters = []
        self._bg_source = None

    def load_data(self, **kwargs):
        self._is_new = kwargs.get('is_new', True)
        self._chat_id = kwargs.get('chat_id', None)
        self._bg_source = None
        self._load_characters()

        if not self._is_new and self._chat_id:
            app = App.get_running_app()
            chat = app.data_manager.get_chat(self._chat_id)
            if chat:
                self.ids.chat_name.text = chat.get('name', '')
                self.ids.macro_prompt.text = chat.get('macro_prompt', '')
                self.ids.memory_count.text = str(chat.get('memory_count', 20))
                self.ids.prefix_prompt.text = chat.get('prefix_prompt', '')
                self._selected_characters = chat.get('character_ids', [])
                self._update_character_selection()
        else:
            self.ids.chat_name.text = ''
            self.ids.macro_prompt.text = ''
            self.ids.memory_count.text = '20'
            self.ids.prefix_prompt.text = ''
            self._selected_characters = []

    def on_enter(self, *args):
        header = self.ids.get('header')
        if header:
            header.set_back_callback(lambda: self._go_back())

    def _go_back(self):
        App.get_running_app().sm.current = 'chat_list'

    def _load_characters(self):
        app = App.get_running_app()
        container = self.ids.get('character_select')
        if not container:
            return
        container.clear_widgets()

        characters = app.data_manager.get_character_list()
        for char in characters:
            toggle = CharacterToggle(char, selected=char['id'] in self._selected_characters)
            container.add_widget(toggle)

        if not characters:
            lbl = Label(
                text='暂无角色，请先在角色库中创建',
                font_size=sp(12),
                size_hint_y=None,
                height=dp(36)
            )
            container.add_widget(lbl)

    def _update_character_selection(self):
        container = self.ids.get('character_select')
        if not container:
            return
        for child in container.children:
            if isinstance(child, CharacterToggle):
                child.selected = child.char_data['id'] in self._selected_characters
                child._update_style()

    def pick_background(self):
        from kivy.core.window import Window
        try:
            from plyer import filechooser
            filechooser.open_file(
                filters=['*.png', '*.jpg', '*.jpeg', '*.webp'],
                on_selection=self._on_bg_selected
            )
        except ImportError:
            self.ids.bg_upload_btn.text = '（需要安装plyer）'

    def _on_bg_selected(self, selection):
        if selection:
            self._bg_source = selection[0]
            self.ids.bg_upload_btn.text = f'已选择: {os.path.basename(selection[0])}'

    def save_chat(self):
        app = App.get_running_app()

        name = self.ids.chat_name.text.strip()
        if not name:
            name = '未命名对话'

        try:
            memory_count = int(self.ids.memory_count.text) if self.ids.memory_count.text else 20
        except ValueError:
            memory_count = 20

        container = self.ids.get('character_select')
        selected_ids = []
        if container:
            for child in container.children:
                if isinstance(child, CharacterToggle) and child.selected:
                    selected_ids.append(child.char_data['id'])

        chat_data = {
            'name': name,
            'character_ids': selected_ids,
            'macro_prompt': self.ids.macro_prompt.text,
            'memory_count': memory_count,
            'prefix_prompt': self.ids.prefix_prompt.text,
        }

        if not self._is_new and self._chat_id:
            chat_data['id'] = self._chat_id
            existing = app.data_manager.get_chat(self._chat_id)
            if existing:
                chat_data['messages'] = existing.get('messages', [])
                chat_data['created_at'] = existing.get('created_at', '')

        chat_id = app.data_manager.save_chat(chat_data)

        if self._bg_source:
            app.data_manager.save_chat_background(chat_id, self._bg_source)

        self._go_back()
