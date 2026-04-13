from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior


Builder.load_string('''
<NavButton>:
    canvas.before:
        Clear
    orientation: 'vertical'
    size_hint_y: None
    height: dp(64)
    padding: dp(4), dp(4)
    spacing: dp(2)

    Label:
        id: icon_label
        font_size: sp(22)
        size_hint_y: None
        height: self.texture_size[1]
        color: root.icon_color

    Label:
        id: text_label
        font_size: sp(11)
        size_hint_y: None
        height: self.texture_size[1]
        color: root.icon_color
        text: root.text

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['bg'])
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            id: content_area
            size_hint_y: 0.9
            orientation: 'vertical'
            padding: dp(16), dp(16)
            spacing: dp(12)

            Label:
                text: 'AI 角色扮演'
                font_size: sp(28)
                bold: True
                size_hint_y: None
                height: dp(50)
                color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['primary'])

            Label:
                text: '沉浸式AI角色扮演体验'
                font_size: sp(14)
                size_hint_y: None
                height: dp(30)
                color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])

            ScrollView:
                GridLayout:
                    cols: 2
                    spacing: dp(12)
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(8)

                    FeatureCard:
                        icon: '💬'
                        title: '对话'
                        desc: '开始或继续一段角色扮演对话'
                        on_release: app.switch_screen('chat_list')

                    FeatureCard:
                        icon: '🎭'
                        title: '角色库'
                        desc: '管理和创建AI角色'
                        on_release: app.switch_screen('character_list')

                    FeatureCard:
                        icon: '🔌'
                        title: 'API配置'
                        desc: '配置AI模型接口'
                        on_release: app.switch_screen('api_config')

                    FeatureCard:
                        icon: '⚙️'
                        title: '设置'
                        desc: '个性化你的应用'
                        on_release: app.switch_screen('settings')

        BoxLayout:
            id: nav_bar
            size_hint_y: 0.1
            padding: dp(8), dp(0)

            canvas.before:
                Color:
                    rgba: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['nav_bg'])
                RoundedRectangle:
                    pos: self.pos
                    size: self.size

            NavButton:
                text: '对话'
                icon_text: '💬'
                active: True
                on_release: app.switch_screen('chat_list')

            NavButton:
                text: '角色'
                icon_text: '🎭'
                on_release: app.switch_screen('character_list')

            NavButton:
                text: 'API'
                icon_text: '🔌'
                on_release: app.switch_screen('api_config')

            NavButton:
                text: '设置'
                icon_text: '⚙️'
                on_release: app.switch_screen('settings')

<FeatureCard@ButtonBehavior+BoxLayout>:
    icon: ''
    title: ''
    desc: ''
    orientation: 'vertical'
    padding: dp(16), dp(12)
    spacing: dp(6)
    size_hint_y: None
    height: dp(140)

    canvas.before:
        Color:
            rgba: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['card_bg'])
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
        Color:
            rgba: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['divider'], 0.3)
        Line:
            rounded_rectangle: (*self.pos, *self.size, dp(12))

    Label:
        text: root.icon
        font_size: sp(36)
        size_hint_y: None
        height: dp(44)

    Label:
        text: root.title
        font_size: sp(16)
        bold: True
        size_hint_y: None
        height: dp(24)
        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text'])

    Label:
        text: root.desc
        font_size: sp(11)
        size_hint_y: None
        height: dp(20)
        color: app.theme_manager.hex_to_rgba(app.theme_manager.get_colors()['text_secondary'])
''')


class NavButton(ButtonBehavior, BoxLayout):
    text = StringProperty('')
    icon_text = StringProperty('')
    active = ObjectProperty(False)
    icon_color = ListProperty([0.62, 0.62, 0.62, 1.0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self._update_color)

    def _update_color(self, instance, value):
        app = self.get_app()
        if app:
            colors = app.theme_manager.get_colors()
            if value:
                self.icon_color = app.theme_manager.hex_to_rgba(colors['nav_active'])
            else:
                self.icon_color = app.theme_manager.hex_to_rgba(colors['nav_inactive'])

    def get_app(self):
        from kivy.app import App
        return App.get_running_app()


class MainScreen(Screen):
    pass
