{
    "patcher": {
        "fileversion": 1,
        "appversion": {
            "major": 9,
            "minor": 1,
            "revision": 4,
            "architecture": "x64",
            "modernui": 1
        },
        "classnamespace": "box",
        "rect": [ 60.0, 100.0, 800.0, 600.0 ],
        "openinpresentation": 1,
        "boxes": [
            {
                "box": {
                    "id": "obj-12",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 484.0, 522.0, 47.0, 22.0 ],
                    "text": "s piezo"
                }
            },
            {
                "box": {
                    "id": "obj-10",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 274.0, 522.0, 65.0, 22.0 ],
                    "text": "s pressure"
                }
            },
            {
                "box": {
                    "id": "obj-7",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 36.5, 522.0, 31.0, 22.0 ],
                    "text": "s tof"
                }
            },
            {
                "box": {
                    "comment": "start receiving data",
                    "id": "obj-6",
                    "index": 2,
                    "maxclass": "inlet",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 489.0, 160.0, 30.0, 30.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-44",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 8.0, 640.0, 88.0, 20.0 ],
                    "text": "TOF"
                }
            },
            {
                "box": {
                    "id": "obj-42",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 115.0, 640.0, 88.0, 20.0 ],
                    "text": "PRESSURE"
                }
            },
            {
                "box": {
                    "id": "obj-41",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 238.5, 640.0, 88.0, 20.0 ],
                    "text": "PIEZO_HIT"
                }
            },
            {
                "box": {
                    "id": "obj-40",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 341.0, 640.0, 108.0, 20.0 ],
                    "text": "PIEZO_STREAM"
                }
            },
            {
                "box": {
                    "hint": "npm install",
                    "id": "obj-38",
                    "maxclass": "textbutton",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 274.0, 257.0, 100.0, 20.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 14.0, 67.0, 74.0, 20.0 ],
                    "text": "close serial",
                    "texton": "close serial"
                }
            },
            {
                "box": {
                    "comment": "",
                    "id": "obj-35",
                    "index": 1,
                    "maxclass": "inlet",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 30.5, 10.0, 30.0, 30.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-33",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 892.0, 135.0, 150.0, 33.0 ],
                    "presentation": 1,
                    "presentation_linecount": 2,
                    "presentation_rect": [ 116.0, 91.0, 150.0, 33.0 ],
                    "text": "pressure port: usbmodem1423401"
                }
            },
            {
                "box": {
                    "id": "obj-34",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 892.0, 89.0, 149.0, 22.0 ],
                    "text": "prepend set pressure port:"
                }
            },
            {
                "box": {
                    "id": "obj-32",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 726.0, 135.0, 150.0, 33.0 ],
                    "presentation": 1,
                    "presentation_linecount": 2,
                    "presentation_rect": [ 116.0, 50.0, 150.0, 33.0 ],
                    "text": "pressure port: usbmodem1423101"
                }
            },
            {
                "box": {
                    "id": "obj-31",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 567.0, 135.0, 150.0, 33.0 ],
                    "presentation": 1,
                    "presentation_linecount": 2,
                    "presentation_rect": [ 116.0, 8.0, 150.0, 33.0 ],
                    "text": "tof port: usbmodem1423301"
                }
            },
            {
                "box": {
                    "id": "obj-23",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 726.0, 89.0, 149.0, 22.0 ],
                    "text": "prepend set pressure port:"
                }
            },
            {
                "box": {
                    "id": "obj-22",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 567.0, 89.0, 116.0, 22.0 ],
                    "text": "prepend set tof port:"
                }
            },
            {
                "box": {
                    "hint": "npm install",
                    "id": "obj-21",
                    "maxclass": "textbutton",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 324.0, 50.0, 100.0, 20.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 14.0, 42.0, 74.0, 20.0 ],
                    "text": "npm install",
                    "texton": "npm install"
                }
            },
            {
                "box": {
                    "id": "obj-8",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 258.0, 80.0, 64.0, 22.0 ],
                    "text": "script start"
                }
            },
            {
                "box": {
                    "id": "obj-43",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 324.0, 80.0, 100.0, 22.0 ],
                    "text": "script npm install"
                }
            },
            {
                "box": {
                    "id": "obj-16",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 341.0, 609.0, 50.0, 22.0 ],
                    "text": "0 0 1 0"
                }
            },
            {
                "box": {
                    "id": "obj-15",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 238.5, 609.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-14",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 115.0, 609.0, 71.0, 22.0 ],
                    "text": "0. 0. 277 11"
                }
            },
            {
                "box": {
                    "id": "obj-13",
                    "linecount": 2,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 8.0, 609.0, 75.0, 35.0 ],
                    "text": "138 45 137 44 0. 0."
                }
            },
            {
                "box": {
                    "id": "obj-11",
                    "maxclass": "toggle",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 484.0, 217.0, 24.0, 24.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 14.0, 96.0, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-9",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 274.0, 288.0, 37.0, 22.0 ],
                    "text": "close"
                }
            },
            {
                "box": {
                    "fontsize": 13.0,
                    "id": "obj-1",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 64.0, 10.0, 800.0, 21.0 ],
                    "text": "AUTO-DETECT TEST PATCH — auto_detect.js autostart on load. Press RESCAN to re-trigger after replug."
                }
            },
            {
                "box": {
                    "id": "obj-2",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 433.0, 54.0, 250.0, 20.0 ],
                    "text": "1. Auto-detect (calls auto_detect.js)"
                }
            },
            {
                "box": {
                    "id": "obj-rescan",
                    "maxclass": "button",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 64.0, 48.0, 24.0, 24.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 14.0, 12.0, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-rescan-label",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 92.0, 50.0, 60.0, 20.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 42.0, 14.0, 60.0, 20.0 ],
                    "text": "RESCAN"
                }
            },
            {
                "box": {
                    "id": "obj-scan-msg",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 64.0, 80.0, 50.0, 22.0 ],
                    "text": "scan"
                }
            },
            {
                "box": {
                    "id": "obj-node",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 64.0, 120.0, 360.0, 22.0 ],
                    "saved_object_attributes": {
                        "autostart": 1,
                        "defer": 0,
                        "node_bin_path": "",
                        "npm_bin_path": "",
                        "watch": 0
                    },
                    "text": "node.script auto_detect.js @autostart 1",
                    "textfile": {
                        "filename": "auto_detect.js",
                        "flags": 0,
                        "embed": 0,
                        "autowatch": 1
                    }
                }
            },
            {
                "box": {
                    "id": "obj-metro",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 484.0, 248.0, 56.0, 22.0 ],
                    "text": "metro 50"
                }
            },
            {
                "box": {
                    "id": "obj-route-auto",
                    "maxclass": "newobj",
                    "numinlets": 7,
                    "numoutlets": 7,
                    "outlettype": [ "", "", "", "", "", "", "" ],
                    "patching_rect": [ 64.0, 160.0, 420.0, 22.0 ],
                    "text": "route tof pressure piezo missing done error"
                }
            },
            {
                "box": {
                    "id": "obj-print-missing",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 567.0, 180.0, 130.0, 22.0 ],
                    "text": "print MISSING"
                }
            },
            {
                "box": {
                    "id": "obj-print-done",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 567.0, 210.0, 130.0, 22.0 ],
                    "text": "print DONE"
                }
            },
            {
                "box": {
                    "id": "obj-print-error",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 567.0, 240.0, 130.0, 22.0 ],
                    "text": "print ERROR"
                }
            },
            {
                "box": {
                    "id": "obj-3",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 293.0, 205.0, 138.0, 33.0 ],
                    "text": "2. Open serial port (\"port $1, open\" macro)"
                }
            },
            {
                "box": {
                    "id": "obj-tof-portmsg",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 64.0, 267.0, 80.0, 22.0 ],
                    "text": "port $1, open"
                }
            },
            {
                "box": {
                    "id": "obj-pres-portmsg",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 131.0, 233.0, 85.0, 22.0 ],
                    "text": "port $1, open"
                }
            },
            {
                "box": {
                    "id": "obj-piezo-portmsg",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 198.0, 204.0, 89.0, 22.0 ],
                    "text": "port $1, open"
                }
            },
            {
                "box": {
                    "id": "obj-serial-tof",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "int", "" ],
                    "patching_rect": [ 64.0, 336.0, 200.0, 22.0 ],
                    "text": "serial a 115200 8 1"
                }
            },
            {
                "box": {
                    "id": "obj-serial-pres",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "int", "" ],
                    "patching_rect": [ 274.0, 336.0, 200.0, 22.0 ],
                    "text": "serial b 115200 8 1"
                }
            },
            {
                "box": {
                    "id": "obj-serial-piezo",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "int", "" ],
                    "patching_rect": [ 484.0, 336.0, 200.0, 22.0 ],
                    "text": "serial c 115200 8 1"
                }
            },
            {
                "box": {
                    "id": "obj-4",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 78.0, 367.0, 400.0, 20.0 ],
                    "text": "3. Parse line-buffered text (sel 10 13 → zl group → itoa → fromsymbol)"
                }
            },
            {
                "box": {
                    "id": "obj-sel-tof",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 3,
                    "outlettype": [ "bang", "bang", "" ],
                    "patching_rect": [ 64.0, 396.0, 80.0, 22.0 ],
                    "text": "sel 10 13"
                }
            },
            {
                "box": {
                    "id": "obj-sel-pres",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 3,
                    "outlettype": [ "bang", "bang", "" ],
                    "patching_rect": [ 274.0, 396.0, 80.0, 22.0 ],
                    "text": "sel 10 13"
                }
            },
            {
                "box": {
                    "id": "obj-sel-piezo",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 3,
                    "outlettype": [ "bang", "bang", "" ],
                    "patching_rect": [ 484.0, 396.0, 80.0, 22.0 ],
                    "text": "sel 10 13"
                }
            },
            {
                "box": {
                    "id": "obj-zl-tof",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 64.0, 426.0, 100.0, 22.0 ],
                    "text": "zl group 1000"
                }
            },
            {
                "box": {
                    "id": "obj-zl-pres",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 274.0, 426.0, 100.0, 22.0 ],
                    "text": "zl group 1000"
                }
            },
            {
                "box": {
                    "id": "obj-zl-piezo",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 484.0, 426.0, 100.0, 22.0 ],
                    "text": "zl group 1000"
                }
            },
            {
                "box": {
                    "id": "obj-itoa-tof",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 64.0, 456.0, 60.0, 22.0 ],
                    "text": "itoa"
                }
            },
            {
                "box": {
                    "id": "obj-itoa-pres",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 274.0, 456.0, 60.0, 22.0 ],
                    "text": "itoa"
                }
            },
            {
                "box": {
                    "id": "obj-itoa-piezo",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 484.0, 456.0, 60.0, 22.0 ],
                    "text": "itoa"
                }
            },
            {
                "box": {
                    "id": "obj-fs-tof",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 64.0, 486.0, 100.0, 22.0 ],
                    "text": "fromsymbol"
                }
            },
            {
                "box": {
                    "id": "obj-fs-pres",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 274.0, 486.0, 100.0, 22.0 ],
                    "text": "fromsymbol"
                }
            },
            {
                "box": {
                    "id": "obj-fs-piezo",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 484.0, 486.0, 100.0, 22.0 ],
                    "text": "fromsymbol"
                }
            },
            {
                "box": {
                    "id": "obj-5",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 498.0, 549.0, 243.0, 33.0 ],
                    "text": "4. Merged content router — three serials → one route, dispatched by message prefix"
                }
            },
            {
                "box": {
                    "id": "obj-route-data",
                    "maxclass": "newobj",
                    "numinlets": 5,
                    "numoutlets": 5,
                    "outlettype": [ "", "", "", "", "" ],
                    "patching_rect": [ 64.0, 549.0, 430.0, 22.0 ],
                    "text": "route /tof /pressure /piezo /piezo/stream"
                }
            },
            {
                "box": {
                    "id": "obj-help",
                    "linecount": 6,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 8.0, 667.0, 627.0, 87.0 ],
                    "presentation": 1,
                    "presentation_linecount": 6,
                    "presentation_rect": [ 14.0, 134.0, 627.0, 87.0 ],
                    "text": "Test flow:\n  1. Plug in all 3 ESP32s before opening this patch\n  2. Open patch → node.script @autostart triggers auto_detect.js → port names appear in the message boxes above\n  3. Click each \"port $1, open\" message OR wire a [t b s] to auto-trigger them\n  4. Watch the Max console: TOF prints fX/fY/rX/rY/vX/vY, PRESSURE prints norm1 norm2 raw1 raw2,\n     PIEZO_HIT prints on each strike, PIEZO_STREAM prints 50Hz activity for 4 channels"
                }
            }
        ],
        "lines": [
            {
                "patchline": {
                    "destination": [ "obj-metro", 0 ],
                    "source": [ "obj-11", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-43", 0 ],
                    "source": [ "obj-21", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-31", 0 ],
                    "source": [ "obj-22", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-32", 0 ],
                    "source": [ "obj-23", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-33", 0 ],
                    "source": [ "obj-34", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-rescan", 0 ],
                    "source": [ "obj-35", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-9", 0 ],
                    "source": [ "obj-38", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-node", 0 ],
                    "source": [ "obj-43", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-11", 0 ],
                    "source": [ "obj-6", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-node", 0 ],
                    "source": [ "obj-8", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-piezo", 0 ],
                    "order": 0,
                    "source": [ "obj-9", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-pres", 0 ],
                    "order": 1,
                    "source": [ "obj-9", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-tof", 0 ],
                    "order": 2,
                    "source": [ "obj-9", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-12", 0 ],
                    "order": 0,
                    "source": [ "obj-fs-piezo", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-route-data", 0 ],
                    "order": 1,
                    "source": [ "obj-fs-piezo", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-10", 0 ],
                    "order": 0,
                    "source": [ "obj-fs-pres", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-route-data", 0 ],
                    "order": 1,
                    "source": [ "obj-fs-pres", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-7", 0 ],
                    "order": 1,
                    "source": [ "obj-fs-tof", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-route-data", 0 ],
                    "order": 0,
                    "source": [ "obj-fs-tof", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-fs-piezo", 0 ],
                    "source": [ "obj-itoa-piezo", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-fs-pres", 0 ],
                    "source": [ "obj-itoa-pres", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-fs-tof", 0 ],
                    "source": [ "obj-itoa-tof", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-piezo", 0 ],
                    "order": 0,
                    "source": [ "obj-metro", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-pres", 0 ],
                    "order": 1,
                    "source": [ "obj-metro", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-tof", 0 ],
                    "order": 2,
                    "source": [ "obj-metro", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-route-auto", 0 ],
                    "source": [ "obj-node", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-piezo", 0 ],
                    "source": [ "obj-piezo-portmsg", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-pres", 0 ],
                    "source": [ "obj-pres-portmsg", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-scan-msg", 0 ],
                    "source": [ "obj-rescan", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-22", 0 ],
                    "order": 0,
                    "source": [ "obj-route-auto", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-23", 0 ],
                    "order": 0,
                    "source": [ "obj-route-auto", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-34", 0 ],
                    "order": 0,
                    "source": [ "obj-route-auto", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-piezo-portmsg", 0 ],
                    "order": 1,
                    "source": [ "obj-route-auto", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-pres-portmsg", 0 ],
                    "order": 1,
                    "source": [ "obj-route-auto", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-print-done", 0 ],
                    "source": [ "obj-route-auto", 4 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-print-error", 0 ],
                    "source": [ "obj-route-auto", 5 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-print-missing", 0 ],
                    "source": [ "obj-route-auto", 3 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-tof-portmsg", 0 ],
                    "order": 1,
                    "source": [ "obj-route-auto", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-13", 1 ],
                    "source": [ "obj-route-data", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 1 ],
                    "source": [ "obj-route-data", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-15", 1 ],
                    "source": [ "obj-route-data", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-16", 1 ],
                    "source": [ "obj-route-data", 3 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-node", 0 ],
                    "source": [ "obj-scan-msg", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-zl-piezo", 0 ],
                    "source": [ "obj-sel-piezo", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-zl-piezo", 0 ],
                    "source": [ "obj-sel-piezo", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-zl-pres", 0 ],
                    "source": [ "obj-sel-pres", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-zl-pres", 0 ],
                    "source": [ "obj-sel-pres", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-zl-tof", 0 ],
                    "source": [ "obj-sel-tof", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-zl-tof", 0 ],
                    "source": [ "obj-sel-tof", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-sel-piezo", 0 ],
                    "source": [ "obj-serial-piezo", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-sel-pres", 0 ],
                    "source": [ "obj-serial-pres", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-sel-tof", 0 ],
                    "source": [ "obj-serial-tof", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-tof", 0 ],
                    "source": [ "obj-tof-portmsg", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-itoa-piezo", 0 ],
                    "source": [ "obj-zl-piezo", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-itoa-pres", 0 ],
                    "source": [ "obj-zl-pres", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-itoa-tof", 0 ],
                    "source": [ "obj-zl-tof", 0 ]
                }
            }
        ]
    }
}