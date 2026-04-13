from kivy.core.window import Window


class ThemeManager:
    THEMES = {
        'light': {
            'bg': '#F5F5F5',
            'card_bg': '#FFFFFF',
            'text': '#212121',
            'text_secondary': '#757575',
            'primary': '#6C63FF',
            'primary_dark': '#5A52D5',
            'accent': '#FF6584',
            'divider': '#E0E0E0',
            'bubble_user': '#DCF8C6',
            'bubble_ai': '#FFFFFF',
            'input_bg': '#FFFFFF',
            'nav_bg': '#FFFFFF',
            'nav_active': '#6C63FF',
            'nav_inactive': '#9E9E9E',
            'danger': '#F44336',
            'success': '#4CAF50',
        },
        'dark': {
            'bg': '#121212',
            'card_bg': '#1E1E1E',
            'text': '#E0E0E0',
            'text_secondary': '#9E9E9E',
            'primary': '#BB86FC',
            'primary_dark': '#9B67DC',
            'accent': '#CF6679',
            'divider': '#333333',
            'bubble_user': '#2E4A2E',
            'bubble_ai': '#2A2A2A',
            'input_bg': '#2A2A2A',
            'nav_bg': '#1E1E1E',
            'nav_active': '#BB86FC',
            'nav_inactive': '#757575',
            'danger': '#CF6679',
            'success': '#81C784',
        }
    }

    COLOR_SCHEMES = {
        'default': {'primary': None, 'accent': None},
        'ocean': {'primary': '#0288D1', 'accent': '#26C6DA'},
        'forest': {'primary': '#388E3C', 'accent': '#8BC34A'},
        'sunset': {'primary': '#E64A19', 'accent': '#FFB74D'},
        'rose': {'primary': '#C2185B', 'accent': '#F48FB1'},
    }

    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.current_theme = data_manager.get_setting('theme', 'light')
        self.current_scheme = data_manager.get_setting('color_scheme', 'default')

    def apply(self, theme=None):
        if theme:
            self.current_theme = theme
        colors = self.get_colors()
        try:
            Window.clearcolor = self._hex_to_kv(colors['bg'])
        except (AttributeError, TypeError):
            pass

    def get_colors(self):
        base = dict(self.THEMES.get(self.current_theme, self.THEMES['light']))
        scheme = self.COLOR_SCHEMES.get(self.current_scheme, self.COLOR_SCHEMES['default'])
        if scheme.get('primary'):
            base['primary'] = scheme['primary']
        if scheme.get('accent'):
            base['accent'] = scheme['accent']
        return base

    def set_theme(self, theme):
        self.current_theme = theme
        self.data_manager.save_settings({'theme': theme})
        self.apply()

    def set_color_scheme(self, scheme):
        self.current_scheme = scheme
        self.data_manager.save_settings({'color_scheme': scheme})
        self.apply()

    @staticmethod
    def _hex_to_kv(hex_color):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, 1.0)

    @staticmethod
    def hex_to_rgba(hex_color, alpha=1.0):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, alpha)
