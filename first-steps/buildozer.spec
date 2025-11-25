[app]
title = Тур-Счётчик
package.name = tourcounter
package.domain = com.natalya
source.dir = .
source.include_exts = py,json
version = 0.1

requirements = python3,kivy,android,jnius

android.permissions = WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.use_androidx = True
android.legacy_build = False

[buildozer]
log_level = 2
