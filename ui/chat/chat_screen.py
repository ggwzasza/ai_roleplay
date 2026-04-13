import copy
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp, sp
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty

from ui.common import HeaderBar

Builder.load_string('''
<ChatScreen>:
    BoxLayout:
        orientation: 'vertical'

        FloatLayout:
            id: bg_container

            Image:
                id: bg_image
                source: ''
                allow_stretch: True
                keep_ratio: False
                opacity: 0.3
                size_hint: 1, 1
                pos: 0, 0

            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                pos: 0, 0

                HeaderBar:
                    id: header

                BoxLayout:
                    id: chat_area
                    orientation: 'vertical'

                    ScrollView:
                        id: msg_scroll
                        do_scroll_x: False

                        GridLayout:
                            id: msg_container
                            cols: 1
                            spacing: dp(6)
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(8)

                    BoxLayout:
                        size_hint_y: None
                        height: dp(56)
                        padding: dp(6), dp(4)
                        spacing: dp(6)

                        canvas.before:
                            Color:
                                rgba: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['card_bg'])
                            Rectangle:
                                pos: self.pos
                                size: self.size

                        TextInput:
                            id: msg_input
                            hint_text: '输入消息...'
                            font_size: sp(15)
                            multiline: False
                            size_hint_x: 0.7
                            on_text_validate: root.send_message()

                        Button:
                            text: '发送'
                            font_size: sp(15)
                            size_hint_x: 0.2
                            background_color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])
                            color: (1, 1, 1, 1)
                            on_release: root.send_message()

                        Button:
                            id: settings_btn
                            text: '⚙'
                            font_size: sp(20)
                            size_hint_x: None
                            width: dp(48)
                            background_color: (0, 0, 0, 0)
                            color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                            on_release: root.toggle_settings()

<ChatSettingsPopup>:
    size_hint: (0.85, 0.5)
    auto_dismiss: True
    title: '聊天设置'

    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)

        Label:
            text: f'字体大小: {root.font_size}px'
            font_size: sp(13)
            size_hint_y: None
            height: dp(24)
            halign: 'left'

        Slider:
            id: font_slider
            min: 10
            max: 24
            value: root.font_size
            step: 1
            size_hint_y: None
            height: dp(44)
            on_value: root.font_size = int(self.value)

        Label:
            text: '流式传输自动下滑'
            font_size: sp(13)
            size_hint_y: None
            height: dp(24)
            halign: 'left'

        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(8)

            ToggleButton:
                id: auto_scroll_yes
                text: '是'
                group: 'auto_scroll'
                font_size: sp(14)
                state: 'down' if root.auto_scroll else 'normal'
                on_press: root.auto_scroll = True

            ToggleButton:
                id: auto_scroll_no
                text: '否'
                group: 'auto_scroll'
                font_size: sp(14)
                state: 'normal' if root.auto_scroll else 'down'
                on_press: root.auto_scroll = False

        Button:
            text: '关闭'
            font_size: sp(15)
            size_hint_y: None
            height: dp(48)
            on_release: root.dismiss()
''')


class MessageBubble(BoxLayout):
    def __init__(self, text, is_user=False, character_name='', character_id=None,
                 font_size=14, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        colors = app.theme_manager.get_colors() if hasattr(app, 'theme_manager') else {}

        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = dp(4), dp(2)

        bubble_color = colors.get('bubble_user', '#DCF8C6') if is_user else colors.get('bubble_ai', '#FFFFFF')
        text_color = colors.get('text', '#212121')

        name_label = None
        if not is_user and character_name:
            name_label = Label(
                text=character_name,
                font_size=sp(12),
                bold=True,
                halign='left',
                size_hint_y=None,
                height=dp(20),
                color=app.theme_manager.hex_to_rgba(colors.get('primary', '#6C63FF')) if colors else (0.42, 0.39, 1, 1)
            )
            name_label.bind(size=name_label.setter('text_size'))

        avatar_path = ''
        if not is_user and character_id:
            avatar_path = app.data_manager.get_avatar_path(character_id)

        content_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            spacing=dp(6)
        )

        if not is_user and avatar_path:
            try:
                avatar = Image(
                    source=avatar_path,
                    size_hint=(None, None),
                    size=(dp(36), dp(36)),
                    allow_stretch=True,
                    keep_ratio=True
                )
                content_row.add_widget(avatar)
            except Exception:
                pass

        bubble = BoxLayout(
            orientation='vertical',
            size_hint_x=0.8,
            size_hint_y=None,
            padding=[dp(10), dp(6)]
        )

        with bubble.canvas.before:
            Color(rgba=app.theme_manager.hex_to_rgba(bubble_color) if colors else (0.86, 0.97, 0.9, 1))
            bubble._bg_rect = RoundedRectangle(
                pos=bubble.pos,
                size=bubble.size,
                radius=[dp(12), dp(12), dp(4), dp(12)] if not is_user else [dp(12), dp(12), dp(12), dp(4)]
            )

        def update_rect(instance, value):
            bubble._bg_rect.pos = bubble.pos
            bubble._bg_rect.size = bubble.size

        bubble.bind(pos=update_rect, size=update_rect)

        self.msg_label = Label(
            text=text,
            font_size=sp(font_size),
            halign='left',
            valign='top',
            color=app.theme_manager.hex_to_rgba(text_color) if colors else (0, 0, 0, 1),
            size_hint_y=None,
        )
        self.msg_label.bind(
            width=lambda *x: self.msg_label.setter('text_size')(self.msg_label, (self.msg_label.width, None)),
            texture_size=lambda *x: setattr(self.msg_label, 'height', self.msg_label.texture_size[1])
        )
        self.msg_label.bind(size=lambda *x: setattr(bubble, 'height', self.msg_label.height + dp(16)))

        bubble.add_widget(self.msg_label)

        if is_user:
            spacer = BoxLayout(size_hint_x=0.2)
            content_row.add_widget(spacer)
            content_row.add_widget(bubble)
        else:
            content_row.add_widget(bubble)
            spacer = BoxLayout(size_hint_x=0.2)
            content_row.add_widget(spacer)

        if name_label:
            self.add_widget(name_label)
        self.add_widget(content_row)

        self.bind(minimum_height=self.setter('height'))


