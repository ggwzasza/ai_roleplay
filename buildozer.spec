[app]

title = AI Roleplay
package.name = airoleplay
package.domain = org.airoleplay
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,ttc,otf
source.exclude_dirs = libs, tests, bin, __pycache__, .git, .github
version = 1.0.0
requirements = python3,kivy,Pillow,openai
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = master
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
