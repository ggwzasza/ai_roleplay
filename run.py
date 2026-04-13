import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
libs_dir = os.path.join(base_dir, 'libs')

if sys.platform == 'win32' and os.path.exists(libs_dir):
    sys.path.insert(0, libs_dir)

    sdl2_bin = os.path.join(libs_dir, 'share', 'sdl2', 'bin')
    glew_bin = os.path.join(libs_dir, 'share', 'glew', 'bin')
    angle_bin = os.path.join(libs_dir, 'share', 'angle', 'bin')

    os.environ['PATH'] = sdl2_bin + os.pathsep + glew_bin + os.pathsep + angle_bin + os.pathsep + os.environ.get('PATH', '')

    import ctypes
    dll_load_order = [
        os.path.join(angle_bin, 'd3dcompiler_47.dll'),
        os.path.join(angle_bin, 'libEGL.dll'),
        os.path.join(angle_bin, 'libGLESv2.dll'),
        os.path.join(glew_bin, 'glew32.dll'),
        os.path.join(sdl2_bin, 'SDL2.dll'),
        os.path.join(sdl2_bin, 'SDL2_image.dll'),
        os.path.join(sdl2_bin, 'SDL2_mixer.dll'),
        os.path.join(sdl2_bin, 'SDL2_ttf.dll'),
    ]

    for dll_path in dll_load_order:
        if os.path.exists(dll_path):
            try:
                ctypes.CDLL(dll_path)
            except OSError:
                pass

os.environ['KIVY_NO_ARGS'] = '1'


def find_cjk_font():
    if sys.platform == 'win32':
        fonts_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
        for name in ['msyh.ttc', 'simhei.ttf', 'msyhbd.ttc', 'simsun.ttc']:
            path = os.path.join(fonts_dir, name)
            if os.path.exists(path):
                return path
    elif sys.platform == 'darwin':
        for path in ['/System/Library/Fonts/PingFang.ttc',
                     '/System/Library/Fonts/STHeiti Light.ttc',
                     '/Library/Fonts/Arial Unicode.ttf']:
            if os.path.exists(path):
                return path
    elif hasattr(sys, 'getandroidapilevel'):
        for path in ['/system/fonts/NotoSansCJK-Regular.ttc',
                     '/system/fonts/NotoSansSC-Regular.otf',
                     '/system/fonts/DroidSansFallback.ttf',
                     '/system/fonts/DroidSansFallbackFull.ttf']:
            if os.path.exists(path):
                return path
    else:
        for path in ['/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
                     '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                     '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                     '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf']:
            if os.path.exists(path):
                return path
    return None


font_path = find_cjk_font()
if font_path:
    os.environ['KIVY_FONT_PATH'] = os.path.dirname(font_path)

import kivy
from kivy.config import Config

Config.set('kivy', 'softinput_mode', 'below_target')
Config.set('kivy', 'exit_on_escape', '0')

if font_path:
    Config.set('kivy', 'default_font',
               ['CJK', font_path, font_path, font_path, font_path])

from main import AIRoleplayApp

if __name__ == '__main__':
    AIRoleplayApp().run()
