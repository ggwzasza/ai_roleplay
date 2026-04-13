import os
import sys


def find_cjk_font():
    if sys.platform == 'win32':
        fonts_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
        candidates = ['msyh.ttc', 'simhei.ttf', 'msyhbd.ttc', 'simsun.ttc']
        for name in candidates:
            path = os.path.join(fonts_dir, name)
            if os.path.exists(path):
                return path
    elif sys.platform == 'darwin':
        candidates = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
    elif hasattr(sys, 'getandroidapilevel'):
        candidates = [
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/NotoSansSC-Regular.otf',
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/DroidSansFallbackFull.ttf',
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
    else:
        candidates = [
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
    return None


def setup_kivy_font():
    font_path = find_cjk_font()
    if font_path:
        os.environ['KIVY_FONT_PATH'] = os.path.dirname(font_path)
        from kivy.config import Config
        Config.set('kivy', 'default_font', [
            'CJK', font_path, font_path, font_path, font_path
        ])
    return font_path
