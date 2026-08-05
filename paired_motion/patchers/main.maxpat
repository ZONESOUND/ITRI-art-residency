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
        "rect": [ 34.0, 92.0, 1212.0, 594.0 ],
        "boxes": [
            {
                "box": {
                    "id": "obj-70",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 72.0, 45.0, 359.0, 23.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 859.0, -63.0, 247.0, 23.0 ],
                    "text": "確認按壓手把，Slider 有同步移動。"
                }
            },
            {
                "box": {
                    "bubble": 1,
                    "bubble_bgcolor": [ 1.0, 0.996078431372549, 0.996078431372549, 1.0 ],
                    "bubbleside": 2,
                    "id": "obj-69",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 630.5, 285.0, 150.0, 39.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 806.0, -67.0, 47.0, 39.0 ],
                    "text": "Step 3",
                    "textcolor": [ 0.07450980392156863, 0.07450980392156863, 0.07450980392156863, 1.0 ]
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.6470588235294118, 0.6431372549019608, 0.6431372549019608, 0.0 ],
                    "bubble_bgcolor": [ 0.8156862745098039, 0.8156862745098039, 0.8156862745098039, 1.0 ],
                    "id": "obj-37",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 57.0, 30.0, 359.0, 37.0 ],
                    "presentation": 1,
                    "presentation_linecount": 2,
                    "presentation_rect": [ 415.0, 1.5, 247.0, 37.0 ],
                    "text": "按同動車右下角Reset按鈕，確認移動手把時，畫面中的圓圈同步移動。"
                }
            },
            {
                "box": {
                    "bubble": 1,
                    "bubble_bgcolor": [ 1.0, 0.996078431372549, 0.996078431372549, 1.0 ],
                    "bubbleside": 2,
                    "id": "obj-33",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 615.5, 270.0, 150.0, 39.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 360.0, -0.5, 47.0, 39.0 ],
                    "text": "Step 2",
                    "textcolor": [ 0.07450980392156863, 0.07450980392156863, 0.07450980392156863, 1.0 ]
                }
            },
            {
                "box": {
                    "bubble": 1,
                    "bubble_bgcolor": [ 1.0, 0.996078431372549, 0.996078431372549, 1.0 ],
                    "id": "obj-32",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 600.5, 255.0, 150.0, 24.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 278.0, -8.5, 65.0, 24.0 ],
                    "text": "Step 1",
                    "textcolor": [ 0.07450980392156863, 0.07450980392156863, 0.07450980392156863, 1.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-19",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 739.0, 578.0, 29.5, 22.0 ],
                    "text": "+ 1"
                }
            },
            {
                "box": {
                    "id": "obj-80",
                    "maxclass": "preset",
                    "numinlets": 1,
                    "numoutlets": 5,
                    "outlettype": [ "preset", "int", "preset", "int", "" ],
                    "patching_rect": [ 739.0, 639.0, 100.0, 40.0 ],
                    "preset_data": [
                        {
                            "number": 1,
                            "data": [ 6, "obj-2", "gain~", "list", 120, 10.0, 5, "obj-5", "radiogroup", "int", 0, 6, "obj-1", "gain~", "list", 88, 10.0 ]
                        },
                        {
                            "number": 2,
                            "data": [ 6, "obj-2", "gain~", "list", 120, 10.0, 5, "obj-5", "radiogroup", "int", 1, 6, "obj-1", "gain~", "list", 0, 10.0 ]
                        },
                        {
                            "number": 3,
                            "data": [ 6, "obj-2", "gain~", "list", 120, 10.0, 5, "obj-5", "radiogroup", "int", 1, 6, "obj-1", "gain~", "list", 0, 10.0 ]
                        },
                        {
                            "number": 4,
                            "data": [ 6, "obj-2", "gain~", "list", 120, 10.0, 5, "obj-5", "radiogroup", "int", 1, 6, "obj-1", "gain~", "list", 0, 10.0 ]
                        },
                        {
                            "number": 5,
                            "data": [ 6, "obj-2", "gain~", "list", 120, 10.0, 5, "obj-5", "radiogroup", "int", 2, 6, "obj-1", "gain~", "list", 0, 10.0 ]
                        }
                    ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-73",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 762.5, 536.0, 87.0, 25.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 947.0, 274.0, 87.0, 25.0 ],
                    "text": "第四幕",
                    "textcolor": [ 0.803922, 0.898039, 0.909804, 1.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-74",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 762.0, 503.0, 88.0, 25.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 947.0, 241.0, 88.0, 25.0 ],
                    "text": "第三幕",
                    "textcolor": [ 0.803922, 0.898039, 0.909804, 1.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-75",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 762.0, 470.0, 88.0, 25.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 947.0, 208.0, 88.0, 25.0 ],
                    "text": "第二幕",
                    "textcolor": [ 0.803922, 0.898039, 0.909804, 1.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-76",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 762.0, 437.0, 87.0, 25.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 947.0, 175.0, 87.0, 25.0 ],
                    "text": "第一幕",
                    "textcolor": [ 0.803922, 0.898039, 0.909804, 1.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-77",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 739.0, 606.0, 53.0, 23.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-78",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 762.0, 407.0, 87.0, 25.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 947.0, 145.0, 87.0, 25.0 ],
                    "text": "待機狀態測試",
                    "textcolor": [ 0.803922, 0.898039, 0.909804, 1.0 ]
                }
            },
            {
                "box": {
                    "disabled": [ 0, 0, 0, 0, 0 ],
                    "id": "obj-79",
                    "itemtype": 0,
                    "maxclass": "radiogroup",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "offset": 32,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 739.0, 407.0, 110.0, 162.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 924.0, 145.0, 110.0, 162.0 ],
                    "size": 5,
                    "value": 0
                }
            },
            {
                "box": {
                    "id": "obj-67",
                    "items": [ "無", ",", "左手", ",", "右手", ",", "雙手" ],
                    "maxclass": "umenu",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "int", "", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 345.0, 494.0, 83.0, 22.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 770.0, -20.0, 83.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-60",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 345.0, 453.0, 83.0, 22.0 ],
                    "text": "r activeVoices"
                }
            },
            {
                "box": {
                    "id": "obj-54",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1120.0, 79.0, 56.0, 20.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 844.0, 9.0, 56.0, 20.0 ],
                    "text": "Hand 2"
                }
            },
            {
                "box": {
                    "id": "obj-38",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1040.0, 79.0, 56.0, 20.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 770.0, 9.0, 56.0, 20.0 ],
                    "text": "Hand 1"
                }
            },
            {
                "box": {
                    "format": 6,
                    "id": "obj-35",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1098.0, 261.0, 50.0, 22.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 844.0, 296.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.57636836783545, 0.576368229540612, 0.576368265679262, 1.0 ],
                    "elementcolor": [ 0.250980392156863, 0.203921568627451, 0.937254901960784, 1.0 ],
                    "floatoutput": 1,
                    "id": "obj-36",
                    "knobcolor": [ 1.0, 0.4, 0.3, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1098.0, 106.0, 20.0, 140.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 844.0, 37.0, 50.0, 244.0 ],
                    "saved_attribute_attributes": {
                        "bgcolor": {
                            "expression": "themecolor.live_dial_needle_zombie"
                        },
                        "elementcolor": {
                            "expression": "themecolor.live_midi_assignment"
                        },
                        "knobcolor": {
                            "expression": "themecolor.live_active_automation"
                        }
                    },
                    "size": 1.0
                }
            },
            {
                "box": {
                    "format": 6,
                    "id": "obj-34",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1027.0, 261.0, 50.0, 22.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 773.0, 296.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.57636836783545, 0.576368229540612, 0.576368265679262, 1.0 ],
                    "elementcolor": [ 0.250980392156863, 0.203921568627451, 0.937254901960784, 1.0 ],
                    "floatoutput": 1,
                    "id": "obj-31",
                    "knobcolor": [ 1.0, 0.4, 0.3, 1.0 ],
                    "maxclass": "slider",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1027.0, 106.0, 20.0, 140.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 773.0, 37.0, 50.0, 244.0 ],
                    "saved_attribute_attributes": {
                        "bgcolor": {
                            "expression": "themecolor.live_dial_needle_zombie"
                        },
                        "elementcolor": {
                            "expression": "themecolor.live_midi_assignment"
                        },
                        "knobcolor": {
                            "expression": "themecolor.live_active_automation"
                        }
                    },
                    "size": 1.0
                }
            },
            {
                "box": {
                    "id": "obj-29",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 1027.0, 27.0, 49.0, 22.0 ],
                    "text": "r hand1"
                }
            },
            {
                "box": {
                    "id": "obj-30",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 1098.0, 27.0, 49.0, 22.0 ],
                    "text": "r hand2"
                }
            },
            {
                "box": {
                    "id": "obj-28",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 790.0, 77.5, 150.0, 23.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 663.0, 15.5, 81.0, 23.0 ],
                    "text": "ToF 距離感測"
                }
            },
            {
                "box": {
                    "id": "obj-25",
                    "maxclass": "pictslider",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "int", "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 693.0, 106.0, 251.0, 177.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 345.0, 37.0, 399.0, 282.0 ],
                    "rightvalue": 360,
                    "topvalue": 320
                }
            },
            {
                "box": {
                    "id": "obj-22",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "int", "int" ],
                    "patching_rect": [ 693.0, 69.0, 67.0, 22.0 ],
                    "text": "unpack 0 0"
                }
            },
            {
                "box": {
                    "id": "obj-21",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 693.0, 36.0, 82.0, 22.0 ],
                    "text": "r tof_visualize"
                }
            },
            {
                "box": {
                    "id": "obj-66",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 456.0, 420.0, 259.0, 23.0 ],
                    "text": "activeVoices: 0=無 1=左 2=右 3=雙手合奏"
                }
            },
            {
                "box": {
                    "id": "obj-65",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 456.0, 387.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-61",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "" ],
                    "patching_rect": [ 345.0, 342.0, 130.0, 22.0 ],
                    "text": "sub_voice_gate"
                }
            },
            {
                "box": {
                    "id": "obj-62",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 345.0, 387.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-63",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 401.0, 387.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-64",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 312.0, 421.0, 139.0, 20.0 ],
                    "text": "voice1 / voice2 (0/1)"
                }
            },
            {
                "box": {
                    "fontface": 0,
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-23",
                    "maxclass": "jit.fpsgui",
                    "mode": 3,
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 1599.0, 276.0, 80.0, 35.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-24",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1677.0, 151.0, 150.0, 20.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-26",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1499.0, 226.0, 54.0, 22.0 ],
                    "text": "dict.print"
                }
            },
            {
                "box": {
                    "bubble": 1,
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-39",
                    "linecount": 3,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1729.0, 26.0, 262.0, 54.0 ],
                    "text": "The list of available sources can be retrieved as a dictionary or as messages to populate a umenu."
                }
            },
            {
                "box": {
                    "id": "obj-40",
                    "maxclass": "jit.pwindow",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "jit_matrix", "" ],
                    "patching_rect": [ 1429.0, 276.0, 160.0, 120.0 ],
                    "sync": 1
                }
            },
            {
                "box": {
                    "id": "obj-41",
                    "maxclass": "meter~",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 1359.0, 407.0, 160.0, 20.0 ]
                }
            },
            {
                "box": {
                    "attr": "tally_onprogram",
                    "id": "obj-42",
                    "lock": 1,
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1704.0, 289.0, 130.0, 22.0 ]
                }
            },
            {
                "box": {
                    "attr": "tally_onpreview",
                    "id": "obj-43",
                    "lock": 1,
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1704.0, 260.0, 130.0, 22.0 ]
                }
            },
            {
                "box": {
                    "hidden": 1,
                    "id": "obj-44",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 1619.0, 16.0, 58.0, 22.0 ],
                    "text": "loadbang"
                }
            },
            {
                "box": {
                    "id": "obj-45",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 1619.0, 46.0, 106.0, 22.0 ],
                    "text": "getsourcelistmenu"
                }
            },
            {
                "box": {
                    "id": "obj-46",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 1529.0, 46.0, 76.0, 22.0 ],
                    "text": "getsourcelist"
                }
            },
            {
                "box": {
                    "id": "obj-47",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "" ],
                    "patching_rect": [ 1499.0, 196.0, 174.0, 22.0 ],
                    "text": "route sourcelist sourcelistmenu"
                }
            },
            {
                "box": {
                    "id": "obj-48",
                    "items": "<empty>",
                    "maxclass": "umenu",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "int", "", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1579.0, 226.0, 200.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-49",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "multichannelsignal", "jit_matrix", "" ],
                    "patching_rect": [ 1359.0, 106.0, 96.0, 22.0 ],
                    "text": "jit.ndi.receive~ 2"
                }
            },
            {
                "box": {
                    "hidden": 1,
                    "id": "obj-50",
                    "linecount": 3,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 1879.0, 151.0, 110.0, 49.0 ],
                    "text": ";\rmax launchbrowser $1"
                }
            },
            {
                "box": {
                    "hidden": 1,
                    "id": "obj-51",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 1879.0, 114.0, 95.0, 22.0 ],
                    "text": "route runtimeurl"
                }
            },
            {
                "box": {
                    "border": 0,
                    "filename": "helpargs.js",
                    "id": "obj-52",
                    "ignoreclick": 1,
                    "jsarguments": [ "jit.ndi.receive~" ],
                    "maxclass": "jsui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1459.0, 106.0, 204.26300048828125, 69.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-53",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1415.0, 26.0, 104.0, 20.0 ],
                    "style": "helpfile_label",
                    "text": "Toggle on qmetro"
                }
            },
            {
                "box": {
                    "id": "obj-56",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1809.0, 226.0, 126.0, 20.0 ],
                    "style": "helpfile_label",
                    "text": "Select an NDI source"
                }
            },
            {
                "box": {
                    "id": "obj-55",
                    "maxclass": "toggle",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1359.0, 26.0, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-57",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 1359.0, 66.0, 81.0, 22.0 ],
                    "text": "qmetro 30 hz"
                }
            },
            {
                "box": {
                    "id": "obj-17",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 42.0, 15.0, 359.0, 23.0 ],
                    "presentation": 1,
                    "presentation_linecount": 2,
                    "presentation_rect": [ 17.5, -15.0, 272.0, 37.0 ],
                    "text": "如果無法讀取到裝置，可先點選 close serial 後重新 RESCAN"
                }
            },
            {
                "box": {
                    "id": "obj-16",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 14.5, 371.0, 62.0, 23.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 47.0, 232.0, 63.0, 23.0 ],
                    "text": "移動手把"
                }
            },
            {
                "box": {
                    "id": "obj-14",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 112.0, 371.0, 62.0, 23.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 162.0, 232.0, 63.0, 23.0 ],
                    "text": "握力感測"
                }
            },
            {
                "box": {
                    "disabled": [ 0, 0, 0 ],
                    "id": "obj-5",
                    "itemtype": 0,
                    "maxclass": "radiogroup",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 93.0, 331.0, 18.0, 50.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 162.0, 173.0, 18.0, 50.0 ],
                    "size": 3,
                    "value": 0
                }
            },
            {
                "box": {
                    "id": "obj-18",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 190.0, 657.0, 72.0, 22.0 ],
                    "text": "startwindow"
                }
            },
            {
                "box": {
                    "id": "obj-15",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 190.0, 629.0, 58.0, 22.0 ],
                    "text": "loadbang"
                }
            },
            {
                "box": {
                    "id": "obj-13",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 629.0, -27.0, 55.0, 22.0 ],
                    "text": "del 4000"
                }
            },
            {
                "box": {
                    "id": "obj-12",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 20.0, -35.0, 55.0, 22.0 ],
                    "text": "del 3000"
                }
            },
            {
                "box": {
                    "id": "obj-11",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 20.0, -67.0, 58.0, 22.0 ],
                    "text": "loadbang"
                }
            },
            {
                "box": {
                    "id": "obj-10",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 214.0, 561.0, 48.0, 23.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 291.0, 232.0, 46.0, 23.0 ],
                    "text": "敲擊"
                }
            },
            {
                "box": {
                    "id": "obj-4",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "patching_rect": [ 28.0, 696.0, 35.0, 22.0 ],
                    "text": "dac~"
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
                    "parameter_enable": 1,
                    "patching_rect": [ 190.0, 441.0, 22.0, 140.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 267.0, 173.0, 22.0, 140.0 ],
                    "saved_attribute_attributes": {
                        "valueof": {
                            "parameter_initial": [ 88 ],
                            "parameter_initial_enable": 1,
                            "parameter_longname": "gain~[1]",
                            "parameter_mmax": 157.0,
                            "parameter_modmode": 3,
                            "parameter_shortname": "gain~[1]",
                            "parameter_type": 0
                        }
                    },
                    "varname": "gain~"
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
                    "parameter_enable": 1,
                    "patching_rect": [ 93.0, 441.0, 22.0, 140.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 133.0, 173.0, 22.0, 140.0 ],
                    "saved_attribute_attributes": {
                        "valueof": {
                            "parameter_initial": [ 120 ],
                            "parameter_initial_enable": 1,
                            "parameter_longname": "gain~[2]",
                            "parameter_mmax": 157.0,
                            "parameter_modmode": 3,
                            "parameter_shortname": "gain~[2]",
                            "parameter_type": 0
                        }
                    },
                    "varname": "gain~[1]"
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
                    "parameter_enable": 1,
                    "patching_rect": [ 28.0, 441.0, 22.0, 140.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 21.0, 173.0, 22.0, 140.0 ],
                    "saved_attribute_attributes": {
                        "valueof": {
                            "parameter_initial": [ 88 ],
                            "parameter_initial_enable": 1,
                            "parameter_longname": "gain~[3]",
                            "parameter_mmax": 157.0,
                            "parameter_modmode": 3,
                            "parameter_shortname": "gain~[3]",
                            "parameter_type": 0
                        }
                    },
                    "varname": "gain~[2]"
                }
            },
            {
                "box": {
                    "id": "obj-9",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 28.0, 396.0, 48.0, 22.0 ],
                    "text": "sub_tof",
                    "varname": "sub_tof"
                }
            },
            {
                "box": {
                    "id": "obj-8",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 93.0, 396.0, 81.0, 22.0 ],
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
                    "patching_rect": [ 190.0, 396.0, 63.0, 22.0 ],
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
                    "patching_rect": [ 20.0, 48.0, 628.0, 232.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 18.0, 26.0, 271.3333414196968, 135.33333736658096 ],
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
                    "patching_rect": [ 20.0, 286.0, 537.0, 25.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 17.0, -42.0, 537.0, 25.0 ],
                    "text": "PAIRED MOTION: 接收與控制同動車上的三組感測器（距離感測、壓力感測、敲擊感測）"
                }
            },
            {
                "box": {
                    "angle": 270.0,
                    "bgcolor": [ 0.609795304305787, 0.805124657532386, 0.576461028292266, 1.0 ],
                    "id": "obj-20",
                    "maxclass": "panel",
                    "mode": 0,
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1080.0, 349.0, 128.0, 128.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 915.0, 135.0, 128.0, 181.0 ],
                    "proportion": 0.39,
                    "saved_attribute_attributes": {
                        "bgfillcolor": {
                            "expression": "themecolor.lesson_inprogress"
                        }
                    }
                }
            },
            {
                "box": {
                    "angle": 270.0,
                    "bgcolor": [ 0.599589840206136, 0.599589696824869, 0.599589734292685, 1.0 ],
                    "id": "obj-68",
                    "maxclass": "panel",
                    "mode": 0,
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1095.0, 364.0, 128.0, 128.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 18.0, -13.0, 271.0, 33.0 ],
                    "proportion": 0.39,
                    "saved_attribute_attributes": {
                        "bgfillcolor": {
                            "expression": "themecolor.lesson_todo"
                        }
                    }
                }
            },
            {
                "box": {
                    "angle": 270.0,
                    "bgcolor": [ 0.599589840206136, 0.599589696824869, 0.599589734292685, 1.0 ],
                    "id": "obj-71",
                    "maxclass": "panel",
                    "mode": 0,
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1110.0, 379.0, 128.0, 128.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 415.0, 2.5, 247.0, 33.0 ],
                    "proportion": 0.39,
                    "saved_attribute_attributes": {
                        "bgfillcolor": {
                            "expression": "themecolor.lesson_todo"
                        }
                    }
                }
            },
            {
                "box": {
                    "angle": 270.0,
                    "bgcolor": [ 0.599589840206136, 0.599589696824869, 0.599589734292685, 1.0 ],
                    "id": "obj-72",
                    "maxclass": "panel",
                    "mode": 0,
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1125.0, 394.0, 128.0, 128.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 859.0, -64.0, 197.0, 21.0 ],
                    "proportion": 0.39,
                    "saved_attribute_attributes": {
                        "bgfillcolor": {
                            "expression": "themecolor.lesson_todo"
                        }
                    }
                }
            },
            {
                "box": {
                    "background": 1,
                    "bgcolor": [ 1.0, 0.788235, 0.470588, 1.0 ],
                    "fontface": 1,
                    "hint": "",
                    "id": "obj-58",
                    "ignoreclick": 1,
                    "legacytextcolor": 1,
                    "maxclass": "textbutton",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1789.0, 226.0, 20.0, 20.0 ],
                    "rounded": 60.0,
                    "text": "1",
                    "textcolor": [ 0.34902, 0.34902, 0.34902, 1.0 ]
                }
            },
            {
                "box": {
                    "background": 1,
                    "bgcolor": [ 1.0, 0.788235, 0.470588, 1.0 ],
                    "fontface": 1,
                    "hint": "",
                    "id": "obj-59",
                    "ignoreclick": 1,
                    "legacytextcolor": 1,
                    "maxclass": "textbutton",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1395.0, 26.0, 20.0, 20.0 ],
                    "rounded": 60.0,
                    "text": "2",
                    "textcolor": [ 0.34902, 0.34902, 0.34902, 1.0 ]
                }
            }
        ],
        "lines": [
            {
                "patchline": {
                    "destination": [ "obj-4", 1 ],
                    "order": 0,
                    "source": [ "obj-1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 0 ],
                    "order": 1,
                    "source": [ "obj-1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-12", 0 ],
                    "order": 1,
                    "source": [ "obj-11", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-13", 0 ],
                    "order": 0,
                    "source": [ "obj-11", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-6", 0 ],
                    "source": [ "obj-12", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-6", 1 ],
                    "source": [ "obj-13", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-18", 0 ],
                    "source": [ "obj-15", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 0 ],
                    "source": [ "obj-18", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-77", 0 ],
                    "source": [ "obj-19", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 1 ],
                    "order": 0,
                    "source": [ "obj-2", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 0 ],
                    "order": 1,
                    "source": [ "obj-2", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-22", 0 ],
                    "source": [ "obj-21", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-25", 1 ],
                    "source": [ "obj-22", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-25", 0 ],
                    "source": [ "obj-22", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-31", 0 ],
                    "source": [ "obj-29", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 1 ],
                    "order": 0,
                    "source": [ "obj-3", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 0 ],
                    "order": 1,
                    "source": [ "obj-3", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-36", 0 ],
                    "source": [ "obj-30", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-34", 0 ],
                    "source": [ "obj-31", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-35", 0 ],
                    "source": [ "obj-36", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "hidden": 1,
                    "midpoints": [ 1713.5, 312.0, 1690.0, 312.0, 1690.0, 258.0, 1345.0, 258.0, 1345.0, 102.0, 1368.5, 102.0 ],
                    "source": [ "obj-42", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "hidden": 1,
                    "midpoints": [ 1713.5, 285.0, 1690.0, 285.0, 1690.0, 258.0, 1345.0, 258.0, 1345.0, 102.0, 1368.5, 102.0 ],
                    "source": [ "obj-43", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-45", 0 ],
                    "hidden": 1,
                    "source": [ "obj-44", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "midpoints": [ 1628.5, 97.0, 1368.5, 97.0 ],
                    "source": [ "obj-45", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "midpoints": [ 1538.5, 97.0, 1368.5, 97.0 ],
                    "source": [ "obj-46", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-26", 0 ],
                    "source": [ "obj-47", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-48", 0 ],
                    "source": [ "obj-47", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-51", 0 ],
                    "hidden": 1,
                    "midpoints": [ 1663.5, 228.0, 1865.203125, 228.0, 1865.203125, 104.0, 1888.5, 104.0 ],
                    "source": [ "obj-47", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "midpoints": [ 1679.0, 256.0, 1784.0, 256.0, 1784.0, 97.0, 1368.5, 97.0 ],
                    "source": [ "obj-48", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-23", 0 ],
                    "midpoints": [ 1407.0, 260.0, 1608.5, 260.0 ],
                    "order": 0,
                    "source": [ "obj-49", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-40", 0 ],
                    "midpoints": [ 1407.0, 259.0, 1438.5, 259.0 ],
                    "order": 1,
                    "source": [ "obj-49", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-41", 0 ],
                    "midpoints": [ 1368.5, 129.0, 1368.5, 129.0 ],
                    "source": [ "obj-49", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-47", 0 ],
                    "midpoints": [ 1445.5, 185.0, 1508.5, 185.0 ],
                    "source": [ "obj-49", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-8", 0 ],
                    "source": [ "obj-5", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-50", 0 ],
                    "hidden": 1,
                    "source": [ "obj-51", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-57", 0 ],
                    "source": [ "obj-55", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "source": [ "obj-57", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-67", 0 ],
                    "source": [ "obj-60", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-62", 0 ],
                    "source": [ "obj-61", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-63", 0 ],
                    "source": [ "obj-61", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-65", 0 ],
                    "source": [ "obj-61", 2 ]
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
                    "destination": [ "obj-80", 0 ],
                    "source": [ "obj-77", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-19", 0 ],
                    "source": [ "obj-79", 0 ]
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
                    "order": 2,
                    "source": [ "obj-80", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-2", 0 ],
                    "order": 0,
                    "source": [ "obj-80", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-5", 0 ],
                    "order": 1,
                    "source": [ "obj-80", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-79", 0 ],
                    "midpoints": [ 789.0, 690.0, 726.0, 690.0, 726.0, 402.0, 748.5, 402.0 ],
                    "source": [ "obj-80", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-1", 0 ],
                    "source": [ "obj-9", 0 ]
                }
            }
        ],
        "parameters": {
            "obj-1": [ "gain~[3]", "gain~[3]", 0 ],
            "obj-2": [ "gain~[2]", "gain~[2]", 0 ],
            "obj-3": [ "gain~[1]", "gain~[1]", 0 ],
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
        "autosave": 0,
        "oscreceiveudpport": 0
    }
}