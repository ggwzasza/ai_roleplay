import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.config import Config

Config.set('kivy', 'exit_on_escape', '0')
Config.set('kivy', 'softinput_mode', 'below_target')

from core.data_manager import DataManager
from core.api_client import APIClient
from core.theme_manager import ThemeManager
from ui.main_screen import MainScreen
from ui.chat.chat_list_screen import ChatListScreen
from ui.chat.chat_edit_screen import ChatEditScreen
from ui.chat.chat_screen import ChatScreen
from ui.character.character_list_screen import CharacterListScreen
from ui.character.character_edit_screen import CharacterEditScreen
from ui.character.user_character_screen import UserCharacterScreen
from ui.api_config.api_config_screen import APIConfigScreen
from ui.settings.settings_screen import SettingsScreen

SCREEN_BACK_MAP = {
    'chat_list': 'main',
    'chat_edit': 'chat_list',
    'chat': 'chat_list',
    'character_list': 'main',
    'character_edit': 'character_list',
    'user_character': 'character_list',
    'api_config': 'main',
    'settings': 'main',
}


class AIRoleplayApp(App):
    title = "AI 角色扮演"

    def build(self):
        self.data_manager = DataManager()
        self.api_client = APIClient(self.data_manager)
        self.theme_manager = ThemeManager(self.data_manager)

        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(ChatListScreen(name='chat_list'))
        self.sm.add_widget(ChatEditScreen(name='chat_edit'))
        self.sm.add_widget(ChatScreen(name='chat'))
        self.sm.add_widget(CharacterListScreen(name='character_list'))
        self.sm.add_widget(CharacterEditScreen(name='character_edit'))
        self.sm.add_widget(UserCharacterScreen(name='user_character'))
        self.sm.add_widget(APIConfigScreen(name='api_config'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        Window.bind(on_keyboard=self._on_keyboard)
        self.apply_theme()
        return self.sm

    def apply_theme(self):
        theme = self.data_manager.get_setting('theme', 'light')
        self.theme_manager.apply(theme)

    def switch_screen(self, screen_name, **kwargs):
        screen = self.sm.get_screen(screen_name)
        if hasattr(screen, 'load_data'):
            screen.load_data(**kwargs)
        self.sm.current = screen_name

    def _on_keyboard(self, instance, key, keycode, codepoint, modifier):
        if key in (27, 1001):
            current = self.sm.current
            if current == 'main':
                return False
            back_screen = SCREEN_BACK_MAP.get(current)
            if back_screen:
                self.sm.current = back_screen
                return True
            return False
        return False


if __name__ == '__main__':
    AIRoleplayApp().run()
