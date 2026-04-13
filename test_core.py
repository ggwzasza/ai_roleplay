import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs'))

from core.data_manager import DataManager
from core.api_client import APIClient
from core.theme_manager import ThemeManager


def test_data_manager():
    dm = DataManager()
    print("[PASS] DataManager initialized")

    api_id = dm.save_api({
        'name': 'TestAPI',
        'url': 'https://api.example.com/v1',
        'api_key': 'sk-test123',
        'model': 'gpt-3.5-turbo',
        'system_prompt': 'You are a helpful assistant.',
        'prefix_prompt': ''
    })
    print(f"[PASS] API saved with id: {api_id}")

    char_id = dm.save_character({
        'name': '艾莉丝',
        'age': '25',
        'race': '精灵',
        'body': '纤细高挑',
        'experience': '千年森林守护者',
        'personality': '温柔但偶尔高傲',
        'speech_style': '优雅古风',
        'habits': '喜欢在月光下独处',
        'api_id': api_id
    })
    print(f"[PASS] Character saved with id: {char_id}")

    chat_id = dm.save_chat({
        'name': '森林奇遇',
        'character_ids': [char_id],
        'macro_prompt': '这是一个魔法与剑的世界',
        'memory_count': 20,
        'prefix_prompt': '请严格扮演你的角色'
    })
    print(f"[PASS] Chat saved with id: {chat_id}")

    dm.add_message_to_chat(chat_id, 'user', '你好，你是谁？')
    dm.add_message_to_chat(chat_id, 'assistant', '我是艾莉丝，千年森林的守护者。', char_id)
    print("[PASS] Messages added to chat")

    chat = dm.get_chat(chat_id)
    assert len(chat['messages']) == 2
    print("[PASS] Chat messages verified")

    apis = dm.get_api_list()
    assert len(apis) >= 1
    print("[PASS] API list retrieved")

    chars = dm.get_character_list()
    assert len(chars) >= 1
    print("[PASS] Character list retrieved")

    chats = dm.get_chat_list()
    assert len(chats) >= 1
    print("[PASS] Chat list retrieved")

    dm.delete_chat(chat_id)
    dm.delete_character(char_id)
    dm.delete_api(api_id)
    print("[PASS] Cleanup completed")

    return True


def test_api_client():
    dm = DataManager()
    client = APIClient(dm)

    api_id = dm.save_api({
        'name': 'DeepSeek',
        'url': 'https://api.deepseek.com',
        'api_key': 'sk-test123',
        'model': 'deepseek-reasoner',
        'temperature': 0.8,
        'max_tokens': 2048,
        'system_prompt': 'You are a helpful assistant.',
        'prefix_prompt': 'Always respond in character.'
    })

    char1_id = dm.save_character({
        'name': '艾莉丝',
        'age': '25',
        'race': '精灵',
        'body': '纤细高挑',
        'experience': '千年森林守护者',
        'personality': '温柔但偶尔高傲',
        'speech_style': '优雅古风',
        'habits': '喜欢在月光下独处',
        'api_id': api_id
    })

    char2_id = dm.save_character({
        'name': '凯恩',
        'age': '30',
        'race': '人类',
        'body': '魁梧健壮',
        'experience': '退役骑士',
        'personality': '沉默寡言但忠诚',
        'speech_style': '简短有力',
        'habits': '习惯性地擦拭剑柄',
        'api_id': api_id
    })

    chat_id = dm.save_chat({
        'name': '森林奇遇',
        'character_ids': [char1_id, char2_id],
        'macro_prompt': '这是一个魔法与剑的世界',
        'memory_count': 20,
        'prefix_prompt': '请严格扮演你的角色'
    })

    dm.add_message_to_chat(chat_id, 'user', '你好')
    dm.add_message_to_chat(chat_id, 'assistant', '你好，旅人。', char1_id)

    prompt = client.build_system_prompt(char1_id, dm.get_chat(chat_id))
    assert '艾莉丝' in prompt
    assert '精灵' in prompt
    assert '重要规则' in prompt
    print("[PASS] System prompt built correctly")
    print(f"  Prompt preview: {prompt[:100]}...")

    prompt_with_context = client.build_system_prompt(
        char2_id, dm.get_chat(chat_id),
        other_character_outputs=[('艾莉丝', '你好，旅人。愿月光指引你的道路。')]
    )
    assert '艾莉丝' in prompt_with_context
    assert '其他角色已经做出的反应' in prompt_with_context
    print("[PASS] Multi-character context prompt built correctly")

    messages = client.build_messages(chat_id, char1_id, '你是谁？')
    assert len(messages) >= 3
    assert messages[0]['role'] == 'system'
    print("[PASS] Messages built correctly")

    messages_with_ctx = client.build_messages(
        chat_id, char2_id, '你是谁？',
        other_character_outputs=[('艾莉丝', '我是艾莉丝，森林守护者。')]
    )
    assert '艾莉丝' in messages_with_ctx[0]['content']
    print("[PASS] Messages with other character context built correctly")

    dm.delete_chat(chat_id)
    dm.delete_character(char1_id)
    dm.delete_character(char2_id)
    dm.delete_api(api_id)

    return True


def test_theme_manager():
    dm = DataManager()
    tm = ThemeManager(dm)

    colors = tm.get_colors()
    assert 'primary' in colors
    assert 'bg' in colors
    print(f"[PASS] Theme colors retrieved, primary: {colors['primary']}")

    tm.set_theme('dark')
    colors = tm.get_colors()
    assert colors['bg'] == '#121212'
    print("[PASS] Dark theme applied")

    tm.set_theme('light')
    colors = tm.get_colors()
    assert colors['bg'] == '#F5F5F5'
    print("[PASS] Light theme restored")

    tm.set_color_scheme('ocean')
    colors = tm.get_colors()
    assert colors['primary'] == '#0288D1'
    print("[PASS] Ocean color scheme applied")

    tm.set_color_scheme('default')
    print("[PASS] Default color scheme restored")

    return True


if __name__ == '__main__':
    print("=" * 50)
    print("AI Roleplay Framework - Module Tests")
    print("=" * 50)

    print("\n--- Testing DataManager ---")
    test_data_manager()

    print("\n--- Testing APIClient ---")
    test_api_client()

    print("\n--- Testing ThemeManager ---")
    test_theme_manager()

    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)
