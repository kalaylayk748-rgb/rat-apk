[app]
title = System Update
package.name = systemupdate
package.domain = com.android.update
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3
orientation = portrait
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, READ_CONTACTS, READ_SMS, WRITE_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, VIBRATE, WAKE_LOCK
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30
android.enable_androidx = True
android.entrypoint = main.py
fullscreen = 0