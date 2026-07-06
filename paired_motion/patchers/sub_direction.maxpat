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
        "rect": [ 59.0, 111.0, 900.0, 560.0 ],
        "boxes": [
            {
                "box": { "id": "obj-30", "maxclass": "comment", "numinlets": 1, "numoutlets": 0, "patching_rect": [ 40.0, 8.0, 780.0, 20.0 ], "text": "sub_direction — vXn/vYn → 方向 (0=無 1=上 2=下 3=左 4=右) + 力度。abs 用物件, expr 只做比較(1/0)與算術", "fontsize": 13.0 }
            },
            {
                "box": { "id": "obj-1", "maxclass": "inlet", "numinlets": 0, "numoutlets": 1, "outlettype": [ "" ], "index": 1, "comment": "vXn (水平 -1..1)", "patching_rect": [ 40.0, 50.0, 30.0, 30.0 ] }
            },
            {
                "box": { "id": "obj-2", "maxclass": "inlet", "numinlets": 0, "numoutlets": 1, "outlettype": [ "" ], "index": 2, "comment": "vYn (垂直 -1..1)", "patching_rect": [ 300.0, 50.0, 30.0, 30.0 ] }
            },
            {
                "box": { "id": "obj-3", "maxclass": "newobj", "numinlets": 2, "numoutlets": 1, "outlettype": [ "list" ], "patching_rect": [ 40.0, 90.0, 60.0, 22.0 ], "text": "pak f f" }
            },
            {
                "box": { "id": "obj-4", "maxclass": "newobj", "numinlets": 1, "numoutlets": 2, "outlettype": [ "float", "float" ], "patching_rect": [ 40.0, 125.0, 80.0, 22.0 ], "text": "unpack f f" }
            },
            {
                "box": { "id": "obj-7", "maxclass": "newobj", "numinlets": 1, "numoutlets": 2, "outlettype": [ "float", "float" ], "patching_rect": [ 40.0, 160.0, 50.0, 22.0 ], "text": "t f f" }
            },
            {
                "box": { "id": "obj-5", "maxclass": "newobj", "numinlets": 1, "numoutlets": 1, "outlettype": [ "float" ], "patching_rect": [ 40.0, 200.0, 50.0, 22.0 ], "text": "abs 0." }
            },
            {
                "box": { "id": "obj-6", "maxclass": "newobj", "numinlets": 1, "numoutlets": 1, "outlettype": [ "float" ], "patching_rect": [ 300.0, 125.0, 50.0, 22.0 ], "text": "abs 0." }
            },
            {
                "box": { "id": "obj-31", "maxclass": "comment", "numinlets": 1, "numoutlets": 0, "patching_rect": [ 40.0, 238.0, 820.0, 20.0 ], "text": "$f1=absX(hot) $f2=absY $f3=vXn $f4=vYn。active=任一軸>0.2; 主導軸+正負號定方向; 極性需現場校正" }
            },
            {
                "box": { "id": "obj-8", "maxclass": "newobj", "numinlets": 4, "numoutlets": 1, "outlettype": [ "" ], "patching_rect": [ 40.0, 270.0, 820.0, 22.0 ], "text": "expr (((($f1 > 0.2) + ($f2 > 0.2)) > 0) * ((($f1 >= $f2) * (3 + ($f3 > 0.))) + ((1 - ($f1 >= $f2)) * (2 - ($f4 > 0.)))))" }
            },
            {
                "box": { "id": "obj-13", "maxclass": "newobj", "numinlets": 2, "numoutlets": 1, "outlettype": [ "" ], "patching_rect": [ 500.0, 330.0, 340.0, 22.0 ], "text": "expr (($f1 >= $f2) * $f1) + ((1 - ($f1 >= $f2)) * $f2)" }
            },
            {
                "box": { "id": "obj-9", "maxclass": "newobj", "numinlets": 1, "numoutlets": 1, "outlettype": [ "" ], "patching_rect": [ 40.0, 330.0, 60.0, 22.0 ], "text": "change" }
            },
            {
                "box": { "id": "obj-10", "maxclass": "newobj", "numinlets": 1, "numoutlets": 0, "patching_rect": [ 40.0, 380.0, 80.0, 22.0 ], "text": "s activeDir" }
            },
            {
                "box": { "id": "obj-11", "maxclass": "number", "numinlets": 1, "numoutlets": 2, "outlettype": [ "", "bang" ], "parameter_enable": 0, "fontsize": 24.0, "patching_rect": [ 140.0, 375.0, 70.0, 36.0 ] }
            },
            {
                "box": { "id": "obj-32", "maxclass": "comment", "numinlets": 1, "numoutlets": 0, "patching_rect": [ 216.0, 385.0, 220.0, 20.0 ], "text": "activeDir (0/1/2/3/4)" }
            },
            {
                "box": { "id": "obj-12", "maxclass": "outlet", "numinlets": 1, "numoutlets": 0, "index": 1, "comment": "activeDir", "patching_rect": [ 40.0, 430.0, 30.0, 30.0 ] }
            },
            {
                "box": { "id": "obj-14", "maxclass": "newobj", "numinlets": 1, "numoutlets": 0, "patching_rect": [ 500.0, 380.0, 70.0, 22.0 ], "text": "s dirMag" }
            },
            {
                "box": { "id": "obj-15", "maxclass": "flonum", "numinlets": 1, "numoutlets": 2, "outlettype": [ "", "bang" ], "parameter_enable": 0, "patching_rect": [ 590.0, 380.0, 60.0, 22.0 ] }
            },
            {
                "box": { "id": "obj-33", "maxclass": "comment", "numinlets": 1, "numoutlets": 0, "patching_rect": [ 656.0, 382.0, 120.0, 20.0 ], "text": "dirMag (0..1)" }
            },
            {
                "box": { "id": "obj-16", "maxclass": "outlet", "numinlets": 1, "numoutlets": 0, "index": 2, "comment": "dirMag", "patching_rect": [ 500.0, 430.0, 30.0, 30.0 ] }
            }
        ],
        "lines": [
            { "patchline": { "source": [ "obj-1", 0 ], "destination": [ "obj-3", 0 ] } },
            { "patchline": { "source": [ "obj-2", 0 ], "destination": [ "obj-3", 1 ] } },
            { "patchline": { "source": [ "obj-3", 0 ], "destination": [ "obj-4", 0 ] } },
            { "patchline": { "source": [ "obj-4", 0 ], "destination": [ "obj-7", 0 ] } },
            { "patchline": { "source": [ "obj-4", 1 ], "destination": [ "obj-8", 3 ] } },
            { "patchline": { "source": [ "obj-4", 1 ], "destination": [ "obj-6", 0 ] } },
            { "patchline": { "source": [ "obj-7", 1 ], "destination": [ "obj-8", 2 ] } },
            { "patchline": { "source": [ "obj-7", 0 ], "destination": [ "obj-5", 0 ] } },
            { "patchline": { "source": [ "obj-5", 0 ], "destination": [ "obj-8", 0 ] } },
            { "patchline": { "source": [ "obj-5", 0 ], "destination": [ "obj-13", 0 ] } },
            { "patchline": { "source": [ "obj-6", 0 ], "destination": [ "obj-8", 1 ] } },
            { "patchline": { "source": [ "obj-6", 0 ], "destination": [ "obj-13", 1 ] } },
            { "patchline": { "source": [ "obj-8", 0 ], "destination": [ "obj-9", 0 ] } },
            { "patchline": { "source": [ "obj-9", 0 ], "destination": [ "obj-10", 0 ] } },
            { "patchline": { "source": [ "obj-9", 0 ], "destination": [ "obj-11", 0 ] } },
            { "patchline": { "source": [ "obj-9", 0 ], "destination": [ "obj-12", 0 ] } },
            { "patchline": { "source": [ "obj-13", 0 ], "destination": [ "obj-14", 0 ] } },
            { "patchline": { "source": [ "obj-13", 0 ], "destination": [ "obj-15", 0 ] } },
            { "patchline": { "source": [ "obj-13", 0 ], "destination": [ "obj-16", 0 ] } }
        ]
    }
}