from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton


class ChatSettingsPopup(Popup):
    font_size = NumericProperty(14)
    auto_scroll = BooleanProperty(True)

    def __init__(self, initial_font_size=14, initial_auto_scroll=True, **kwargs):
        self.font_size = initial_font_size
        self.auto_scroll = initial_auto_scroll
        super().__init__(**kwargs)


class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._chat_id = None
        self._chat_data = None
        self._current_character_id = None
        self._font_size = 14
        self._auto_scroll = True
        self._streaming = False
        self._current_bubble = None

    def load_data(self, **kwargs):
        self._chat_id = kwargs.get('chat_id')
        if self._chat_id:
            self._load_chat()

    def on_enter(self, *args):
        if self._chat_id:
            self._reload_chat_data()
        header = self.ids.get('header')
        if header and self._chat_data:
            header.title = self._chat_data.get('name', '对话')
            header.set_back_callback(lambda: self._go_back())

    def _go_back(self):
        App.get_running_app().sm.current = 'chat_list'

    def _reload_chat_data(self):
        app = App.get_running_app()
        self._chat_data = app.data_manager.get_chat(self._chat_id)
        self._font_size = app.data_manager.get_setting('font_size', 14)
        self._auto_scroll = app.data_manager.get_setting('auto_scroll', True)
        self._load_background()

    def _load_chat(self):
        self._reload_chat_data()
        if not self._chat_data:
            return

        container = self.ids.get('msg_container')
        if container:
            container.clear_widgets()
            app = App.get_running_app()
            for msg in self._chat_data.get('messages', []):
                is_user = msg['role'] == 'user'
                char_name = ''
                char_id = msg.get('character_id')
                if not is_user and char_id:
                    char = app.data_manager.get_character(char_id)
                    if char:
                        char_name = char.get('name', '')
                bubble = MessageBubble(
                    text=msg['content'],
                    is_user=is_user,
                    character_name=char_name,
                    character_id=char_id,
                    font_size=self._font_size
                )
                container.add_widget(bubble)

            Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)

    def _load_background(self):
        bg_image = self.ids.get('bg_image')
        if bg_image and self._chat_id:
            app = App.get_running_app()
            bg_path = app.data_manager.get_chat_bg_path(self._chat_id)
            bg_image.source = bg_path
            bg_image.opacity = 0.3 if bg_path else 0

    def _scroll_to_bottom(self):
        scroll = self.ids.get('msg_scroll')
        if scroll:
            scroll.scroll_y = 0

    def send_message(self):
        if self._streaming:
            return

        input_field = self.ids.get('msg_input')
        if not input_field or not input_field.text.strip():
            return

        user_text = input_field.text.strip()
        input_field.text = ''

        self._reload_chat_data()

        app = App.get_running_app()
        app.data_manager.add_message_to_chat(self._chat_id, 'user', user_text)

        container = self.ids.get('msg_container')
        if container:
            bubble = MessageBubble(
                text=user_text,
                is_user=True,
                font_size=self._font_size
            )
            container.add_widget(bubble)

        character_ids = list(self._chat_data.get('character_ids', []))
        if not character_ids:
            if container:
                hint = MessageBubble(
                    text='[提示] 请先在对话设置中添加参与角色',
                    is_user=False,
                    font_size=self._font_size
                )
                container.add_widget(hint)
            return

        self._pending_characters = character_ids
        self._character_outputs = []
        self._current_char_index = 0
        self._start_next_character_stream()

    def _start_next_character_stream(self):
        if self._current_char_index >= len(self._pending_characters):
            self._streaming = False
            self._pending_characters = []
            self._character_outputs = []
            return

        self._streaming = True
        char_id = self._pending_characters[self._current_char_index]
        self._current_character_id = char_id

        app = App.get_running_app()
        character = app.data_manager.get_character(char_id)

        other_outputs = list(self._character_outputs) if self._character_outputs else None

        result = app.api_client.send_message(
            self._chat_id,
            char_id,
            None,
            stream=True,
            other_character_outputs=other_outputs
        )

        container = self.ids.get('msg_container')

        if result is None:
            error_msg = '[未配置API或角色未绑定API]'
            app.data_manager.add_message_to_chat(
                self._chat_id, 'assistant', error_msg, char_id
            )
            if container:
                err_bubble = MessageBubble(
                    text=error_msg,
                    is_user=False,
                    character_name=character.get('name', '') if character else '',
                    character_id=char_id,
                    font_size=self._font_size
                )
                container.add_widget(err_bubble)
            self._current_char_index += 1
            Clock.schedule_once(lambda dt: self._start_next_character_stream(), 0.3)
            return

        char_name = character.get('name', '') if character else ''

        ai_bubble = MessageBubble(
            text='',
            is_user=False,
            character_name=char_name,
            character_id=char_id,
            font_size=self._font_size
        )
        if container:
            container.add_widget(ai_bubble)
        self._current_bubble = ai_bubble
        self._full_response = ''

        self._stream_gen = result
        Clock.schedule_interval(self._stream_tick, 0.05)

        try:
            chunk = next(result)
            self._full_response += chunk
            if ai_bubble.msg_label:
                ai_bubble.msg_label.text = self._full_response + '▌'
        except StopIteration:
            self._finish_current_character()

    def _stream_tick(self, dt):
        try:
            chunk = next(self._stream_gen)
            self._full_response += chunk
            if self._current_bubble and self._current_bubble.msg_label:
                self._current_bubble.msg_label.text = self._full_response + '▌'
            if self._auto_scroll:
                self._scroll_to_bottom()
        except StopIteration:
            self._finish_current_character()

    def _finish_current_character(self):
        try:
            Clock.unschedule(self._stream_tick)
        except Exception:
            pass

        if self._current_bubble and self._current_bubble.msg_label:
            self._current_bubble.msg_label.text = self._full_response

        app = App.get_running_app()
        app.data_manager.add_message_to_chat(
            self._chat_id, 'assistant', self._full_response, self._current_character_id
        )

        character = app.data_manager.get_character(self._current_character_id)
        char_name = character.get('name', '') if character else ''
        self._character_outputs.append((char_name, self._full_response))

        self._current_char_index += 1

        if self._auto_scroll:
            self._scroll_to_bottom()

        if self._current_char_index < len(self._pending_characters):
            Clock.schedule_once(lambda dt: self._start_next_character_stream(), 0.5)
        else:
            self._streaming = False
            self._pending_characters = []
            self._character_outputs = []

    def toggle_settings(self):
        popup = ChatSettingsPopup(
            initial_font_size=self._font_size,
            initial_auto_scroll=self._auto_scroll
        )
        popup.bind(on_dismiss=self._apply_settings)
        popup.open()

    def _apply_settings(self, instance):
        self._font_size = instance.font_size
        self._auto_scroll = instance.auto_scroll

        app = App.get_running_app()
        app.data_manager.save_settings({
            'font_size': self._font_size,
            'auto_scroll': self._auto_scroll
        })

        self._reload_chat_and_refresh()

    def _reload_chat_and_refresh(self):
        self._reload_chat_data()
        if not self._chat_data:
            return

        container = self.ids.get('msg_container')
        if not container:
            return

        container.clear_widgets()
        app = App.get_running_app()
        for msg in self._chat_data.get('messages', []):
            is_user = msg['role'] == 'user'
            char_name = ''
            char_id = msg.get('character_id')
            if not is_user and char_id:
                char = app.data_manager.get_character(char_id)
                if char:
                    char_name = char.get('name', '')
            bubble = MessageBubble(
                text=msg['content'],
                is_user=is_user,
                character_name=char_name,
                character_id=char_id,
                font_size=self._font_size
            )
            container.add_widget(bubble)

        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
