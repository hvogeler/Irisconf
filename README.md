1. Convert json keymap from https://config.qmk.fm/ to keymap.c
qmk json2c -o keymap.c hvo07.json
qmk compile
cp keymap.c /home/hvo/tmp/qmk_firmware/keyboards/keebio/iris/keymaps/hvo
2. edit the rules.mk file
3. run \Users\hvogeler\bin\qmk_toolbox.exe, select the hex file, press flash button under keyboards and flash.


