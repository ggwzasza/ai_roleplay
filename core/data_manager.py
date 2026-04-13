import copy
import json
import os
import shutil
import uuid
from datetime import datetime
from PIL import Image


class DataManager:
    def _get_data_dir(self):
        import sys
        if hasattr(sys, 'getandroidapilevel'):
            try:
                from android.storage import app_storage_path
                return os.path.join(app_storage_path(), 'ai_roleplay')
            except ImportError:
                pass
        return os.path.join(os.path.expanduser('~'), '.ai_roleplay')

    DATA_DIR = None
    CHATS_DIR = None
    CHARACTERS_DIR = None
    APIS_DIR = None
    ASSETS_DIR = None
    SETTINGS_FILE = None
    USER_CHARACTER_FILE = None

    def __init__(self):
        self.DATA_DIR = self._get_data_dir()
        self.CHATS_DIR = os.path.join(self.DATA_DIR, 'chats')
        self.CHARACTERS_DIR = os.path.join(self.DATA_DIR, 'characters')
        self.APIS_DIR = os.path.join(self.DATA_DIR, 'apis')
        self.ASSETS_DIR = os.path.join(self.DATA_DIR, 'assets')
        self.SETTINGS_FILE = os.path.join(self.DATA_DIR, 'settings.json')
        self.USER_CHARACTER_FILE = os.path.join(self.DATA_DIR, 'user_character.json')
        self._ensure_dirs()
        self.settings = self._load_settings()
        self.user_character = self._load_user_character()

    def _ensure_dirs(self):
        for d in [self.DATA_DIR, self.CHATS_DIR, self.CHARACTERS_DIR,
                  self.APIS_DIR, self.ASSETS_DIR]:
            os.makedirs(d, exist_ok=True)

    # ==================== Settings ====================
    def _load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'theme': 'light',
            'color_scheme': 'default',
            'font_size': 14,
            'auto_scroll': True
        }

    def save_settings(self, settings=None):
        if settings:
            self.settings.update(settings)
        with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    # ==================== User Character ====================
    def _load_user_character(self):
        if os.path.exists(self.USER_CHARACTER_FILE):
            with open(self.USER_CHARACTER_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'prompt': ''}

    def save_user_character(self, data):
        self.user_character = data
        with open(self.USER_CHARACTER_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ==================== Chats ====================
    def get_chat_list(self):
        chats = []
        for fname in os.listdir(self.CHATS_DIR):
            if fname.endswith('.json'):
                with open(os.path.join(self.CHATS_DIR, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    chats.append({
                        'id': data['id'],
                        'name': data.get('name', '未命名对话'),
                        'created_at': data.get('created_at', ''),
                        'updated_at': data.get('updated_at', '')
                    })
        chats.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return chats

    def get_chat(self, chat_id):
        path = os.path.join(self.CHATS_DIR, f'{chat_id}.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_chat(self, chat_data):
        chat_data = copy.deepcopy(chat_data)
        if 'id' not in chat_data:
            chat_data['id'] = str(uuid.uuid4())
        chat_data['updated_at'] = datetime.now().isoformat()
        if 'created_at' not in chat_data:
            chat_data['created_at'] = chat_data['updated_at']
        path = os.path.join(self.CHATS_DIR, f'{chat_data["id"]}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, ensure_ascii=False, indent=2)
        return chat_data['id']

    def delete_chat(self, chat_id):
        path = os.path.join(self.CHATS_DIR, f'{chat_id}.json')
        if os.path.exists(path):
            os.remove(path)
        bg_path = os.path.join(self.ASSETS_DIR, f'chat_bg_{chat_id}.png')
        if os.path.exists(bg_path):
            os.remove(bg_path)

    def add_message_to_chat(self, chat_id, role, content, character_id=None):
        chat = self.get_chat(chat_id)
        if chat is None:
            return
        message = {
            'role': role,
            'content': content,
            'character_id': character_id,
            'timestamp': datetime.now().isoformat()
        }
        if 'messages' not in chat:
            chat['messages'] = []
        chat['messages'].append(message)
        self.save_chat(chat)

    # ==================== Characters ====================
    def get_character_list(self):
        characters = []
        for fname in os.listdir(self.CHARACTERS_DIR):
            if fname.endswith('.json'):
                with open(os.path.join(self.CHARACTERS_DIR, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    characters.append({
                        'id': data['id'],
                        'name': data.get('name', '未命名角色'),
                        'avatar': data.get('avatar', '')
                    })
        return characters

    def get_character(self, character_id):
        path = os.path.join(self.CHARACTERS_DIR, f'{character_id}.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_character(self, character_data):
        character_data = copy.deepcopy(character_data)
        if 'id' not in character_data:
            character_data['id'] = str(uuid.uuid4())
        path = os.path.join(self.CHARACTERS_DIR, f'{character_data["id"]}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(character_data, f, ensure_ascii=False, indent=2)
        return character_data['id']

    def delete_character(self, character_id):
        path = os.path.join(self.CHARACTERS_DIR, f'{character_id}.json')
        if os.path.exists(path):
            os.remove(path)
        avatar_path = os.path.join(self.ASSETS_DIR, f'avatar_{character_id}.png')
        if os.path.exists(avatar_path):
            os.remove(avatar_path)

    # ==================== API Configs ====================
    def get_api_list(self):
        apis = []
        for fname in os.listdir(self.APIS_DIR):
            if fname.endswith('.json'):
                with open(os.path.join(self.APIS_DIR, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    apis.append({
                        'id': data['id'],
                        'name': data.get('name', '未命名API'),
                        'url': data.get('url', ''),
                        'api_key': data.get('api_key', '')
                    })
        return apis

    def get_api(self, api_id):
        path = os.path.join(self.APIS_DIR, f'{api_id}.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_api(self, api_data):
        api_data = copy.deepcopy(api_data)
        if 'id' not in api_data:
            api_data['id'] = str(uuid.uuid4())
        path = os.path.join(self.APIS_DIR, f'{api_data["id"]}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, ensure_ascii=False, indent=2)
        return api_data['id']

    def delete_api(self, api_id):
        path = os.path.join(self.APIS_DIR, f'{api_id}.json')
        if os.path.exists(path):
            os.remove(path)

    # ==================== Assets ====================
    def save_avatar(self, character_id, source_path):
        dest = os.path.join(self.ASSETS_DIR, f'avatar_{character_id}.png')
        self._resize_and_save(source_path, dest, (256, 256))
        return dest

    def save_chat_background(self, chat_id, source_path):
        dest = os.path.join(self.ASSETS_DIR, f'chat_bg_{chat_id}.png')
        self._resize_and_save(source_path, dest, (1920, 1080))
        return dest

    def get_avatar_path(self, character_id):
        path = os.path.join(self.ASSETS_DIR, f'avatar_{character_id}.png')
        return path if os.path.exists(path) else ''

    def get_chat_bg_path(self, chat_id):
        path = os.path.join(self.ASSETS_DIR, f'chat_bg_{chat_id}.png')
        return path if os.path.exists(path) else ''

    def _resize_and_save(self, source_path, dest_path, max_size):
        img = Image.open(source_path)
        img.thumbnail(max_size, Image.LANCZOS)
        img.save(dest_path, 'PNG')

    def copy_asset(self, source_path, dest_filename):
        dest = os.path.join(self.ASSETS_DIR, dest_filename)
        shutil.copy2(source_path, dest)
        return dest
