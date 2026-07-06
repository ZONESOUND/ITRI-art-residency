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
        "rect": [ 34.0, 92.0, 1498.0, 941.0 ],
        "boxes": [
            {
                "box": {
                    "id": "obj-66",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 526.0, 664.5, 340.0, 23.0 ],
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
                    "patching_rect": [ 474.0, 665.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-61",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 3,
                    "outlettype": [ "", "", "" ],
                    "patching_rect": [ 339.0, 620.0, 130.0, 22.0 ],
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
                    "patching_rect": [ 339.0, 665.0, 50.0, 22.0 ]
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
                    "patching_rect": [ 409.0, 665.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-64",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 339.0, 697.0, 200.0, 20.0 ],
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
                    "patching_rect": [ 1007.0, 342.0, 80.0, 35.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-24",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1085.0, 217.0, 150.0, 20.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-26",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 907.0, 292.0, 54.0, 22.0 ],
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
                    "patching_rect": [ 1137.0, 92.0, 262.0, 54.0 ],
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
                    "patching_rect": [ 837.0, 342.0, 160.0, 120.0 ],
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
                    "patching_rect": [ 767.0, 473.0, 160.0, 20.0 ]
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
                    "patching_rect": [ 1112.0, 355.0, 130.0, 22.0 ]
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
                    "patching_rect": [ 1112.0, 326.0, 130.0, 22.0 ]
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
                    "patching_rect": [ 1027.0, 82.0, 58.0, 22.0 ],
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
                    "patching_rect": [ 1027.0, 112.0, 106.0, 22.0 ],
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
                    "patching_rect": [ 937.0, 112.0, 76.0, 22.0 ],
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
                    "patching_rect": [ 907.0, 262.0, 174.0, 22.0 ],
                    "text": "route sourcelist sourcelistmenu"
                }
            },
            {
                "box": {
                    "id": "obj-48",
                    "items": "IPHONE 9B3A (HX Camera)",
                    "maxclass": "umenu",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "int", "", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 987.0, 292.0, 200.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-49",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "multichannelsignal", "jit_matrix", "" ],
                    "patching_rect": [ 767.0, 172.0, 96.0, 22.0 ],
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
                    "patching_rect": [ 1287.0, 217.0, 110.0, 49.0 ],
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
                    "patching_rect": [ 1287.0, 180.0, 95.0, 22.0 ],
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
                    "patching_rect": [ 867.0, 172.0, 204.26300048828125, 69.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-53",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 823.0, 92.0, 104.0, 20.0 ],
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
                    "patching_rect": [ 1217.0, 292.0, 126.0, 20.0 ],
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
                    "patching_rect": [ 767.0, 92.0, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-57",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 767.0, 132.0, 81.0, 22.0 ],
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
                    "presentation_rect": [ 16.333337873220444, -30.99999976158142, 272.0, 37.0 ],
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
                    "presentation_rect": [ 46.0, 213.16667127609253, 63.0, 23.0 ],
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
                    "presentation_rect": [ 161.0, 213.16667127609253, 63.0, 23.0 ],
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
                    "presentation_rect": [ 161.0, 154.66667127609253, 18.0, 50.0 ],
                    "size": 3,
                    "value": 1
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
                    "presentation_rect": [ 290.0, 213.16667127609253, 46.0, 23.0 ],
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
                    "presentation_rect": [ 266.00000858306885, 154.66667127609253, 22.0, 140.0 ],
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
                    "presentation_rect": [ 132.0, 154.66667127609253, 22.0, 140.0 ],
                    "saved_attribute_attributes": {
                        "valueof": {
                            "parameter_initial": [ 88 ],
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
                    "presentation_rect": [ 20.000000596046448, 154.66667127609253, 22.0, 140.0 ],
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
                    "presentation_rect": [ 16.66666716337204, 8.000000238418579, 271.3333414196968, 135.33333736658096 ],
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
                    "presentation_rect": [ 16.333337873220444, -60.0, 537.0, 25.0 ],
                    "text": "PAIRED MOTION: 接收與控制同動車上的三組感測器（距離感測、壓力感測、敲擊感測）"
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
                    "patching_rect": [ 1197.0, 292.0, 20.0, 20.0 ],
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
                    "patching_rect": [ 803.0, 92.0, 20.0, 20.0 ],
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
                    "destination": [ "obj-49", 0 ],
                    "hidden": 1,
                    "midpoints": [ 1121.5, 378.0, 1098.0, 378.0, 1098.0, 324.0, 753.0, 324.0, 753.0, 168.0, 776.5, 168.0 ],
                    "source": [ "obj-42", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "hidden": 1,
                    "midpoints": [ 1121.5, 351.0, 1098.0, 351.0, 1098.0, 324.0, 753.0, 324.0, 753.0, 168.0, 776.5, 168.0 ],
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
                    "midpoints": [ 1036.5, 163.0, 776.5, 163.0 ],
                    "source": [ "obj-45", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "midpoints": [ 946.5, 163.0, 776.5, 163.0 ],
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
                    "midpoints": [ 1071.5, 294.0, 1273.203125, 294.0, 1273.203125, 170.0, 1296.5, 170.0 ],
                    "source": [ "obj-47", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-49", 0 ],
                    "midpoints": [ 1087.0, 322.0, 1192.0, 322.0, 1192.0, 163.0, 776.5, 163.0 ],
                    "source": [ "obj-48", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-23", 0 ],
                    "midpoints": [ 815.0, 326.0, 1016.5, 326.0 ],
                    "order": 0,
                    "source": [ "obj-49", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-40", 0 ],
                    "midpoints": [ 815.0, 325.0, 846.5, 325.0 ],
                    "order": 1,
                    "source": [ "obj-49", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-41", 0 ],
                    "midpoints": [ 776.5, 195.0, 776.5, 195.0 ],
                    "source": [ "obj-49", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-47", 0 ],
                    "midpoints": [ 853.5, 251.0, 916.5, 251.0 ],
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
                    "destination": [ "obj-2", 0 ],
                    "source": [ "obj-8", 0 ]
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
        "autosave": 0
    }
}