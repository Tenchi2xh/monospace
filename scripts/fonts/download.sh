#!/bin/bash

IOSEVKA_VERSION=1.14.3
IOSEVKA_VARIANT=ss10

wget -O iosevka.zip "https://github.com/be5invis/Iosevka/releases/download/v${IOSEVKA_VERSION}/iosevka-${IOSEVKA_VARIANT}-${IOSEVKA_VERSION}.zip"
unzip -j iosevka.zip 'ttf/*.ttf' -d iosevka
rename "s/-${IOSEVKA_VARIANT}//" iosevka/*
rm iosevka.zip

wget -O slab.zip "https://github.com/be5invis/Iosevka/releases/download/v${IOSEVKA_VERSION}/iosevka-slab-${IOSEVKA_VERSION}.zip"
unzip -j slab.zip 'ttf/*.ttf' -d iosevka
rm slab.zip
