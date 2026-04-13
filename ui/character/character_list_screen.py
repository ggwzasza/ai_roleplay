from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.app import App

from ui.common import CardItem, show_confirm_popup

Builder.load_string('''
<CharacterListScreen>:
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
            title: '角色库'

        BoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: dp(12), dp(4)
            spacing: dp(8)

            Button:
                text: '已有角色'
                font_size: sp(14)
                size_hint_x: 0.33
                background_color: (0, 0, 0, 0)
                color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])
                bold: True
                on_release: root.show_existing()

            Button:
                text: '+ 新建角色'
                font_size: sp(14)
                size_hint_x: 0.33
                background_color: (0, 0, 0, 0)
                color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['accent'])
                bold: True
                on_release: root.new_character()

            Button:
                text: '用户角色'
                font_size: sp(14)
                size_hint_x: 0.33
                background_color: (0, 0, 0, 0)
                color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                bold: True
                on_release: root.edit_user_character()

        ScrollView:
            id: char_scroll
            GridLayout:
                id: char_list_container
                cols: 1
                spacing: dp(6)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(8)
''')


class CharacterItem(CardItem):
    def __init__(self, char_data, on_click=None, on_edit=None, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.char_data = char_data
        self._on_click = on_click
        self._on_edit = on_edit
        self._on_delete = on_delete

        app = App.get_running_app()
        colors = app.theme_manager.get_colors() if hasattr(app, 'theme_manager') else {}

        avatar_path = app.data_manager.get_avatar_path(char_data['id'])
        if avatar_path:
            from kivy.uix.image import Image
            avatar = Image(
                source=avatar_path,
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                allow_stretch=True,
                keep_ratio=True
            )
            self.add_widget(avatar)
        else:
            placeholder = Label(
                text=char_data.get('name', '?')[0],
                font_size=sp(20),
                bold=True,
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                color=app.theme_manager.hex_to_rgba(colors.get('primary', '#6C63FF')) if colors else (0.42, 0.39, 1, 1)
            )
            self.add_widget(placeholder)

        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.55, spacing=dp(2))

        name_label = Label(
            text=char_data.get('name', '未命名角色'),
            font_size=sp(15),
            bold=True,
            halign='left',
            valign='middle',
            color=app.theme_manager.hex_to_rgba(colors.get('text', '#212121')) if colors else (0, 0, 0, 1),
            size_hint_y=0.5
        )
        name_label.bind(size=name_label.setter('text_size'))

        race_label = Label(
            text=char_data.get('race', ''),
            font_size=sp(11),
            halign='left',
            valign='middle',
            color=app.theme_manager.hex_to_rgba(colors.get('text_secondary', '#757575')) if colors else (0.5, 0.5, 0.5, 1),
            size_hint_y=0.5
        )
        race_label.bind(size=race_label.setter('text_size'))

        info_layout.add_widget(name_label)
        info_layout.add_widget(race_label)

        btn_layout = BoxLayout(size_hint_x=0.3, spacing=dp(4))

        edit_btn = Button(
            text='编辑',
            font_size=sp(12),
            background_color=(0, 0, 0, 0),
            color=app.theme_manager.hex_to_rgba(colors.get('primary', '#6C63FF')) if colors else (0.42, 0.39, 1, 1)
        )
        edit_btn.bind(on_release=lambda x: self._on_edit(self.char_data) if self._on_edit else None)

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

    def _confirm_delete(self):
        show_confirm_popup(
            '删除角色',
            f'确定要删除角色「{self.char_data.get("name", "未命名")}」吗？',
            lambda: self._do_delete()
        )

    def _do_delete(self):
        app = App.get_running_app()
        app.data_manager.delete_character(self.char_data['id'])
        if self._on_delete:
            self._on_delete(self.char_data)


class CharacterListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_data(self, **kwargs):
        self._refresh_list()

    def on_enter(self, *args):
        header = self.ids.get('header')
        if header:
            header.set_back_callback(lambda: self._go_back())
        self._refresh_list()

    def _go_back(self):
        App.get_running_app().sm.current = 'main'

    def show_existing(self):
        self._refresh_list()

    def new_character(self):
        app = App.get_running_app()
        app.switch_screen('character_edit', is_new=True)

    def edit_user_character(self):
        app = App.get_running_app()
        app.switch_screen('user_character')

    def _refresh_list(self):
        app = App.get_running_app()
        container = self.ids.get('char_list_container')
        if not container:
            return

        container.clear_widgets()
        characters = app.data_manager.get_character_list()

        if not characters:
            empty_label = Label(
                text='暂无角色\n点击「新建角色」创建',
                font_size=sp(14),
                color=app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary']),
                size_hint_y=None,
                height=dp(200)
            )
            container.add_widget(empty_label)
            return

        for char in characters:
            item = CharacterItem(
                char_data=char,
                on_edit=self._edit_character,
                on_delete=lambda d: self._refresh_list()
            )
            container.add_widget(item)

    def _edit_character(self, char_data):
        app = App.get_running_app()
        app.switch_screen('character_edit', character_id=char_data['id'], is_new=False)
