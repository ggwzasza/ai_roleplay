[app]

title = AI Roleplay
package.name = airoleplay
package.domain = org.airoleplay
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,ttc,otf
source.exclude_dirs = libs, tests, bin, __pycache__, .git, .github
version = 1.0.0
requirements = python3,kivy==2.3.1,Pillow,openai,plyer,openssl
orientation = portrait
fullscreen = 1
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
android.statusbar_color = #6C63FF
p4a.branch = master
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
