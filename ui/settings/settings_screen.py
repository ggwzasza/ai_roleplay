from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

from ui.common import HeaderBar

Builder.load_string('''
<SettingsScreen>:
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
            title: '设置'

        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)

                Label:
                    text: '外观'
                    font_size: sp(16)
                    bold: True
                    size_hint_y: None
                    height: dp(30)
                    halign: 'left'
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])
                    text_size: self.size

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(8)

                    Label:
                        text: '日间/夜间模式'
                        font_size: sp(14)
                        halign: 'left'
                        size_hint_x: 0.5
                        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                        text_size: self.size

                    ToggleButton:
                        id: theme_light
                        text: '日间'
                        group: 'theme'
                        font_size: sp(14)
                        size_hint_x: 0.25
                        on_press: root.set_theme('light')

                    ToggleButton:
                        id: theme_dark
                        text: '夜间'
                        group: 'theme'
                        font_size: sp(14)
                        size_hint_x: 0.25
                        on_press: root.set_theme('dark')

                Label:
                    text: '主题色'
                    font_size: sp(14)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(24)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                    text_size: self.size

                GridLayout:
                    id: color_scheme_grid
                    cols: 5
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(44)

                Label:
                    text: '聊天'
                    font_size: sp(16)
                    bold: True
                    size_hint_y: None
                    height: dp(30)
                    halign: 'left'
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])
                    text_size: self.size

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(8)

                    Label:
                        text: '默认字体大小'
                        font_size: sp(14)
                        halign: 'left'
                        size_hint_x: 0.5
                        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                        text_size: self.size

                    Label:
                        id: font_size_label
                        text: '14px'
                        font_size: sp(14)
                        halign: 'right'
                        size_hint_x: 0.2
                        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])

                    Button:
                        id: font_minus
                        text: '-'
                        font_size: sp(18)
                        size_hint_x: None
                        width: dp(44)
                        background_color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['divider'])
                        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                        on_release: root.change_font_size(-1)

                    Button:
                        id: font_plus
                        text: '+'
                        font_size: sp(18)
                        size_hint_x: None
                        width: dp(44)
                        background_color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['divider'])
                        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                        on_release: root.change_font_size(1)

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(8)

                    Label:
                        text: '流式自动下滑'
                        font_size: sp(14)
                        halign: 'left'
                        size_hint_x: 0.5
                        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])
                        text_size: self.size

                    ToggleButton:
                        id: scroll_yes
                        text: '是'
                        group: 'auto_scroll'
                        font_size: sp(14)
                        size_hint_x: 0.25
                        on_press: root.set_auto_scroll(True)

                    ToggleButton:
                        id: scroll_no
                        text: '否'
                        group: 'auto_scroll'
                        font_size: sp(14)
                        size_hint_x: 0.25
                        on_press: root.set_auto_scroll(False)

                Label:
                    text: '关于'
                    font_size: sp(16)
                    bold: True
                    size_hint_y: None
                    height: dp(30)
                    halign: 'left'
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])
                    text_size: self.size

                Label:
                    text: 'AI角色扮演 v1.0.0 - 跨平台AI角色扮演框架 - 基于Kivy开发'
                    font_size: sp(12)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(60)
                    color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
                    text_size: self.size
''')


class ColorSchemeButton(Button):
    def __init__(self, scheme_name, color_hex, on_select=None, **kwargs):
        super().__init__(**kwargs)
        self.scheme_name = scheme_name
        self._on_select = on_select
        self.size_hint_x = None
        self.width = dp(48)
        self.font_size = sp(11)

        from core.theme_manager import ThemeManager
        rgba = ThemeManager.hex_to_rgba(color_hex)
        self.background_color = rgba
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.text = scheme_name[:2]

    def on_release(self):
        if self._on_select:
            self._on_select(self.scheme_name)


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_data(self, **kwargs):
        pass

    def on_enter(self, *args):
        header = self.ids.get('header')
        if header:
            header.set_back_callback(lambda: self._go_back())
        self._load_settings()

    def _go_back(self):
        App.get_running_app().sm.current = 'main'

    def _load_settings(self):
        app = App.get_running_app()
        theme = app.data_manager.get_setting('theme', 'light')
        auto_scroll = app.data_manager.get_setting('auto_scroll', True)
        font_size = app.data_manager.get_setting('font_size', 14)
        color_scheme = app.data_manager.get_setting('color_scheme', 'default')

        if hasattr(self.ids, 'theme_light'):
            self.ids.theme_light.state = 'down' if theme == 'light' else 'normal'
        if hasattr(self.ids, 'theme_dark'):
            self.ids.theme_dark.state = 'down' if theme == 'dark' else 'normal'
        if hasattr(self.ids, 'scroll_yes'):
            self.ids.scroll_yes.state = 'down' if auto_scroll else 'normal'
        if hasattr(self.ids, 'scroll_no'):
            self.ids.scroll_no.state = 'normal' if auto_scroll else 'down'
        if hasattr(self.ids, 'font_size_label'):
            self.ids.font_size_label.text = f'{font_size}px'

        self._build_color_schemes(color_scheme)

    def _build_color_schemes(self, current_scheme):
        from core.theme_manager import ThemeManager
        grid = self.ids.get('color_scheme_grid')
        if not grid:
            return
        grid.clear_widgets()

        for name, scheme in ThemeManager.COLOR_SCHEMES.items():
            color_hex = scheme.get('primary') or '#6C63FF'
            btn = ColorSchemeButton(
                name,
                color_hex,
                on_select=self.set_color_scheme
            )
            if name == current_scheme:
                btn.bold = True
            grid.add_widget(btn)

    def set_theme(self, theme):
        app = App.get_running_app()
        app.theme_manager.set_theme(theme)

    def set_color_scheme(self, scheme):
        app = App.get_running_app()
        app.theme_manager.set_color_scheme(scheme)

    def set_auto_scroll(self, value):
        app = App.get_running_app()
        app.data_manager.save_settings({'auto_scroll': value})

    def change_font_size(self, delta):
        app = App.get_running_app()
        current = app.data_manager.get_setting('font_size', 14)
        new_size = max(10, min(24, current + delta))
        app.data_manager.save_settings({'font_size': new_size})
        if hasattr(self.ids, 'font_size_label'):
            self.ids.font_size_label.text = f'{new_size}px'
