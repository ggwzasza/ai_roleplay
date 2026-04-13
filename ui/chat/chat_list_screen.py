from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.app import App

from ui.common import CardItem, show_confirm_popup

Builder.load_string('''
<ChatListScreen>:
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
            title: '对话'

        BoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: dp(12), dp(4)
            spacing: dp(8)

            canvas.before:
                Color:
                    rgba: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['bg'])
                Rectangle:
                    pos: self.pos
                    size: self.size

            Button:
                text: '历史对话'
                font_size: sp(14)
                size_hint_x: 0.5
                background_color: (0, 0, 0, 0)
                color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])
                bold: True
                on_release: root.show_history()

            Button:
                text: '+ 新建对话'
                font_size: sp(14)
                size_hint_x: 0.5
                background_color: (0, 0, 0, 0)
                color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['accent'])
                bold: True
                on_release: root.new_chat()

        ScrollView:
            id: chat_scroll
            GridLayout:
                id: chat_list_container
                cols: 1
                spacing: dp(6)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(8)
''')


class ChatItem(ButtonBehavior, CardItem):
    def __init__(self, chat_data, on_click=None, on_edit=None, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.chat_data = chat_data
        self._on_click = on_click
        self._on_edit = on_edit
        self._on_delete = on_delete

        app = App.get_running_app()
        colors = app.theme_manager.get_colors() if hasattr(app, 'theme_manager') else {}

        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.65, spacing=dp(2))

        name_label = Label(
            text=chat_data.get('name', '未命名对话'),
            font_size=sp(15),
            bold=True,
            halign='left',
            valign='middle',
            color=app.theme_manager.hex_to_rgba(colors.get('text', '#212121')) if colors else (0, 0, 0, 1),
            size_hint_y=0.5
        )
        name_label.bind(size=name_label.setter('text_size'))

        date_label = Label(
            text=chat_data.get('updated_at', '')[:16] if chat_data.get('updated_at') else '',
            font_size=sp(11),
            halign='left',
            valign='middle',
            color=app.theme_manager.hex_to_rgba(colors.get('text_secondary', '#757575')) if colors else (0.5, 0.5, 0.5, 1),
            size_hint_y=0.5
        )
        date_label.bind(size=date_label.setter('text_size'))

        info_layout.add_widget(name_label)
        info_layout.add_widget(date_label)

        btn_layout = BoxLayout(size_hint_x=0.35, spacing=dp(4))

        edit_btn = Button(
            text='编辑',
            font_size=sp(12),
            background_color=(0, 0, 0, 0),
            color=app.theme_manager.hex_to_rgba(colors.get('primary', '#6C63FF')) if colors else (0.42, 0.39, 1, 1)
        )
        edit_btn.bind(on_release=lambda x: self._on_edit(self.chat_data) if self._on_edit else None)

        delete_btn = Button(
            text='删除',
            font_size=sp(12),
            background_color=(0, 0, 0, 0),
            color=app.theme_manager.hex_to_rgba(colors.get('danger', '#F44336')) if colors else (0.96, 0.26, 0.21, 1)
        )
        delete_btn.bind(on_release=lambda x: self._confirm_delete())

        btn_layout.add_widget(edit_btn)
        btn_layout.add_widget(delete_btn)

        self.add_widget(info_layout)
        self.add_widget(btn_layout)

    def on_release(self):
        if self._on_click:
            self._on_click(self.chat_data)

    def _confirm_delete(self):
        show_confirm_popup(
            '删除对话',
            f'确定要删除对话「{self.chat_data.get("name", "未命名")}」吗？',
            lambda: self._do_delete()
        )

    def _do_delete(self):
        app = App.get_running_app()
        app.data_manager.delete_chat(self.chat_data['id'])
        if self._on_delete:
            self._on_delete(self.chat_data)


class ChatListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._chat_data = []

    def load_data(self, **kwargs):
        self._refresh_list()

    def on_enter(self, *args):
        header = self.ids.get('header')
        if header:
            header.set_back_callback(lambda: self._go_back())
        self._refresh_list()

    def _go_back(self):
        App.get_running_app().sm.current = 'main'

    def show_history(self):
        self._refresh_list()

    def new_chat(self):
        app = App.get_running_app()
        app.switch_screen('chat_edit', is_new=True)

    def _refresh_list(self):
        app = App.get_running_app()
        container = self.ids.get('chat_list_container')
        if not container:
            return

        container.clear_widgets()
        chats = app.data_manager.get_chat_list()
        self._chat_data = chats

        if not chats:
            empty_label = Label(
                text='暂无对话记录\n点击「新建对话」开始',
                font_size=sp(14),
                color=app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary']),
                size_hint_y=None,
                height=dp(200)
            )
            container.add_widget(empty_label)
            return

        for chat in chats:
            item = ChatItem(
                chat_data=chat,
                on_click=self._open_chat,
                on_edit=self._edit_chat,
                on_delete=lambda d: self._refresh_list()
            )
            container.add_widget(item)

    def _open_chat(self, chat_data):
        app = App.get_running_app()
        app.switch_screen('chat', chat_id=chat_data['id'])

    def _edit_chat(self, chat_data):
        app = App.get_running_app()
        app.switch_screen('chat_edit', chat_id=chat_data['id'], is_new=False)
