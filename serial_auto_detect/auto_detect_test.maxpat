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
        "rect": [ 60.0, 92.0, 783.0, 714.0 ],
        "boxes": [
            {
                "box": {
                    "id": "obj-19",
                    "linecount": 2,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 480.5, 132.0, 99.0, 35.0 ],
                    "text": "usbmodem1423301"
                }
            },
            {
                "box": {
                    "id": "obj-17",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 352.0, 583.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-16",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 250.0, 583.0, 50.0, 22.0 ],
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
                    "patching_rect": [ 160.0, 583.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-14",
                    "linecount": 2,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 74.0, 583.0, 50.0, 35.0 ],
                    "presentation_linecount": 2,
                    "text": "0. 0. 277 5"
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
                    "patching_rect": [ 1.0, 583.0, 50.0, 35.0 ],
                    "text": "3 0 0 0 0. 0."
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
                    "patching_rect": [ 659.0, 293.0, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-9",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 672.0, 440.0, 37.0, 22.0 ],
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
                    "patching_rect": [ 10.0, 10.0, 800.0, 21.0 ],
                    "text": "AUTO-DETECT TEST PATCH — auto_detect.js autostart on load. Press RESCAN to re-trigger after replug."
                }
            },
            {
                "box": {
                    "id": "obj-2",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 10.0, 50.0, 250.0, 20.0 ],
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
                    "patching_rect": [ 10.0, 80.0, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-rescan-label",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 38.0, 82.0, 60.0, 20.0 ],
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
                    "patching_rect": [ 100.0, 80.0, 50.0, 22.0 ],
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
                    "patching_rect": [ 10.0, 120.0, 360.0, 22.0 ],
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
                    "patching_rect": [ 666.0, 340.0, 70.0, 22.0 ],
                    "text": "metro 20"
                }
            },
            {
                "box": {
                    "id": "obj-metro-trig",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "bang", "bang", "bang" ],
                    "patching_rect": [ 666.0, 370.0, 70.0, 22.0 ],
                    "text": "t b b b"
                }
            },
            {
                "box": {
                    "id": "obj-route-auto",
                    "maxclass": "newobj",
                    "numinlets": 7,
                    "numoutlets": 7,
                    "outlettype": [ "", "", "", "", "", "", "" ],
                    "patching_rect": [ 10.0, 160.0, 420.0, 22.0 ],
                    "text": "route tof pressure piezo missing done error"
                }
            },
            {
                "box": {
                    "id": "obj-print-missing",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 660.0, 200.0, 130.0, 22.0 ],
                    "text": "print MISSING"
                }
            },
            {
                "box": {
                    "id": "obj-print-done",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 660.0, 230.0, 130.0, 22.0 ],
                    "text": "print DONE"
                }
            },
            {
                "box": {
                    "id": "obj-print-error",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 660.0, 260.0, 130.0, 22.0 ],
                    "text": "print ERROR"
                }
            },
            {
                "box": {
                    "id": "obj-3",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 10.0, 240.0, 300.0, 20.0 ],
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
                    "patching_rect": [ 10.0, 270.0, 160.0, 22.0 ],
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
                    "patching_rect": [ 220.0, 270.0, 160.0, 22.0 ],
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
                    "patching_rect": [ 430.0, 270.0, 160.0, 22.0 ],
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
                    "patching_rect": [ 10.0, 310.0, 200.0, 22.0 ],
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
                    "patching_rect": [ 220.0, 310.0, 200.0, 22.0 ],
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
                    "patching_rect": [ 430.0, 310.0, 200.0, 22.0 ],
                    "text": "serial c 115200 8 1"
                }
            },
            {
                "box": {
                    "id": "obj-4",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 10.0, 340.0, 400.0, 20.0 ],
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
                    "patching_rect": [ 10.0, 370.0, 80.0, 22.0 ],
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
                    "patching_rect": [ 220.0, 370.0, 80.0, 22.0 ],
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
                    "patching_rect": [ 430.0, 370.0, 80.0, 22.0 ],
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
                    "patching_rect": [ 10.0, 400.0, 100.0, 22.0 ],
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
                    "patching_rect": [ 220.0, 400.0, 100.0, 22.0 ],
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
                    "patching_rect": [ 430.0, 400.0, 100.0, 22.0 ],
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
                    "patching_rect": [ 10.0, 430.0, 60.0, 22.0 ],
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
                    "patching_rect": [ 220.0, 430.0, 60.0, 22.0 ],
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
                    "patching_rect": [ 430.0, 430.0, 60.0, 22.0 ],
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
                    "patching_rect": [ 10.0, 460.0, 100.0, 22.0 ],
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
                    "patching_rect": [ 220.0, 460.0, 100.0, 22.0 ],
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
                    "patching_rect": [ 430.0, 460.0, 100.0, 22.0 ],
                    "text": "fromsymbol"
                }
            },
            {
                "box": {
                    "id": "obj-5",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 10.0, 500.0, 600.0, 20.0 ],
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
                    "patching_rect": [ 10.0, 530.0, 380.0, 22.0 ],
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
                    "patching_rect": [ 10.0, 640.0, 627.0, 87.0 ],
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
                    "destination": [ "obj-route-data", 0 ],
                    "source": [ "obj-fs-piezo", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-route-data", 0 ],
                    "source": [ "obj-fs-pres", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-route-data", 0 ],
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
                    "destination": [ "obj-metro-trig", 0 ],
                    "source": [ "obj-metro", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-piezo", 0 ],
                    "source": [ "obj-metro-trig", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-pres", 0 ],
                    "source": [ "obj-metro-trig", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-serial-tof", 0 ],
                    "source": [ "obj-metro-trig", 2 ]
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
                    "destination": [ "obj-19", 1 ],
                    "order": 0,
                    "source": [ "obj-route-auto", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-piezo-portmsg", 0 ],
                    "source": [ "obj-route-auto", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-pres-portmsg", 0 ],
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
                    "destination": [ "obj-17", 1 ],
                    "source": [ "obj-route-data", 4 ]
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
        ],
        "autosave": 0
    }
}