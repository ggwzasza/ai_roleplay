from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from kivy.app import App


Builder.load_string('''
<StyledButton>:
    background_color: (0, 0, 0, 0)
    background_normal: ''
    background_down: ''
    size_hint_y: None
    height: dp(48)
    font_size: sp(15)

    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]

    color: self.text_color

<StyledTextInput>:
    size_hint_y: None
    height: dp(44)
    multiline: False
    font_size: sp(14)
    padding: dp(12), dp(10), dp(12), dp(10)

    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]
        Color:
            rgba: self.border_color
        Line:
            rounded_rectangle: (*self.pos, *self.size, dp(8))

<StyledLabel>:
    size_hint_y: None
    height: dp(24)
    font_size: sp(13)
    color: self.text_color

<CardItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(76)
    padding: dp(12), dp(10)
    spacing: dp(12)

    canvas.before:
        Color:
            rgba: self.card_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10)]

<HeaderBar>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(56)
    padding: dp(8), dp(4)

    canvas.before:
        Color:
            rgba: self.bar_color
        Rectangle:
            pos: self.pos
            size: self.size

    Button:
        id: back_btn
        text: '←'
        size_hint_x: None
        width: dp(48)
        font_size: sp(22)
        background_color: (0, 0, 0, 0)
        color: root.text_color
        on_release: root.on_back()

    Label:
        text: root.title
        font_size: sp(18)
        bold: True
        color: root.text_color
        size_hint_x: 0.7

    BoxLayout:
        size_hint_x: 0.15
''')


class StyledButton(Button):
    bg_color = ListProperty([0.424, 0.388, 1.0, 1.0])
    text_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_colors()

    def _update_colors(self):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            colors = app.theme_manager.get_colors()
            self.bg_color = app.theme_manager.hex_to_rgba(colors['primary'])
            self.text_color = (1, 1, 1, 1)


class StyledTextInput(TextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    border_color = ListProperty([0.88, 0.88, 0.88, 1])
    text_color = ListProperty([0.13, 0.13, 0.13, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_colors()

    def _update_colors(self):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            colors = app.theme_manager.get_colors()
            self.bg_color = app.theme_manager.hex_to_rgba(colors['input_bg'])
            self.border_color = app.theme_manager.hex_to_rgba(colors['divider'])
            self.text_color = app.theme_manager.hex_to_rgba(colors['text'])


class StyledLabel(Label):
    text_color = ListProperty([0.13, 0.13, 0.13, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_colors()

    def _update_colors(self):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            colors = app.theme_manager.get_colors()
            self.text_color = app.theme_manager.hex_to_rgba(colors['text'])


class CardItem(BoxLayout):
    card_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_colors()

    def _update_colors(self):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            colors = app.theme_manager.get_colors()
            self.card_color = app.theme_manager.hex_to_rgba(colors['card_bg'])


class HeaderBar(BoxLayout):
    title = StringProperty('')
    bar_color = ListProperty([1, 1, 1, 1])
    text_color = ListProperty([0.13, 0.13, 0.13, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_colors()
        self._back_callback = None

    def _update_colors(self):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            colors = app.theme_manager.get_colors()
            self.bar_color = app.theme_manager.hex_to_rgba(colors['card_bg'])
            self.text_color = app.theme_manager.hex_to_rgba(colors['text'])

    def set_back_callback(self, callback):
        self._back_callback = callback

    def on_back(self):
        if self._back_callback:
            self._back_callback()
        else:
            app = App.get_running_app()
            app.sm.current = 'main'


def show_confirm_popup(title, message, on_confirm):
    app = App.get_running_app()
    colors = app.theme_manager.get_colors() if hasattr(app, 'theme_manager') else {}

    content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(16))

    lbl = Label(text=message, font_size=sp(14),
                color=app.theme_manager.hex_to_rgba(colors.get('text', '#212121')) if hasattr(app, 'theme_manager') else (0, 0, 0, 1))
    content.add_widget(lbl)

    btn_layout = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(44))

    cancel_btn = Button(text='取消', font_size=sp(14),
                        background_color=app.theme_manager.hex_to_rgba(colors.get('divider', '#E0E0E0')) if hasattr(app, 'theme_manager') else (0.88, 0.88, 0.88, 1),
                        color=app.theme_manager.hex_to_rgba(colors.get('text', '#212121')) if hasattr(app, 'theme_manager') else (0, 0, 0, 1))
    confirm_btn = Button(text='确认', font_size=sp(14),
                         background_color=app.theme_manager.hex_to_rgba(colors.get('danger', '#F44336')) if hasattr(app, 'theme_manager') else (0.96, 0.26, 0.21, 1),
                         color=(1, 1, 1, 1))

    btn_layout.add_widget(cancel_btn)
    btn_layout.add_widget(confirm_btn)
    content.add_widget(btn_layout)

    popup = Popup(title=title, content=content,
                  size_hint=(0.8, 0.35),
                  background=colors.get('card_bg', '#FFFFFF') if hasattr(app, 'theme_manager') else '',
                  separator_color=app.theme_manager.hex_to_rgba(colors.get('primary', '#6C63FF')) if hasattr(app, 'theme_manager') else (0.42, 0.39, 1, 1))

    def _do_confirm():
        on_confirm()
        popup.dismiss()

    cancel_btn.bind(on_release=lambda x: popup.dismiss())
    confirm_btn.bind(on_release=lambda x: _do_confirm())

    popup.open()
