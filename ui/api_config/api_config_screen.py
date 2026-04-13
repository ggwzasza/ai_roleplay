from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle

from ui.common import StyledButton, show_confirm_popup

Builder.load_string('''
<APIConfigScreen>:
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
            title: 'API配置'

        ScrollView:
            GridLayout:
                id: api_list_container
                cols: 1
                spacing: dp(8)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)

        StyledButton:
            text: '+ 添加API配置'
            font_size: sp(16)
            size_hint_y: None
            height: dp(52)
            on_release: root.add_api_config()
''')


class APIConfigItem(BoxLayout):
    def __init__(self, api_data, on_edit=None, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.api_data = api_data
        self._on_edit = on_edit
        self._on_delete = on_delete
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(72)
        self.padding = dp(12), dp(8)
        self.spacing = dp(10)

        app = App.get_running_app()
        colors = app.theme_manager.get_colors() if hasattr(app, 'theme_manager') else {}

        with self.canvas.before:
            Color(rgba=app.theme_manager.hex_to_rgba(colors.get('card_bg', '#FFFFFF')) if colors else (1, 1, 1, 1))
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._update_rect, size=self._update_rect)

        info = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=dp(2))

        name_lbl = Label(
            text=api_data.get('name', '未命名API'),
            font_size=sp(14),
            bold=True,
            halign='left',
            valign='middle',
            color=app.theme_manager.hex_to_rgba(colors.get('text', '#212121')) if colors else (0, 0, 0, 1),
            size_hint_y=0.5
        )
        name_lbl.bind(size=name_lbl.setter('text_size'))

        url_lbl = Label(
            text=api_data.get('url', '')[:40],
            font_size=sp(11),
            halign='left',
            valign='middle',
            color=app.theme_manager.hex_to_rgba(colors.get('text_secondary', '#757575')) if colors else (0.5, 0.5, 0.5, 1),
            size_hint_y=0.5
        )
        url_lbl.bind(size=url_lbl.setter('text_size'))

        info.add_widget(name_lbl)
        info.add_widget(url_lbl)

        btn_layout = BoxLayout(size_hint_x=0.4, spacing=dp(4))

        edit_btn = Button(
            text='编辑',
            font_size=sp(12),
            background_color=(0, 0, 0, 0),
            color=app.theme_manager.hex_to_rgba(colors.get('primary', '#6C63FF')) if colors else (0.42, 0.39, 1, 1)
        )
        edit_btn.bind(on_release=lambda x: self._on_edit(self.api_data) if self._on_edit else None)

        delete_btn = Button(
            text='删除',
            font_size=sp(12),
            background_color=(0, 0, 0, 0),
            color=app.theme_manager.hex_to_rgba(colors.get('danger', '#F44336')) if colors else (0.96, 0.26, 0.21, 1)
        )
        delete_btn.bind(on_release=lambda x: self._confirm_delete())

        btn_layout.add_widget(edit_btn)
        btn_layout.add_widget(delete_btn)

        self.add_widget(info)
        self.add_widget(btn_layout)

    def _update_rect(self, instance, value):
        self._bg_rect.pos = instance.pos
        self._bg_rect.size = instance.size

    def _confirm_delete(self):
        show_confirm_popup(
            '删除API配置',
            f'确定要删除「{self.api_data.get("name", "未命名")}」吗？',
            lambda: self._do_delete()
        )

    def _do_delete(self):
        app = App.get_running_app()
        app.data_manager.delete_api(self.api_data['id'])
        if self._on_delete:
            self._on_delete(self.api_data)


class APIEditPopup(Popup):
    def __init__(self, api_data=None, on_save=None, **kwargs):
        self._api_data = api_data or {}
        self._on_save = on_save
        super().__init__(**kwargs)
        self.title = '编辑API' if api_data else '添加API'
        self.size_hint = (0.9, 0.8)
        self._build_content()

    def _build_content(self):
        app = App.get_running_app()

        layout = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(10))

        self._fields = {}
        field_defs = [
            ('name', 'API名称', False),
            ('api_key', 'API Key（密钥）', False),
            ('url', 'API地址（如 https://api.deepseek.com）', False),
            ('model', '模型名称（如 deepseek-chat / deepseek-reasoner）', False),
            ('temperature', '温度（0.0-2.0，默认0.8）', False),
            ('max_tokens', '最大输出长度（默认2048）', False),
            ('system_prompt', '提示词（用于设定AI行为和角色约束）', True),
            ('prefix_prompt', '前置提示词（权重高于普通提示词，用于强制约束）', True),
        ]

        for key, label, is_multiline in field_defs:
            lbl = Label(
                text=label,
                font_size=sp(12),
                halign='left',
                size_hint_y=None,
                height=dp(20),
                color=app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary']) if hasattr(app, 'theme_manager') else (0.5, 0.5, 0.5, 1)
            )
            lbl.bind(size=lbl.setter('text_size'))
            layout.add_widget(lbl)

            inp = TextInput(
                text=self._api_data.get(key, ''),
                font_size=sp(14),
                size_hint_y=None,
                height=dp(80) if is_multiline else dp(44),
                multiline=is_multiline,
                hint_text=label
            )
            layout.add_widget(inp)
            self._fields[key] = inp

        save_btn = StyledButton(text='保存', font_size=sp(16), size_hint_y=None, height=dp(52))
        save_btn.bind(on_release=lambda x: self._save())
        layout.add_widget(save_btn)

        self.content = layout

    def _save(self):
        data = {}
        for key, inp in self._fields.items():
            data[key] = inp.text.strip()

        if not data.get('name'):
            return
        if not data.get('url'):
            return

        try:
            data['temperature'] = float(data.get('temperature') or '0.8')
        except ValueError:
            data['temperature'] = 0.8

        try:
            data['max_tokens'] = int(data.get('max_tokens') or '2048')
        except ValueError:
            data['max_tokens'] = 2048

        if self._api_data.get('id'):
            data['id'] = self._api_data['id']

        app = App.get_running_app()
        app.data_manager.save_api(data)

        app.api_client.clear_client_cache(data.get('id'))

        if self._on_save:
            self._on_save(data)
        self.dismiss()


class APIConfigScreen(Screen):
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

    def add_api_config(self):
        popup = APIEditPopup(on_save=lambda d: self._refresh_list())
        popup.open()

    def _edit_api(self, api_data):
        app = App.get_running_app()
        full_data = app.data_manager.get_api(api_data['id'])
        popup = APIEditPopup(api_data=full_data, on_save=lambda d: self._refresh_list())
        popup.open()

    def _refresh_list(self):
        app = App.get_running_app()
        container = self.ids.get('api_list_container')
        if not container:
            return

        container.clear_widgets()
        apis = app.data_manager.get_api_list()

        if not apis:
            empty_label = Label(
                text='暂无API配置\n点击下方按钮添加',
                font_size=sp(14),
                color=app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary']),
                size_hint_y=None,
                height=dp(200)
            )
            container.add_widget(empty_label)
            return

        for api in apis:
            item = APIConfigItem(
                api_data=api,
                on_edit=self._edit_api,
                on_delete=lambda d: self._refresh_list()
            )
            container.add_widget(item)
