{
    "patcher": {
        "fileversion": 1,
        "appversion": {
            "major": 9,
            "minor": 1,
            "revision": 1,
            "architecture": "x64",
            "modernui": 1
        },
        "classnamespace": "box",
        "rect": [ 367.0, 92.0, 879.0, 594.0 ],
        "boxes": [
            {
                "box": {
                    "id": "obj-14",
                    "maxclass": "ezdac~",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "patching_rect": [ 21.0, 470.0, 45.0, 45.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-12",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 21.0, 196.0, 65.0, 23.0 ],
                    "text": "距離感測"
                }
            },
            {
                "box": {
                    "id": "obj-11",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 99.0, 196.0, 97.0, 23.0 ],
                    "text": "握把壓力感測"
                }
            },
            {
                "box": {
                    "id": "obj-10",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 196.0, 196.0, 97.0, 37.0 ],
                    "text": "敲擊感測（目前四顆沒有分別）"
                }
            },
            {
                "box": {
                    "id": "obj-3",
                    "maxclass": "gain~",
                    "multichannelvariant": 0,
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 196.0, 280.0, 22.0, 140.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-2",
                    "maxclass": "gain~",
                    "multichannelvariant": 0,
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 99.0, 280.0, 22.0, 140.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-1",
                    "maxclass": "gain~",
                    "multichannelvariant": 0,
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 21.0, 280.0, 22.0, 140.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-9",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 21.0, 235.0, 48.0, 22.0 ],
                    "text": "sub_tof"
                }
            },
            {
                "box": {
                    "id": "obj-8",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 99.0, 235.0, 81.0, 22.0 ],
                    "text": "sub_pressure"
                }
            },
            {
                "box": {
                    "id": "obj-7",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 196.0, 235.0, 63.0, 22.0 ],
                    "text": "sub_piezo"
                }
            },
            {
                "box": {
                    "bgmode": 0,
                    "border": 0,
                    "clickthrough": 0,
                    "enablehscroll": 0,
                    "enablevscroll": 0,
                    "id": "obj-6",
                    "lockeddragscroll": 0,
                    "lockedsize": 0,
                    "maxclass": "bpatcher",
                    "name": "sub_auto_detect.maxpat",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "offset": [ 0.0, 0.0 ],
                    "patching_rect": [ 20.0, 48.0, 628.0, 135.0 ],
                    "viewvisibility": 1
                }
            },
            {
                "box": {
                    "fontsize": 13.0,
                    "id": "obj-header",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 20.0, 20.0, 628.0, 25.0 ],
                    "text": "PAIRED MOTION (+VIZ): 三組感測器 + ToF 視覺化分支 → 瀏覽器 http://localhost:8080"
                }
            },
            {
                "box": {
                    "id": "obj-viz-comment",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 370.0, 196.0, 280.0, 23.0 ],
                    "text": "視覺化分支 → http://localhost:8080"
                }
            },
            {
                "box": {
                    "id": "obj-viz-rtof",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 370.0, 235.0, 45.0, 22.0 ],
                    "text": "r tof"
                }
            },
            {
                "box": {
                    "id": "obj-viz-start",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 425.0, 235.0, 80.0, 22.0 ],
                    "text": "script start"
                }
            },
            {
                "box": {
                    "id": "obj-viz-stop",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 515.0, 235.0, 80.0, 22.0 ],
                    "text": "script stop"
                }
            },
            {
                "box": {
                    "id": "obj-viz-restart",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 605.0, 235.0, 90.0, 22.0 ],
                    "text": "script restart"
                }
            },
            {
                "box": {
                    "id": "obj-viz-node",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "int" ],
                    "patching_rect": [ 370.0, 275.0, 260.0, 22.0 ],
                    "text": "node.script ../visualization/server.js"
                }
            },
            {
                "box": {
                    "id": "obj-viz-print",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 370.0, 310.0, 80.0, 22.0 ],
                    "text": "print viz"
                }
            },
            {
                "box": {
                    "id": "obj-viz-hint",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 460.0, 310.0, 320.0, 23.0 ],
                    "text": "啟動順序：sub_auto_detect 掃描完 → script start → 開瀏覽器"
                }
            }
        ],
        "lines": [
            {
                "patchline": {
                    "destination": [ "obj-14", 1 ],
                    "order": 0,
                    "source": [ "obj-1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 0 ],
                    "order": 1,
                    "source": [ "obj-1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 1 ],
                    "order": 0,
                    "source": [ "obj-2", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 0 ],
                    "order": 1,
                    "source": [ "obj-2", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 1 ],
                    "order": 0,
                    "source": [ "obj-3", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 0 ],
                    "order": 1,
                    "source": [ "obj-3", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-3", 0 ],
                    "source": [ "obj-7", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-2", 0 ],
                    "source": [ "obj-8", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-1", 0 ],
                    "source": [ "obj-9", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-viz-node", 0 ],
                    "source": [ "obj-viz-rtof", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-viz-node", 0 ],
                    "source": [ "obj-viz-start", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-viz-node", 0 ],
                    "source": [ "obj-viz-stop", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-viz-node", 0 ],
                    "source": [ "obj-viz-restart", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-viz-print", 0 ],
                    "source": [ "obj-viz-node", 0 ]
                }
            }
        ],
        "parameters": {
            "obj-7::obj-105": [ "gain~", "gain~", 0 ],
            "obj-8::obj-54": [ "live.gain~[3]", "live.gain~", 0 ],
            "obj-8::obj-58": [ "live.gain~[4]", "live.gain~", 0 ],
            "obj-9::obj-63::obj-27": [ "live.gain~[2]", "live.gain~", 0 ],
            "parameterbanks": {
                "0": {
                    "index": 0,
                    "name": "",
                    "parameters": [ "-", "-", "-", "-", "-", "-", "-", "-" ],
                    "buttons": [ "-", "-", "-", "-", "-", "-", "-", "-" ]
                }
            },
            "parameter_overrides": {
                "obj-7::obj-105": {
                    "parameter_initial": 100,
                    "parameter_initial_enable": 1
                }
            },
            "inherited_shortname": 1
        },
        "autosave": 0
    }
}