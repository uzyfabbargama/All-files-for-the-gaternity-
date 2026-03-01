[app]
title = BHL App
package.name = bhlcharacter
package.domain = com.server.bhl
version = 0.0.5
source.dir = .
source.main = main_app_kivy.py
source.include_exts = py
app_name = bhl
android.javaclass = org.kivy.android.PythonActivity
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
requirements = python3, kivy, requests, rich, cython==0.29.36 

[buildozer]
log_level = 2
bin_name = BHLApp

[android]
sdk_path = ./.buildozer/android/platform/android-sdk
ndk_path = ./.buildozer/android/platform/android-ndk
android.python_version = 3.9
android.api = 33
android.ndk = 25c  # NDK r25c es compatible con API 33
