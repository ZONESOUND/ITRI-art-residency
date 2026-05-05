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
        "rect": [ 134.0, 92.0, 1061.0, 714.0 ],
        "boxes": [
            {
                "box": {
                    "id": "obj-5",
                    "linecount": 2,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 18.0, 325.0, 105.5, 35.0 ],
                    "text": "/tof 37 181 36 180 -0. -0."
                }
            },
            {
                "box": {
                    "id": "obj-17",
                    "maxclass": "button",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 241.0, 462.0, 20.0, 20.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 261.0, 195.0, 33.0, 33.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-91",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 95.0, 987.0, 29.5, 22.0 ],
                    "text": "120"
                }
            },
            {
                "box": {
                    "id": "obj-85",
                    "interpinlet": 1,
                    "maxclass": "gain~",
                    "multichannelvariant": 0,
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 209.0, 984.0, 21.0, 81.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-75",
                    "linecount": 7,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 373.0, 966.0, 409.0, 104.0 ],
                    "presentation": 1,
                    "presentation_linecount": 7,
                    "presentation_rect": [ 7.0, 130.0, 294.0, 104.0 ],
                    "text": "操作說明：\n1. 瞬間音量增減會觸發一個合成的Tiny Sound\n2. 平均音量超過一定程度會切換Tiny Sound的音色\n3. 原始的聲音輸入會隨機通過一個Multi-Delay效果\n\n*** 最左邊音量推桿要推出來才有聲音\n*** 按open可選擇音訊輸入/輸出裝置"
                }
            },
            {
                "box": {
                    "id": "obj-95",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 179.0, 804.0, 29.5, 22.0 ],
                    "text": "+ 1"
                }
            },
            {
                "box": {
                    "id": "obj-94",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 179.0, 779.0, 29.5, 22.0 ],
                    "text": "/ 2"
                }
            },
            {
                "box": {
                    "id": "obj-82",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 243.0, 1047.0, 67.0, 23.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 44.0, 97.5, 60.0, 23.0 ],
                    "text": "音訊設定"
                }
            },
            {
                "box": {
                    "id": "obj-18",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 69.0, 961.0, 58.0, 22.0 ],
                    "text": "loadbang"
                }
            },
            {
                "box": {
                    "id": "obj-76",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 243.0, 1070.0, 35.0, 22.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 7.0, 97.5, 35.0, 22.0 ],
                    "text": "open"
                }
            },
            {
                "box": {
                    "id": "obj-74",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 214.0, 462.0, 23.0, 22.0 ],
                    "text": "r b"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-19",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 681.0, 448.0, 42.0, 23.0 ],
                    "text": "clear"
                }
            },
            {
                "box": {
                    "id": "obj-88",
                    "maxclass": "button",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 658.0, 385.0, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-21",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 658.0, 512.0, 29.5, 22.0 ],
                    "text": "+ 1"
                }
            },
            {
                "box": {
                    "id": "obj-22",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "int", "bang" ],
                    "patching_rect": [ 658.0, 485.0, 43.0, 22.0 ],
                    "text": "urn 24"
                }
            },
            {
                "box": {
                    "id": "obj-48",
                    "linecount": 2,
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "signal" ],
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
                        "rect": [ 264.0, 130.0, 763.0, 544.0 ],
                        "boxes": [
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-12",
                                    "index": 1,
                                    "maxclass": "inlet",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "int" ],
                                    "patching_rect": [ 26.0, 88.0, 30.0, 30.0 ]
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-36",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 31.25, 334.5, 29.5, 22.0 ],
                                    "text": "120"
                                }
                            },
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-25",
                                    "index": 2,
                                    "maxclass": "inlet",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 87.99996948242188, 57.0, 30.0, 30.0 ]
                                }
                            },
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-14",
                                    "index": 2,
                                    "maxclass": "outlet",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 123.0, 477.5, 30.0, 30.0 ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-22",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 631.0, 111.0, 21.0, 20.0 ],
                                    "text": "R"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-30",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 525.0, 111.0, 21.0, 20.0 ],
                                    "text": "L"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-63",
                                    "linecount": 2,
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 526.0, 78.0, 126.0, 33.0 ],
                                    "text": "stereo position for each \"playback head\""
                                }
                            },
                            {
                                "box": {
                                    "fontsize": 12.0,
                                    "id": "obj-94",
                                    "maxclass": "preset",
                                    "numinlets": 1,
                                    "numoutlets": 5,
                                    "outlettype": [ "preset", "int", "preset", "int", "" ],
                                    "patching_rect": [ 10.0, 148.0, 43.0, 54.0 ],
                                    "preset_data": [
                                        {
                                            "number": 1,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 45.355735778808594, 64.1427001953125, 78.55844116210938, 90.71147155761719, 101.41851043701172, 111.0984115600586, 120.0, 12, "obj-32", "multislider", "list", 1.0, 0.928571403026581, 0.857142865657806, 0.785714268684387, 0.714285731315613, 0.642857134342194, 0.571428596973419, 0.5, 5, "obj-19", "number", "float", 0.5, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 120.0, 5, "obj-13", "number", "float", 1.0, 5, "obj-11", "number", "float", 1.0, 5, "obj-10", "number", "float", 0.5, 12, "obj-64", "multislider", "list", -0.283333331346512, 0.383333325386047, -1.0, 0.850000023841858, -0.666666686534882, 1.0, -1.0, 0.850000023841858, 12, "obj-49", "multislider", "list", 68, 57, 55, 54, 54, 55, 59, 62, 5, "obj-58", "number", "float", 10.0, 5, "obj-71", "number", "float", 1.0, 5, "obj-87", "number", "float", 300.0, 5, "obj-88", "number", "float", 0.300000011920929 ]
                                        },
                                        {
                                            "number": 2,
                                            "data": [ 12, "obj-34", "multislider", "list", 1.0, 240.0, 693.3333129882812, 746.6666870117188, 400.0, 373.3333435058594, 463.2016906738281, 1000.0, 12, "obj-32", "multislider", "list", 0.200000002980232, 0.333333343267441, 0.533333361148834, 0.493333339691162, 0.319999992847443, 0.266666680574417, 0.266666680574417, 0.5, 5, "obj-19", "number", "float", 5.0, 5, "obj-17", "number", "float", 1.0, 5, "obj-16", "number", "float", 1000.0, 5, "obj-13", "number", "float", 3.0, 5, "obj-11", "number", "float", 0.100000001490116, 5, "obj-10", "number", "float", 0.5, 12, "obj-64", "multislider", "list", -0.813558995723724, 0.271185994148254, -0.45762699842453, -0.118643999099731, 0.338982999324799, 1.0, -0.933333337306976, -0.796609997749329, 12, "obj-49", "multislider", "list", 50, 64, 77, 93, 80, 78, 64, 50, 5, "obj-58", "number", "float", 5.0, 5, "obj-71", "number", "float", 0.600000023841858, 5, "obj-87", "number", "float", 333.0, 5, "obj-88", "number", "float", 0.800000011920929 ]
                                        },
                                        {
                                            "number": 3,
                                            "data": [ 12, "obj-34", "multislider", "list", 10.0, 69.1962890625, 155.55642700195312, 256.3757019042969, 367.90545654296875, 488.1427001953125, 615.8076782226562, 750.0, 12, "obj-32", "multislider", "list", 0.300000011920929, 0.300577133893967, 0.318468481302261, 0.440245121717453, 0.890991866588593, 1.0, 1.0, 1.0, 5, "obj-19", "number", "float", 1.297999978065491, 5, "obj-17", "number", "float", 10.0, 5, "obj-16", "number", "float", 750.0, 5, "obj-13", "number", "float", 5.0, 5, "obj-11", "number", "float", 0.300000011920929, 5, "obj-10", "number", "float", 10.0, 12, "obj-64", "multislider", "list", -0.813558995723724, 0.271185994148254, -0.45762699842453, -0.118643999099731, 0.338982999324799, 1.0, 0.0, -0.796609997749329, 12, "obj-49", "multislider", "list", 50, 64, 77, 93, 49, 63, 77, 92, 5, "obj-58", "number", "float", 5.0, 5, "obj-71", "number", "float", 0.600000023841858, 5, "obj-87", "number", "float", 500.0, 5, "obj-88", "number", "float", 0.5 ]
                                        },
                                        {
                                            "number": 4,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 59.996238708496094, 147.52340698242188, 249.70509338378906, 362.7420349121094, 484.6040954589844, 613.9942626953125, 750.0, 12, "obj-32", "multislider", "list", 0.146666660904884, 0.300637453794479, 0.30771866440773, 0.333198428153992, 0.393464595079422, 0.508607268333435, 0.701997637748718, 0.800000011920929, 5, "obj-19", "number", "float", 1.297999978065491, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 750.0, 5, "obj-13", "number", "float", 3.598000049591064, 5, "obj-11", "number", "float", 0.300000011920929, 5, "obj-10", "number", "float", 1.0, 12, "obj-64", "multislider", "list", -1.0, 1.0, -0.600000023841858, -0.118643999099731, 0.338982999324799, 1.0, 0.0, -1.0, 12, "obj-49", "multislider", "list", 50, 64, 77, 93, 49, 63, 77, 92, 5, "obj-58", "number", "float", 5.0, 5, "obj-71", "number", "float", 0.600000023841858, 5, "obj-87", "number", "float", 750.0, 5, "obj-88", "number", "float", 0.649999976158142 ]
                                        },
                                        {
                                            "number": 5,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 57.14285659790039, 114.28571319580078, 171.42857360839844, 228.57142639160156, 285.71429443359375, 342.8571472167969, 1813.3333740234375, 12, "obj-32", "multislider", "list", 0.893333315849304, 0.395918369293213, 0.383673489093781, 0.363265305757523, 0.334693878889084, 0.297959178686142, 0.253061234951019, 0.200000002980232, 5, "obj-19", "number", "float", 1.0, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 400.0, 5, "obj-13", "number", "float", 2.0, 5, "obj-11", "number", "float", 0.400000005960464, 5, "obj-10", "number", "float", 0.200000002980232, 12, "obj-64", "multislider", "list", -0.349999994039536, -0.5, -0.666666686534882, 0.16666667163372, 0.383333325386047, 0.616666674613953, 0.866666674613953, 1.0, 12, "obj-49", "multislider", "list", 55, 77, 50, 48, 59, 51, 71, 53, 5, "obj-58", "number", "float", 55.0, 5, "obj-71", "number", "float", 0.100000001490116, 5, "obj-87", "number", "float", 15.0, 5, "obj-88", "number", "float", 0.400000005960464 ]
                                        },
                                        {
                                            "number": 6,
                                            "data": [ 12, "obj-34", "multislider", "list", 1.0, 9.142857551574707, 33.57143020629883, 74.28571319580078, 131.2857208251953, 204.57142639160156, 294.1428527832031, 400.0, 12, "obj-32", "multislider", "list", 0.400000005960464, 0.395918369293213, 0.383673459291458, 0.363265305757523, 0.334693878889084, 0.297959178686142, 0.253061234951019, 0.200000002980232, 5, "obj-19", "number", "float", 2.0, 5, "obj-17", "number", "float", 1.0, 5, "obj-16", "number", "float", 400.0, 5, "obj-13", "number", "float", 2.0, 5, "obj-11", "number", "float", 0.400000005960464, 5, "obj-10", "number", "float", 0.200000002980232, 12, "obj-64", "multislider", "list", -0.779660999774933, -0.779660999774933, -0.779660999774933, -1.0, 1.0, 0.881356000900269, 0.881356000900269, 0.881356000900269, 12, "obj-49", "multislider", "list", 55, 76, 47, 77, 59, 84, 50, 84, 5, "obj-58", "number", "float", 160.0, 5, "obj-71", "number", "float", 0.25, 5, "obj-87", "number", "float", 75.0, 5, "obj-88", "number", "float", 0.550000011920929 ]
                                        },
                                        {
                                            "number": 7,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 107.14286041259766, 214.2857208251953, 321.4285583496094, 428.5714416503906, 535.7142944335938, 642.8571166992188, 750.0, 12, "obj-32", "multislider", "list", 0.200000002980232, 0.257142871618271, 0.314285725355148, 0.371428579092026, 0.428571432828903, 0.360000014305115, 0.239999994635582, 0.106666669249535, 5, "obj-19", "number", "float", 1.0, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 750.0, 5, "obj-13", "number", "float", 1.0, 5, "obj-11", "number", "float", 0.200000002980232, 5, "obj-10", "number", "float", 0.600000023841858, 12, "obj-64", "multislider", "list", -1.0, 0.983051002025604, -0.983051002025604, 1.0, -1.0, 1.0, -1.0, 1.0, 12, "obj-49", "multislider", "list", 96, 79, 62, 52, 47, 43, 41, 39, 5, "obj-58", "number", "float", 15.0, 5, "obj-71", "number", "float", 0.5, 5, "obj-87", "number", "float", 180.0, 5, "obj-88", "number", "float", 0.800000011920929 ]
                                        },
                                        {
                                            "number": 8,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 107.14286, 214.285721, 321.428558, 428.571442, 535.714294, 642.857117, 750.0, 12, "obj-32", "multislider", "list", 0.2, 0.257143, 0.314286, 0.371429, 0.428571, 0.485714, 0.542857, 0.6, 5, "obj-19", "number", "float", 1.0, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 750.0, 5, "obj-13", "number", "float", 1.0, 5, "obj-11", "number", "float", 0.2, 5, "obj-10", "number", "float", 0.6, 12, "obj-64", "multislider", "list", -1.0, 0.983051, -0.983051, 1.0, -1.0, 1.0, -1.0, 1.0, 12, "obj-49", "multislider", "list", 96, 79, 62, 52, 47, 43, 41, 39, 5, "obj-58", "number", "float", 15.0, 5, "obj-71", "number", "float", 0.5, 5, "obj-87", "number", "float", 150.0, 5, "obj-88", "number", "float", 0.65 ]
                                        },
                                        {
                                            "number": 9,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 7.713560581207275, 43.63448715209961, 120.24250793457031, 246.8339385986328, 431.2011413574219, 680.1943359375, 1000.0, 12, "obj-32", "multislider", "list", 0.699999988079071, 0.687952876091003, 0.658049464225769, 0.612963438034058, 0.553919732570648, 0.481712162494659, 0.396921068429947, 0.300000011920929, 5, "obj-19", "number", "float", 2.5, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 1000.0, 5, "obj-13", "number", "float", 1.799999952316284, 5, "obj-11", "number", "float", 0.699999988079071, 5, "obj-10", "number", "float", 0.300000011920929, 12, "obj-64", "multislider", "list", -0.796609997749329, -0.474575996398926, -0.033897999674082, 0.288136005401611, 0.508475005626678, 0.694914996623993, 0.91525399684906, -0.847458004951477, 12, "obj-49", "multislider", "list", 82, 78, 69, 85, 67, 75, 87, 79, 5, "obj-58", "number", "float", 20.0, 5, "obj-71", "number", "float", 0.300000011920929, 5, "obj-87", "number", "float", 100.0, 5, "obj-88", "number", "float", 0.300000011920929 ]
                                        },
                                        {
                                            "number": 10,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 7.713561, 43.634487, 120.242508, 246.833939, 431.201141, 680.194336, 1000.0, 12, "obj-32", "multislider", "list", 0.7, 0.687953, 0.658049, 0.612963, 0.55392, 0.481712, 0.396921, 0.3, 5, "obj-19", "number", "float", 2.5, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 1000.0, 5, "obj-13", "number", "float", 1.8, 5, "obj-11", "number", "float", 0.7, 5, "obj-10", "number", "float", 0.3, 12, "obj-64", "multislider", "list", -0.79661, -0.474576, -0.033898, 0.288136, 0.508475, 0.694915, 0.915254, -0.847458, 12, "obj-49", "multislider", "list", 96, 96, 96, 96, 96, 95, 94, 93, 5, "obj-58", "number", "float", 20.0, 5, "obj-71", "number", "float", 0.3, 5, "obj-87", "number", "float", 666.599976, 5, "obj-88", "number", "float", 0.62 ]
                                        },
                                        {
                                            "number": 11,
                                            "data": [ 12, "obj-34", "multislider", "list", 0.0, 15.42712116241455, 87.26897430419922, 240.48501586914062, 493.6678771972656, 862.4022827148438, 1360.388671875, 853.3333129882812, 12, "obj-32", "multislider", "list", 0.386666655540466, 0.41333332657814, 0.578827857971191, 0.557491958141327, 0.540112376213074, 0.333333343267441, 0.079999998211861, 0.0, 5, "obj-19", "number", "float", 2.5, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 2000.0, 5, "obj-13", "number", "float", 0.400000005960464, 5, "obj-11", "number", "float", 0.699999988079071, 5, "obj-10", "number", "float", 0.5, 12, "obj-64", "multislider", "list", 0.016948999837041, -0.118643999099731, -0.559321999549866, -1.0, 1.0, 0.694914996623993, 0.288136005401611, -0.466666668653488, 12, "obj-49", "multislider", "list", 72, 49, 49, 54, 61, 57, 49, 80, 5, "obj-58", "number", "float", 20.0, 5, "obj-71", "number", "float", 0.5, 5, "obj-87", "number", "float", 50.0, 5, "obj-88", "number", "float", 0.25 ]
                                        },
                                        {
                                            "number": 12,
                                            "data": [ 12, "obj-34", "multislider", "list", 880.0, 880.0, 693.3333129882812, 400.0, 493.6678771972656, 720.0, 720.0, 720.0, 12, "obj-32", "multislider", "list", 0.293333321809769, 0.453333348035812, 0.578827857971191, 0.759999990463257, 0.54666668176651, 0.386666655540466, 0.479999989271164, 0.706666648387909, 5, "obj-19", "number", "float", 2.5, 5, "obj-17", "number", "float", 0.0, 5, "obj-16", "number", "float", 2000.0, 5, "obj-13", "number", "float", 0.400000005960464, 5, "obj-11", "number", "float", 0.699999988079071, 5, "obj-10", "number", "float", 0.5, 12, "obj-64", "multislider", "list", 1.0, 0.850000023841858, 0.266666680574417, 0.200000002980232, 0.200000002980232, -0.483333319425583, -0.933333337306976, -1.0, 12, "obj-49", "multislider", "list", 61, 61, 58, 54, 51, 46, 41, 54, 5, "obj-58", "number", "float", 10.0, 5, "obj-71", "number", "float", 1.0, 5, "obj-87", "number", "float", 1125.0, 5, "obj-88", "number", "float", 0.800000011920929 ]
                                        },
                                        {
                                            "number": 13,
                                            "data": [ 12, "obj-34", "multislider", "list", 1000.0, 1173.544922, 1323.846191, 1466.466919, 1604.318359, 1738.728394, 1870.45813, 2000.0, 12, "obj-32", "multislider", "list", 0.5, 0.637747, 0.681758, 0.713762, 0.739831, 0.762223, 0.782061, 0.8, 5, "obj-19", "number", "float", 0.9, 5, "obj-17", "number", "float", 1000.0, 5, "obj-16", "number", "float", 2000.0, 5, "obj-13", "number", "float", 0.4, 5, "obj-11", "number", "float", 0.5, 5, "obj-10", "number", "float", 0.8, 12, "obj-64", "multislider", "list", -0.38983, -0.152542, -0.050847, 0.050847, 0.135593, 0.20339, 0.254237, 0.355932, 12, "obj-49", "multislider", "list", 91, 36, 38, 40, 41, 44, 46, 95, 5, "obj-58", "number", "float", 90.0, 5, "obj-71", "number", "float", 0.35, 5, "obj-87", "number", "float", 0.0, 5, "obj-88", "number", "float", 0.0 ]
                                        },
                                        {
                                            "number": 14,
                                            "data": [ 12, "obj-34", "multislider", "list", 1000.0, 1173.544922, 1323.846191, 1466.466919, 1604.318359, 1738.728394, 1870.45813, 2000.0, 12, "obj-32", "multislider", "list", 0.5, 0.637747, 0.681758, 0.713762, 0.739831, 0.762223, 0.782061, 0.8, 5, "obj-19", "number", "float", 0.9, 5, "obj-17", "number", "float", 1000.0, 5, "obj-16", "number", "float", 2000.0, 5, "obj-13", "number", "float", 0.4, 5, "obj-11", "number", "float", 0.5, 5, "obj-10", "number", "float", 0.8, 12, "obj-64", "multislider", "list", -0.38983, -0.152542, -0.050847, 0.050847, 0.135593, 0.20339, 0.254237, 0.355932, 12, "obj-49", "multislider", "list", 91, 36, 38, 40, 41, 44, 46, 95, 5, "obj-58", "number", "float", 90.0, 5, "obj-71", "number", "float", 0.35, 5, "obj-87", "number", "float", 375.0, 5, "obj-88", "number", "float", 0.75 ]
                                        },
                                        {
                                            "number": 15,
                                            "data": [ 12, "obj-34", "multislider", "list", 750.0, 1403.87146, 1573.636108, 1692.700562, 1787.476685, 1867.504761, 1937.453857, 2000.0, 12, "obj-32", "multislider", "list", 1.0, 0.816337, 0.757656, 0.714984, 0.680225, 0.65037, 0.623919, 0.6, 5, "obj-19", "number", "float", 0.333, 5, "obj-17", "number", "float", 750.0, 5, "obj-16", "number", "float", 2000.0, 5, "obj-13", "number", "float", 0.4, 5, "obj-11", "number", "float", 1.0, 5, "obj-10", "number", "float", 0.6, 12, "obj-64", "multislider", "list", 0.966102, 0.474576, 0.254237, 0.084746, -0.169492, -0.322034, -0.59322, -0.983051, 12, "obj-49", "multislider", "list", 58, 95, 92, 91, 88, 95, 92, 90, 5, "obj-58", "number", "float", 70.0, 5, "obj-71", "number", "float", 0.15, 5, "obj-87", "number", "float", 0.0, 5, "obj-88", "number", "float", 0.0 ]
                                        },
                                        {
                                            "number": 16,
                                            "data": [ 12, "obj-34", "multislider", "list", 750.0, 1403.87146, 1573.636108, 1692.700562, 1787.476685, 1867.504761, 1937.453857, 2000.0, 12, "obj-32", "multislider", "list", 1.0, 0.816337, 0.757656, 0.714984, 0.680225, 0.65037, 0.623919, 0.6, 5, "obj-19", "number", "float", 0.333, 5, "obj-17", "number", "float", 750.0, 5, "obj-16", "number", "float", 2000.0, 5, "obj-13", "number", "float", 0.4, 5, "obj-11", "number", "float", 1.0, 5, "obj-10", "number", "float", 0.6, 12, "obj-64", "multislider", "list", 0.966102, 0.474576, 0.254237, 0.084746, -0.169492, -0.322034, -0.59322, -0.983051, 12, "obj-49", "multislider", "list", 58, 95, 92, 91, 88, 95, 92, 90, 5, "obj-58", "number", "float", 70.0, 5, "obj-71", "number", "float", 0.15, 5, "obj-87", "number", "float", 100.0, 5, "obj-88", "number", "float", 0.8 ]
                                        }
                                    ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-93",
                                    "linecount": 2,
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 139.0, 190.0, 61.0, 33.0 ],
                                    "text": "feedback amount"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-92",
                                    "linecount": 2,
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 116.0, 136.0, 61.0, 33.0 ],
                                    "text": "feedback delay"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-88",
                                    "maxclass": "flonum",
                                    "maximum": 0.99,
                                    "minimum": 0.0,
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 141.0, 222.0, 50.0, 22.0 ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-87",
                                    "maxclass": "flonum",
                                    "maximum": 2000.0,
                                    "minimum": 0.0,
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 115.0, 168.0, 50.0, 22.0 ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-85",
                                    "maxclass": "newobj",
                                    "numinlets": 3,
                                    "numoutlets": 1,
                                    "outlettype": [ "signal" ],
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
                                        "rect": [ 74.0, 104.0, 238.0, 204.0 ],
                                        "boxes": [
                                            {
                                                "box": {
                                                    "fontname": "Arial",
                                                    "fontsize": 12.0,
                                                    "id": "obj-7",
                                                    "linecount": 2,
                                                    "maxclass": "comment",
                                                    "numinlets": 1,
                                                    "numoutlets": 0,
                                                    "patching_rect": [ 172.0, 8.0, 61.0, 33.0 ],
                                                    "text": "feedback amount"
                                                }
                                            },
                                            {
                                                "box": {
                                                    "fontname": "Arial",
                                                    "fontsize": 12.0,
                                                    "id": "obj-6",
                                                    "linecount": 2,
                                                    "maxclass": "comment",
                                                    "numinlets": 1,
                                                    "numoutlets": 0,
                                                    "patching_rect": [ 112.0, 8.0, 61.0, 33.0 ],
                                                    "text": "feedback delay"
                                                }
                                            },
                                            {
                                                "box": {
                                                    "comment": "",
                                                    "id": "obj-4",
                                                    "index": 3,
                                                    "maxclass": "inlet",
                                                    "numinlets": 0,
                                                    "numoutlets": 1,
                                                    "outlettype": [ "" ],
                                                    "patching_rect": [ 184.0, 46.0, 25.0, 25.0 ]
                                                }
                                            },
                                            {
                                                "box": {
                                                    "fontname": "Arial",
                                                    "fontsize": 12.0,
                                                    "id": "obj-3",
                                                    "maxclass": "newobj",
                                                    "numinlets": 2,
                                                    "numoutlets": 1,
                                                    "outlettype": [ "signal" ],
                                                    "patching_rect": [ 45.0, 133.0, 101.5, 20.0 ],
                                                    "text": "*~"
                                                }
                                            },
                                            {
                                                "box": {
                                                    "comment": "",
                                                    "id": "obj-2",
                                                    "index": 2,
                                                    "maxclass": "inlet",
                                                    "numinlets": 0,
                                                    "numoutlets": 1,
                                                    "outlettype": [ "" ],
                                                    "patching_rect": [ 124.0, 47.0, 25.0, 25.0 ]
                                                }
                                            },
                                            {
                                                "box": {
                                                    "fontname": "Arial",
                                                    "fontsize": 12.0,
                                                    "id": "obj-1",
                                                    "maxclass": "newobj",
                                                    "numinlets": 1,
                                                    "numoutlets": 1,
                                                    "outlettype": [ "signal" ],
                                                    "patching_rect": [ 45.0, 106.0, 51.0, 20.0 ],
                                                    "text": "tapout~"
                                                }
                                            },
                                            {
                                                "box": {
                                                    "fontname": "Arial",
                                                    "fontsize": 12.0,
                                                    "id": "obj-45",
                                                    "maxclass": "newobj",
                                                    "numinlets": 1,
                                                    "numoutlets": 1,
                                                    "outlettype": [ "tapconnect" ],
                                                    "patching_rect": [ 45.0, 65.0, 74.0, 20.0 ],
                                                    "text": "tapin~ 2000"
                                                }
                                            },
                                            {
                                                "box": {
                                                    "comment": "",
                                                    "id": "obj-83",
                                                    "index": 1,
                                                    "maxclass": "inlet",
                                                    "numinlets": 0,
                                                    "numoutlets": 1,
                                                    "outlettype": [ "signal" ],
                                                    "patching_rect": [ 13.0, 8.0, 25.0, 25.0 ]
                                                }
                                            },
                                            {
                                                "box": {
                                                    "comment": "",
                                                    "id": "obj-84",
                                                    "index": 1,
                                                    "maxclass": "outlet",
                                                    "numinlets": 1,
                                                    "numoutlets": 0,
                                                    "patching_rect": [ 13.0, 171.0, 25.0, 25.0 ]
                                                }
                                            }
                                        ],
                                        "lines": [
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-3", 0 ],
                                                    "source": [ "obj-1", 0 ]
                                                }
                                            },
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-1", 0 ],
                                                    "midpoints": [ 133.5, 93.5, 54.5, 93.5 ],
                                                    "source": [ "obj-2", 0 ]
                                                }
                                            },
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-45", 0 ],
                                                    "midpoints": [ 54.5, 162.0, 158.0, 162.0, 158.0, 40.0, 54.5, 40.0 ],
                                                    "order": 0,
                                                    "source": [ "obj-3", 0 ]
                                                }
                                            },
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-84", 0 ],
                                                    "order": 1,
                                                    "source": [ "obj-3", 0 ]
                                                }
                                            },
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-3", 1 ],
                                                    "source": [ "obj-4", 0 ]
                                                }
                                            },
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-1", 0 ],
                                                    "midpoints": [ 54.5, 93.0, 54.5, 93.0 ],
                                                    "source": [ "obj-45", 0 ]
                                                }
                                            },
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-45", 0 ],
                                                    "order": 0,
                                                    "source": [ "obj-83", 0 ]
                                                }
                                            },
                                            {
                                                "patchline": {
                                                    "destination": [ "obj-84", 0 ],
                                                    "order": 1,
                                                    "source": [ "obj-83", 0 ]
                                                }
                                            }
                                        ]
                                    },
                                    "patching_rect": [ 106.0, 263.0, 69.0, 22.0 ],
                                    "text": "p feedback"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-78",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 574.0, 335.0, 66.0, 20.0 ],
                                    "text": "reson gain"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-77",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 492.0, 333.0, 56.0, 20.0 ],
                                    "text": "Q factor"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-75",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 322.0, 333.0, 132.0, 20.0 ],
                                    "text": "resonance frequency"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-69",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 574.0, 404.0, 59.0, 22.0 ],
                                    "text": "s resgain"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-70",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 574.0, 381.0, 71.0, 22.0 ],
                                    "text": "target 0, $1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-71",
                                    "maxclass": "flonum",
                                    "maximum": 1.0,
                                    "minimum": 0.0,
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 574.0, 356.0, 50.0, 22.0 ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-68",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 323.0, 269.0, 57.0, 22.0 ],
                                    "text": "r resgain"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-61",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 239.0, 359.0, 34.0, 22.0 ],
                                    "text": "mtof"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-59",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 492.0, 404.0, 43.0, 22.0 ],
                                    "text": "s resq"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-60",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 492.0, 381.0, 71.0, 22.0 ],
                                    "text": "target 0, $1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-58",
                                    "maxclass": "flonum",
                                    "minimum": 0.5,
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 492.0, 356.0, 50.0, 22.0 ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-56",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 239.0, 430.0, 57.0, 22.0 ],
                                    "text": "s resfreq"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-27",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 239.0, 407.0, 78.0, 22.0 ],
                                    "text": "target $1, $2"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-29",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "list" ],
                                    "patching_rect": [ 239.0, 384.0, 69.0, 22.0 ],
                                    "text": "listfunnel 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-35",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 448.0, 348.0, 42.0, 20.0 ],
                                    "text": "C 6"
                                }
                            },
                            {
                                "box": {
                                    "bgcolor": [ 1.0, 1.0, 1.0, 1.0 ],
                                    "candicane2": [ 0.145098, 0.203922, 0.356863, 1.0 ],
                                    "candicane3": [ 0.290196, 0.411765, 0.713726, 1.0 ],
                                    "candicane4": [ 0.439216, 0.619608, 0.070588, 1.0 ],
                                    "candicane5": [ 0.584314, 0.827451, 0.431373, 1.0 ],
                                    "candicane6": [ 0.733333, 0.035294, 0.788235, 1.0 ],
                                    "candicane7": [ 0.878431, 0.243137, 0.145098, 1.0 ],
                                    "candicane8": [ 0.027451, 0.447059, 0.501961, 1.0 ],
                                    "contdata": 1,
                                    "ghostbar": 40,
                                    "id": "obj-49",
                                    "maxclass": "multislider",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 327.0, 353.0, 120.0, 90.0 ],
                                    "peakcolor": [ 0.498039, 0.498039, 0.498039, 1.0 ],
                                    "setminmax": [ 36.0, 96.0 ],
                                    "settype": 0,
                                    "size": 8,
                                    "slidercolor": [ 0.392157, 0.207843, 0.129412, 1.0 ],
                                    "spacing": 1
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-53",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 447.0, 432.0, 43.0, 20.0 ],
                                    "text": "C 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-24",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 461.0, 269.0, 41.0, 22.0 ],
                                    "text": "r resq"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-4",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 392.0, 269.0, 55.0, 22.0 ],
                                    "text": "r resfreq"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-2",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 502.0, 123.0, 23.0, 20.0 ],
                                    "text": "1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-1",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 502.0, 190.0, 23.0, 20.0 ],
                                    "text": "0"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-54",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 527.0, 237.0, 78.0, 22.0 ],
                                    "text": "target $1, $2"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-55",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "list" ],
                                    "patching_rect": [ 527.0, 214.0, 68.0, 22.0 ],
                                    "text": "listfunnel 1"
                                }
                            },
                            {
                                "box": {
                                    "candicane2": [ 0.145098, 0.203922, 0.356863, 1.0 ],
                                    "candicane3": [ 0.290196, 0.411765, 0.713726, 1.0 ],
                                    "candicane4": [ 0.439216, 0.619608, 0.070588, 1.0 ],
                                    "candicane5": [ 0.584314, 0.827451, 0.431373, 1.0 ],
                                    "candicane6": [ 0.733333, 0.035294, 0.788235, 1.0 ],
                                    "candicane7": [ 0.878431, 0.243137, 0.145098, 1.0 ],
                                    "candicane8": [ 0.027451, 0.447059, 0.501961, 1.0 ],
                                    "id": "obj-64",
                                    "maxclass": "multislider",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "orientation": 0,
                                    "outlettype": [ "", "" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 527.0, 127.0, 120.0, 75.0 ],
                                    "peakcolor": [ 0.498039, 0.498039, 0.498039, 1.0 ],
                                    "setstyle": 1,
                                    "signed": 1,
                                    "size": 8,
                                    "spacing": 1
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-50",
                                    "maxclass": "newobj",
                                    "numinlets": 4,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 381.0, 47.0, 80.0, 22.0 ],
                                    "text": "pak 8 0. 0. 0."
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-31",
                                    "interpinlet": 1,
                                    "maxclass": "gain~",
                                    "multichannelvariant": 0,
                                    "numinlets": 2,
                                    "numoutlets": 2,
                                    "outlettype": [ "signal", "" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 112.999969, 334.5, 21.0, 81.0 ]
                                }
                            },
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-41",
                                    "index": 1,
                                    "maxclass": "outlet",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 88.99996948242188, 477.5, 30.0, 30.0 ]
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-42",
                                    "interpinlet": 1,
                                    "maxclass": "gain~",
                                    "multichannelvariant": 0,
                                    "numinlets": 2,
                                    "numoutlets": 2,
                                    "outlettype": [ "signal", "" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 88.999969, 334.5, 21.0, 81.0 ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-20",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 382.0, 237.0, 78.0, 22.0 ],
                                    "text": "target $1, $2"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-26",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "list" ],
                                    "patching_rect": [ 382.0, 214.0, 68.0, 22.0 ],
                                    "text": "listfunnel 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-18",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 204.0, 237.0, 78.0, 22.0 ],
                                    "text": "target $1, $2"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-3",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "list" ],
                                    "patching_rect": [ 204.0, 214.0, 68.0, 22.0 ],
                                    "text": "listfunnel 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-52",
                                    "maxclass": "newobj",
                                    "numinlets": 4,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 204.0, 48.0, 80.0, 22.0 ],
                                    "text": "pak 8 0. 0. 0."
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-5",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 431.0, 3.0, 31.0, 20.0 ],
                                    "text": "end"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-6",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 379.0, 3.0, 34.0, 20.0 ],
                                    "text": "start"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-7",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 486.0, 3.0, 40.0, 20.0 ],
                                    "text": "curve"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-8",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 257.0, 3.0, 31.0, 20.0 ],
                                    "text": "end"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-9",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 204.0, 3.0, 34.0, 20.0 ],
                                    "text": "start"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-10",
                                    "maxclass": "flonum",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 432.0, 20.0, 52.0, 22.0 ],
                                    "triscale": 0.9
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-11",
                                    "maxclass": "flonum",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 379.0, 20.0, 52.0, 22.0 ],
                                    "triscale": 0.9
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-13",
                                    "maxclass": "flonum",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 485.0, 20.0, 46.0, 22.0 ],
                                    "triscale": 0.9
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-15",
                                    "maxclass": "newobj",
                                    "numinlets": 4,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 381.0, 71.0, 90.0, 22.0 ],
                                    "text": "vs.explist 0 1 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-16",
                                    "maxclass": "flonum",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 258.0, 20.0, 54.0, 22.0 ],
                                    "triscale": 0.9
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-17",
                                    "maxclass": "flonum",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 203.0, 20.0, 54.0, 22.0 ],
                                    "triscale": 0.9
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "format": 6,
                                    "id": "obj-19",
                                    "maxclass": "flonum",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 313.0, 20.0, 46.0, 22.0 ],
                                    "triscale": 0.9
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-21",
                                    "maxclass": "newobj",
                                    "numinlets": 4,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 204.0, 71.0, 110.0, 22.0 ],
                                    "text": "vs.explist 0 1000 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "hidden": 1,
                                    "id": "obj-23",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 10.0, 57.0, 72.0, 22.0 ],
                                    "text": "loadmess 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-28",
                                    "linecount": 2,
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 391.0, 93.0, 114.0, 33.0 ],
                                    "text": "amplitude for each \"playback head\""
                                }
                            },
                            {
                                "box": {
                                    "candicane2": [ 0.145098, 0.203922, 0.356863, 1.0 ],
                                    "candicane3": [ 0.290196, 0.411765, 0.713726, 1.0 ],
                                    "candicane4": [ 0.439216, 0.619608, 0.070588, 1.0 ],
                                    "candicane5": [ 0.584314, 0.827451, 0.431373, 1.0 ],
                                    "candicane6": [ 0.733333, 0.035294, 0.788235, 1.0 ],
                                    "candicane7": [ 0.878431, 0.243137, 0.145098, 1.0 ],
                                    "candicane8": [ 0.027451, 0.447059, 0.501961, 1.0 ],
                                    "ghostbar": 40,
                                    "id": "obj-32",
                                    "maxclass": "multislider",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 382.0, 127.0, 120.0, 75.0 ],
                                    "peakcolor": [ 0.498039, 0.498039, 0.498039, 1.0 ],
                                    "setminmax": [ 0.0, 1.0 ],
                                    "size": 8,
                                    "spacing": 1
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-33",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 323.0, 123.0, 57.0, 20.0 ],
                                    "text": "2000 ms"
                                }
                            },
                            {
                                "box": {
                                    "candicane2": [ 0.145098, 0.203922, 0.356863, 1.0 ],
                                    "candicane3": [ 0.290196, 0.411765, 0.713726, 1.0 ],
                                    "candicane4": [ 0.439216, 0.619608, 0.070588, 1.0 ],
                                    "candicane5": [ 0.584314, 0.827451, 0.431373, 1.0 ],
                                    "candicane6": [ 0.733333, 0.035294, 0.788235, 1.0 ],
                                    "candicane7": [ 0.878431, 0.243137, 0.145098, 1.0 ],
                                    "candicane8": [ 0.027451, 0.447059, 0.501961, 1.0 ],
                                    "ghostbar": 40,
                                    "id": "obj-34",
                                    "maxclass": "multislider",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 204.0, 127.0, 120.0, 75.0 ],
                                    "peakcolor": [ 0.498039, 0.498039, 0.498039, 1.0 ],
                                    "setminmax": [ 0.0, 2000.0 ],
                                    "size": 8,
                                    "spacing": 1
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-38",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "signal" ],
                                    "patching_rect": [ 88.0, 110.0, 34.0, 22.0 ],
                                    "text": "*~ 1."
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-44",
                                    "maxclass": "newobj",
                                    "numinlets": 7,
                                    "numoutlets": 2,
                                    "outlettype": [ "signal", "signal" ],
                                    "patching_rect": [ 123.0, 294.0, 423.0, 22.0 ],
                                    "text": "poly~ p_resontaps~ 8"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-46",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 323.0, 190.0, 37.0, 20.0 ],
                                    "text": "0 ms"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-47",
                                    "linecount": 2,
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 214.0, 93.0, 129.0, 33.0 ],
                                    "text": "delay time for each \"playback head\""
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-51",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 313.0, 3.0, 40.0, 20.0 ],
                                    "text": "curve"
                                }
                            }
                        ],
                        "lines": [
                            {
                                "patchline": {
                                    "destination": [ "obj-50", 2 ],
                                    "source": [ "obj-10", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-50", 1 ],
                                    "source": [ "obj-11", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-94", 0 ],
                                    "source": [ "obj-12", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-50", 3 ],
                                    "source": [ "obj-13", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-32", 0 ],
                                    "source": [ "obj-15", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-52", 2 ],
                                    "source": [ "obj-16", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-52", 1 ],
                                    "source": [ "obj-17", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-44", 1 ],
                                    "source": [ "obj-18", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-52", 3 ],
                                    "source": [ "obj-19", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-44", 2 ],
                                    "source": [ "obj-20", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-34", 0 ],
                                    "source": [ "obj-21", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-36", 0 ],
                                    "order": 0,
                                    "source": [ "obj-23", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-94", 0 ],
                                    "hidden": 1,
                                    "order": 1,
                                    "source": [ "obj-23", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-44", 5 ],
                                    "source": [ "obj-24", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-38", 0 ],
                                    "source": [ "obj-25", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-20", 0 ],
                                    "source": [ "obj-26", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-56", 0 ],
                                    "source": [ "obj-27", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-27", 0 ],
                                    "source": [ "obj-29", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-18", 0 ],
                                    "source": [ "obj-3", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-14", 0 ],
                                    "source": [ "obj-31", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-26", 0 ],
                                    "source": [ "obj-32", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-3", 0 ],
                                    "source": [ "obj-34", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-42", 0 ],
                                    "source": [ "obj-36", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-31", 0 ],
                                    "midpoints": [ 97.5, 276.0 ],
                                    "order": 0,
                                    "source": [ "obj-38", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-42", 0 ],
                                    "order": 2,
                                    "source": [ "obj-38", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-85", 0 ],
                                    "order": 1,
                                    "source": [ "obj-38", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-44", 4 ],
                                    "source": [ "obj-4", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-31", 0 ],
                                    "hidden": 1,
                                    "source": [ "obj-42", 1 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-41", 0 ],
                                    "source": [ "obj-42", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-31", 0 ],
                                    "order": 0,
                                    "source": [ "obj-44", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-42", 0 ],
                                    "order": 1,
                                    "source": [ "obj-44", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-61", 0 ],
                                    "midpoints": [ 336.5, 446.0, 321.0, 446.0, 321.0, 351.0, 248.5, 351.0 ],
                                    "source": [ "obj-49", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-15", 0 ],
                                    "source": [ "obj-50", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-21", 0 ],
                                    "source": [ "obj-52", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-44", 6 ],
                                    "source": [ "obj-54", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-54", 0 ],
                                    "source": [ "obj-55", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-60", 0 ],
                                    "source": [ "obj-58", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-59", 0 ],
                                    "source": [ "obj-60", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-29", 0 ],
                                    "source": [ "obj-61", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-55", 0 ],
                                    "source": [ "obj-64", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-44", 3 ],
                                    "source": [ "obj-68", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-69", 0 ],
                                    "source": [ "obj-70", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-70", 0 ],
                                    "source": [ "obj-71", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-44", 0 ],
                                    "midpoints": [ 115.5, 288.0, 132.5, 288.0 ],
                                    "source": [ "obj-85", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-85", 1 ],
                                    "midpoints": [ 124.5, 248.0, 140.5, 248.0 ],
                                    "source": [ "obj-87", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-85", 2 ],
                                    "midpoints": [ 150.5, 256.0, 165.5, 256.0 ],
                                    "source": [ "obj-88", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-31", 0 ],
                                    "hidden": 1,
                                    "order": 0,
                                    "source": [ "obj-94", 2 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-42", 0 ],
                                    "hidden": 1,
                                    "order": 1,
                                    "source": [ "obj-94", 2 ]
                                }
                            }
                        ]
                    },
                    "patching_rect": [ 179.0, 831.0, 71.0, 35.0 ],
                    "text": "p Multi_Delay"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "format": 6,
                    "id": "obj-25",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 65.0, 895.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-29",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "float" ],
                    "patching_rect": [ 65.0, 870.0, 32.5, 22.0 ],
                    "text": "!/ 1."
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-73",
                    "maxclass": "newobj",
                    "numinlets": 0,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 65.0, 845.0, 58.0, 22.0 ],
                    "text": "r numres"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-72",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 424.0, 516.0, 60.0, 22.0 ],
                    "text": "s numres"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-71",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 179.0, 935.0, 32.5, 22.0 ],
                    "text": "*~"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "hidden": 1,
                    "id": "obj-70",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 274.0, 460.0, 56.0, 22.0 ],
                    "text": "deferlow"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-69",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 65.0, 619.0, 36.0, 22.0 ],
                    "text": "*~ -1"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-59",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 65.0, 545.0, 32.5, 22.0 ],
                    "text": "int"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-58",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 79.0, 484.0, 99.0, 20.0 ],
                    "text": "rebound speed"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-57",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 129.0, 500.0, 51.0, 20.0 ],
                    "text": "end"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-55",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 130.0, 521.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-51",
                    "maxclass": "preset",
                    "numinlets": 1,
                    "numoutlets": 5,
                    "outlettype": [ "preset", "int", "preset", "int", "" ],
                    "patching_rect": [ 498.0, 493.0, 52.0, 78.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 34.0, 15.0, 52.0, 76.0 ],
                    "preset_data": [
                        {
                            "number": 1,
                            "data": [ 5, "obj-67", "number", "int", 4, 5, "obj-42", "number", "float", 400.0, 5, "obj-41", "number", "float", 8000.0, 5, "obj-40", "number", "float", 0.06, 5, "obj-38", "number", "float", 0.12, 5, "obj-46", "number", "int", 4, 5, "obj-47", "number", "int", 4000, 5, "obj-55", "number", "int", 600 ]
                        },
                        {
                            "number": 2,
                            "data": [ 5, "obj-67", "number", "int", 30, 5, "obj-42", "number", "float", 2800.0, 5, "obj-41", "number", "float", 12000.0, 5, "obj-40", "number", "float", 0.050000000745058, 5, "obj-38", "number", "float", 0.5, 5, "obj-46", "number", "int", 10, 5, "obj-47", "number", "int", 30, 5, "obj-55", "number", "int", 50, 5, "obj-25", "number", "float", 0.033333335071802 ]
                        },
                        {
                            "number": 3,
                            "data": [ 5, "obj-67", "number", "int", 10, 5, "obj-42", "number", "float", 500.0, 5, "obj-41", "number", "float", 4000.0, 5, "obj-40", "number", "float", 0.02, 5, "obj-38", "number", "float", 0.05, 5, "obj-46", "number", "int", 6, 5, "obj-47", "number", "int", 3000, 5, "obj-55", "number", "int", 800 ]
                        },
                        {
                            "number": 4,
                            "data": [ 5, "obj-67", "number", "int", 15, 5, "obj-42", "number", "float", 100.0, 5, "obj-41", "number", "float", 6000.0, 5, "obj-40", "number", "float", 0.001, 5, "obj-38", "number", "float", 0.02, 5, "obj-46", "number", "int", 3, 5, "obj-47", "number", "int", 3000, 5, "obj-55", "number", "int", 800, 5, "obj-25", "number", "float", 0.066667 ]
                        },
                        {
                            "number": 5,
                            "data": [ 5, "obj-67", "number", "int", 4, 5, "obj-42", "number", "float", 200.0, 5, "obj-41", "number", "float", 700.0, 5, "obj-40", "number", "float", 0.059999998658895, 5, "obj-38", "number", "float", 0.119999997317791, 5, "obj-46", "number", "int", 1, 5, "obj-47", "number", "int", 6000, 5, "obj-55", "number", "int", 300, 5, "obj-25", "number", "float", 0.25 ]
                        },
                        {
                            "number": 6,
                            "data": [ 5, "obj-67", "number", "int", 33, 5, "obj-42", "number", "float", 300.0, 5, "obj-41", "number", "float", 100.0, 5, "obj-40", "number", "float", 0.100000001490116, 5, "obj-38", "number", "float", 2.0, 5, "obj-46", "number", "int", 11, 5, "obj-47", "number", "int", 6000, 5, "obj-55", "number", "int", 66, 5, "obj-25", "number", "float", 0.050000000745058 ]
                        },
                        {
                            "number": 7,
                            "data": [ 5, "obj-67", "number", "int", 12, 5, "obj-42", "number", "float", 75.0, 5, "obj-41", "number", "float", 150.0, 5, "obj-40", "number", "float", 0.300000011920929, 5, "obj-38", "number", "float", 3.0, 5, "obj-46", "number", "int", 3, 5, "obj-47", "number", "int", 10000, 5, "obj-55", "number", "int", 30, 5, "obj-25", "number", "float", 0.08333333581686 ]
                        },
                        {
                            "number": 8,
                            "data": [ 5, "obj-67", "number", "int", 40, 5, "obj-42", "number", "float", 125.0, 5, "obj-41", "number", "float", 800.0, 5, "obj-40", "number", "float", 0.5, 5, "obj-38", "number", "float", 3.0, 5, "obj-46", "number", "int", 2, 5, "obj-47", "number", "int", 10000, 5, "obj-55", "number", "int", 5, 5, "obj-25", "number", "float", 0.009999999776483 ]
                        },
                        {
                            "number": 9,
                            "data": [ 5, "obj-67", "number", "int", 8, 5, "obj-42", "number", "float", 1000.0, 5, "obj-41", "number", "float", 15000.0, 5, "obj-40", "number", "float", 0.050000000745058, 5, "obj-38", "number", "float", 1.200000047683716, 5, "obj-46", "number", "int", 5, 5, "obj-47", "number", "int", 3000, 5, "obj-55", "number", "int", 800, 5, "obj-25", "number", "float", 0.050000000745058 ]
                        },
                        {
                            "number": 10,
                            "data": [ 5, "obj-67", "number", "int", 4, 5, "obj-42", "number", "float", 1000.0, 5, "obj-41", "number", "float", 10000.0, 5, "obj-40", "number", "float", 0.699999988079071, 5, "obj-38", "number", "float", 1.200000047683716, 5, "obj-46", "number", "int", 8, 5, "obj-47", "number", "int", 3000, 5, "obj-55", "number", "int", 800, 5, "obj-25", "number", "float", 0.079999998211861 ]
                        },
                        {
                            "number": 11,
                            "data": [ 5, "obj-67", "number", "int", 2, 5, "obj-42", "number", "float", 1000.0, 5, "obj-41", "number", "float", 4000.0, 5, "obj-40", "number", "float", 0.200000002980232, 5, "obj-38", "number", "float", 0.5, 5, "obj-46", "number", "int", 6, 5, "obj-47", "number", "int", 3000, 5, "obj-55", "number", "int", 2000, 5, "obj-25", "number", "float", 0.123999997973442 ]
                        },
                        {
                            "number": 12,
                            "data": [ 5, "obj-67", "number", "int", 2, 5, "obj-42", "number", "float", 1000.0, 5, "obj-41", "number", "float", 100.0, 5, "obj-40", "number", "float", 0.200000002980232, 5, "obj-38", "number", "float", 0.5, 5, "obj-46", "number", "int", 6, 5, "obj-47", "number", "int", 3000, 5, "obj-55", "number", "int", 2000, 5, "obj-25", "number", "float", 0.125 ]
                        },
                        {
                            "number": 13,
                            "data": [ 5, "obj-67", "number", "int", 4, 5, "obj-42", "number", "float", 500.0, 5, "obj-41", "number", "float", 8000.0, 5, "obj-40", "number", "float", 2.0, 5, "obj-38", "number", "float", 3.0, 5, "obj-46", "number", "int", 2, 5, "obj-47", "number", "int", 10000, 5, "obj-55", "number", "int", 350, 5, "obj-25", "number", "float", 0.079999998211861 ]
                        },
                        {
                            "number": 14,
                            "data": [ 5, "obj-67", "number", "int", 20, 5, "obj-42", "number", "float", 50.0, 5, "obj-41", "number", "float", 8000.0, 5, "obj-40", "number", "float", 0.100000001490116, 5, "obj-38", "number", "float", 0.100000001490116, 5, "obj-46", "number", "int", 1, 5, "obj-47", "number", "int", 10000, 5, "obj-55", "number", "int", 350 ]
                        },
                        {
                            "number": 15,
                            "data": [ 5, "obj-67", "number", "int", 10, 5, "obj-42", "number", "float", 222.0, 5, "obj-41", "number", "float", 100.0, 5, "obj-40", "number", "float", 0.699999988079071, 5, "obj-38", "number", "float", 6.0, 5, "obj-46", "number", "int", 1, 5, "obj-47", "number", "int", 15000, 5, "obj-55", "number", "int", 350 ]
                        },
                        {
                            "number": 16,
                            "data": [ 5, "obj-67", "number", "int", 32, 5, "obj-42", "number", "float", 33.0, 5, "obj-41", "number", "float", 888.0, 5, "obj-40", "number", "float", 1.5, 5, "obj-38", "number", "float", 1.5, 5, "obj-46", "number", "int", 1, 5, "obj-47", "number", "int", 15000, 5, "obj-55", "number", "int", 350, 5, "obj-25", "number", "float", 0.025000000372529 ]
                        },
                        {
                            "number": 17,
                            "data": [ 5, "obj-67", "number", "int", 8, 5, "obj-42", "number", "float", 50.0, 5, "obj-41", "number", "float", 8000.0, 5, "obj-40", "number", "float", 0.0, 5, "obj-38", "number", "float", 0.1, 5, "obj-46", "number", "int", 100, 5, "obj-47", "number", "int", 2000, 5, "obj-55", "number", "int", 3 ]
                        },
                        {
                            "number": 18,
                            "data": [ 5, "obj-67", "number", "int", 12, 5, "obj-42", "number", "float", 4800.0, 5, "obj-41", "number", "float", 720.0, 5, "obj-40", "number", "float", 0.800000011920929, 5, "obj-38", "number", "float", 0.100000001490116, 5, "obj-46", "number", "int", 33, 5, "obj-47", "number", "int", 2000, 5, "obj-55", "number", "int", 3, 5, "obj-25", "number", "float", 0.019999999552965 ]
                        },
                        {
                            "number": 19,
                            "data": [ 5, "obj-67", "number", "int", 32, 5, "obj-42", "number", "float", 3.5, 5, "obj-41", "number", "float", 12000.0, 5, "obj-40", "number", "float", 0.0, 5, "obj-38", "number", "float", 0.600000023841858, 5, "obj-46", "number", "int", 30, 5, "obj-47", "number", "int", 1500, 5, "obj-55", "number", "int", 1, 5, "obj-25", "number", "float", 0.03125 ]
                        },
                        {
                            "number": 20,
                            "data": [ 5, "obj-67", "number", "int", 16, 5, "obj-42", "number", "float", 50.0, 5, "obj-41", "number", "float", 8000.0, 5, "obj-40", "number", "float", 0.001, 5, "obj-38", "number", "float", 0.09, 5, "obj-46", "number", "int", 10, 5, "obj-47", "number", "int", 1500, 5, "obj-55", "number", "int", 50000 ]
                        },
                        {
                            "number": 21,
                            "data": [ 5, "obj-67", "number", "int", 5, 5, "obj-42", "number", "float", 100.0, 5, "obj-41", "number", "float", 7000.0, 5, "obj-40", "number", "float", 0.5, 5, "obj-38", "number", "float", 0.119999997317791, 5, "obj-46", "number", "int", 2, 5, "obj-47", "number", "int", 6000, 5, "obj-55", "number", "int", 22, 5, "obj-25", "number", "float", 0.200000002980232 ]
                        },
                        {
                            "number": 22,
                            "data": [ 5, "obj-67", "number", "int", 20, 5, "obj-42", "number", "float", 75.0, 5, "obj-41", "number", "float", 150.0, 5, "obj-40", "number", "float", 0.009999999776483, 5, "obj-38", "number", "float", 0.03999999910593, 5, "obj-46", "number", "int", 3, 5, "obj-47", "number", "int", 6000, 5, "obj-55", "number", "int", 350 ]
                        },
                        {
                            "number": 23,
                            "data": [ 5, "obj-67", "number", "int", 12, 5, "obj-42", "number", "float", 75.0, 5, "obj-41", "number", "float", 150.0, 5, "obj-40", "number", "float", 0.300000011920929, 5, "obj-38", "number", "float", 1.600000023841858, 5, "obj-46", "number", "int", 1, 5, "obj-47", "number", "int", 10000, 5, "obj-55", "number", "int", 350 ]
                        },
                        {
                            "number": 24,
                            "data": [ 5, "obj-67", "number", "int", 3, 5, "obj-42", "number", "float", 20000.0, 5, "obj-41", "number", "float", 10000.0, 5, "obj-40", "number", "float", 0.050000000745058, 5, "obj-38", "number", "float", 0.125, 5, "obj-46", "number", "int", 5, 5, "obj-47", "number", "int", 3000, 5, "obj-55", "number", "int", 1, 5, "obj-25", "number", "float", 0.333333343267441 ]
                        }
                    ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-50",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 273.0, 520.0, 54.0, 20.0 ],
                    "text": "duration"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-49",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 79.0, 500.0, 51.0, 20.0 ],
                    "text": "start"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-47",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 226.0, 521.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-46",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 79.0, 521.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-39",
                    "maxclass": "newobj",
                    "numinlets": 6,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 214.0, 568.0, 110.0, 22.0 ],
                    "text": "pack 1 0 0 0 0 -0.8"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-37",
                    "maxclass": "newobj",
                    "numinlets": 6,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 65.0, 568.0, 113.0, 22.0 ],
                    "text": "pack 4 0 0 0 0 0.75"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "format": 6,
                    "id": "obj-38",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 594.0, 611.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "format": 6,
                    "id": "obj-40",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 542.0, 611.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "format": 6,
                    "id": "obj-41",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 481.0, 612.0, 52.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "format": 6,
                    "id": "obj-42",
                    "maxclass": "flonum",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 429.0, 612.0, 50.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-43",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 137.0, 600.0, 43.0, 20.0 ],
                    "text": "phase"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-15",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 130.0, 619.0, 32.5, 22.0 ],
                    "text": "0"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-45",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 562.0, 593.0, 85.0, 20.0 ],
                    "text": "resonator dur."
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-44",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 436.0, 593.0, 89.0, 20.0 ],
                    "text": "resonator freq."
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "hidden": 1,
                    "id": "obj-52",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 498.0, 460.0, 72.0, 22.0 ],
                    "text": "loadmess 1"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-53",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 331.0, 617.0, 58.0, 22.0 ],
                    "text": "target $1"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-54",
                    "maxclass": "newobj",
                    "numinlets": 4,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 526.0, 638.0, 121.0, 22.0 ],
                    "text": "vs.between 0. 0."
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-56",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "int", "int", "int" ],
                    "patching_rect": [ 334.0, 516.0, 63.0, 22.0 ],
                    "text": "t i i i"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-60",
                    "maxclass": "newobj",
                    "numinlets": 4,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 392.0, 638.0, 130.0, 22.0 ],
                    "text": "vs.between 0. 0."
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-62",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "bang", "" ],
                    "patching_rect": [ 392.0, 567.0, 36.0, 22.0 ],
                    "text": "sel 0"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-63",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 334.0, 567.0, 36.0, 22.0 ],
                    "text": "pack"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-65",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 351.0, 540.0, 77.5, 22.0 ],
                    "text": ">"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-66",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 396.0, 457.0, 69.0, 33.0 ],
                    "text": "number of resonators"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-67",
                    "maxclass": "number",
                    "maximum": 40,
                    "minimum": 1,
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 410.0, 489.0, 42.0, 22.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-68",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 258.0, 617.0, 71.0, 22.0 ],
                    "text": "mute $1 $2"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-78",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 3,
                    "outlettype": [ "bang", "bang", "int" ],
                    "patching_rect": [ 241.0, 486.0, 112.0, 22.0 ],
                    "text": "uzi 40"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-79",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "bang" ],
                    "patching_rect": [ 214.0, 592.0, 47.0, 22.0 ],
                    "text": "curve~"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-80",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 65.0, 702.0, 32.5, 22.0 ],
                    "text": "*~"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-81",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "bang" ],
                    "patching_rect": [ 65.0, 592.0, 47.0, 22.0 ],
                    "text": "curve~"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-4",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 65.0, 648.0, 54.0, 22.0 ],
                    "text": "phasor~"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-83",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 69.0, 1011.0, 74.0, 22.0 ],
                    "text": "startwindow"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-86",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "patching_rect": [ 179.0, 1096.0, 55.0, 22.0 ],
                    "text": "dac~ 1 2"
                }
            },
            {
                "box": {
                    "id": "obj-3",
                    "interpinlet": 1,
                    "maxclass": "gain~",
                    "multichannelvariant": 0,
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "signal", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 179.0, 984.0, 21.0, 81.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 7.0, 15.0, 21.0, 76.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-6",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 92.0, 1036.0, 50.0, 22.0 ],
                    "text": "stop"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 12.0,
                    "id": "obj-87",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 258.0, 662.0, 287.0, 22.0 ],
                    "text": "poly~ p_resonators~ 40"
                }
            },
            {
                "box": {
                    "id": "obj-30",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 0,
                    "patching_rect": [ 658.0, 316.0, 49.0, 22.0 ],
                    "text": "noteout"
                }
            },
            {
                "box": {
                    "id": "obj-31",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 773.0, 217.0, 39.0, 22.0 ],
                    "text": "!- 180"
                }
            },
            {
                "box": {
                    "id": "obj-32",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 773.0, 137.0, 79.0, 22.0 ],
                    "text": "drunk 100 10"
                }
            },
            {
                "box": {
                    "id": "obj-33",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 2,
                    "outlettype": [ "float", "float" ],
                    "patching_rect": [ 658.0, 268.0, 193.60000610351562, 22.0 ],
                    "text": "makenote 120 100"
                }
            },
            {
                "box": {
                    "id": "obj-10",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 732.0, 217.0, 32.0, 22.0 ],
                    "text": "+ 48"
                }
            },
            {
                "box": {
                    "id": "obj-9",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 697.0, 217.0, 32.0, 22.0 ],
                    "text": "+ 36"
                }
            },
            {
                "box": {
                    "id": "obj-8",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 658.0, 217.0, 32.0, 22.0 ],
                    "text": "+ 24"
                }
            },
            {
                "box": {
                    "id": "obj-7",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 697.0, 183.0, 54.0, 22.0 ],
                    "text": "bucket 2"
                }
            },
            {
                "box": {
                    "id": "obj-34",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 697.0, 137.0, 69.0, 22.0 ],
                    "text": "drunk 48 -3"
                }
            },
            {
                "box": {
                    "id": "obj-35",
                    "maxclass": "nslider",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "int", "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 877.0, 137.0, 58.181814713911635, 153.59999084472656 ]
                }
            },
            {
                "box": {
                    "id": "obj-36",
                    "maxclass": "toggle",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 697.0, 21.0, 63.0, 63.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-1",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 697.0, 99.0, 63.0, 22.0 ],
                    "text": "metro 100"
                }
            },
            {
                "box": {
                    "fontname": "Trebuchet MS",
                    "fontsize": 12.0,
                    "id": "obj-61",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 120.5, 3.0, 59.0, 22.0 ],
                    "text": "loadbang"
                }
            },
            {
                "box": {
                    "fontname": "Trebuchet MS",
                    "fontsize": 12.0,
                    "id": "obj-77",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "clear" ],
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
                        "rect": [ 34.0, 79.0, 667.0, 547.0 ],
                        "boxes": [
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-10",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 148.0, 212.0, 52.0, 22.0 ],
                                    "text": "select..."
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 12.0,
                                    "id": "obj-8",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 3,
                                    "outlettype": [ "print", "bang", "clear" ],
                                    "patching_rect": [ 51.0, 76.0, 80.0, 22.0 ],
                                    "text": "t print b clear"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 10.0,
                                    "id": "obj-1",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "" ],
                                    "patching_rect": [ 90.0, 171.0, 56.0, 20.0 ],
                                    "text": "route port"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 10.0,
                                    "id": "obj-3",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 90.0, 358.0, 111.0, 20.0 ],
                                    "text": "prepend append"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 10.0,
                                    "id": "obj-4",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 2,
                                    "outlettype": [ "int", "" ],
                                    "patching_rect": [ 64.0, 115.0, 36.0, 20.0 ],
                                    "text": "serial"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Arial",
                                    "fontsize": 10.0,
                                    "id": "obj-5",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 31.0, 271.0, 25.0, 20.0 ],
                                    "text": "iter"
                                }
                            },
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-6",
                                    "index": 1,
                                    "maxclass": "inlet",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 64.0, 45.0, 15.0, 15.0 ]
                                }
                            },
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-7",
                                    "index": 1,
                                    "maxclass": "outlet",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 148.0, 432.0, 15.0, 15.0 ]
                                }
                            }
                        ],
                        "lines": [
                            {
                                "patchline": {
                                    "destination": [ "obj-5", 0 ],
                                    "source": [ "obj-1", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-3", 0 ],
                                    "midpoints": [ 106.0, 260.0 ],
                                    "source": [ "obj-10", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-7", 0 ],
                                    "source": [ "obj-3", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-1", 0 ],
                                    "source": [ "obj-4", 1 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-3", 0 ],
                                    "source": [ "obj-5", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-8", 0 ],
                                    "source": [ "obj-6", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-10", 0 ],
                                    "midpoints": [ 229.0, 217.0 ],
                                    "source": [ "obj-8", 1 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-4", 0 ],
                                    "source": [ "obj-8", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-7", 0 ],
                                    "midpoints": [ 364.0, 251.0 ],
                                    "source": [ "obj-8", 2 ]
                                }
                            }
                        ]
                    },
                    "patching_rect": [ 120.5, 62.0, 61.0, 22.0 ],
                    "text": "p devices"
                }
            },
            {
                "box": {
                    "fontname": "Trebuchet MS",
                    "fontsize": 12.0,
                    "id": "obj-64",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 120.5, 32.0177, 48.0, 22.0 ],
                    "presentation": 1,
                    "presentation_rect": [ 84.5, 109.214874, 48.0, 22.0 ],
                    "text": "update"
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-16",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
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
                        "rect": [ 519.0, 114.0, 213.0, 363.0 ],
                        "default_fontname": "Verdana",
                        "boxes": [
                            {
                                "box": {
                                    "id": "obj-1",
                                    "maxclass": "button",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "bang" ],
                                    "parameter_enable": 0,
                                    "patching_rect": [ 114.0, 142.0, 15.0, 15.0 ]
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Verdana",
                                    "fontsize": 9.0,
                                    "id": "obj-2",
                                    "maxclass": "message",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 114.0, 168.0, 33.0, 15.0 ],
                                    "text": "clear"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Verdana",
                                    "fontsize": 9.0,
                                    "id": "obj-3",
                                    "linecount": 2,
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 24.0, 167.0, 78.0, 28.0 ],
                                    "text": "prepend append"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Verdana",
                                    "fontsize": 9.0,
                                    "id": "obj-4",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "" ],
                                    "patching_rect": [ 24.0, 116.0, 47.0, 17.0 ],
                                    "text": "zl iter 1"
                                }
                            },
                            {
                                "box": {
                                    "fontname": "Verdana",
                                    "fontsize": 9.0,
                                    "id": "obj-5",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 2,
                                    "outlettype": [ "", "" ],
                                    "patching_rect": [ 24.0, 76.0, 56.0, 17.0 ],
                                    "text": "route port"
                                }
                            },
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-6",
                                    "index": 1,
                                    "maxclass": "outlet",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 24.0, 246.0, 16.0, 16.0 ]
                                }
                            },
                            {
                                "box": {
                                    "comment": "",
                                    "id": "obj-7",
                                    "index": 1,
                                    "maxclass": "inlet",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 24.0, 32.0, 16.0, 16.0 ]
                                }
                            }
                        ],
                        "lines": [
                            {
                                "patchline": {
                                    "destination": [ "obj-2", 0 ],
                                    "source": [ "obj-1", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-6", 0 ],
                                    "source": [ "obj-2", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-6", 0 ],
                                    "source": [ "obj-3", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-3", 0 ],
                                    "source": [ "obj-4", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-1", 0 ],
                                    "order": 0,
                                    "source": [ "obj-5", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-4", 0 ],
                                    "order": 1,
                                    "source": [ "obj-5", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-5", 0 ],
                                    "source": [ "obj-7", 0 ]
                                }
                            }
                        ]
                    },
                    "patching_rect": [ 204.5, 172.0, 72.0, 19.0 ],
                    "saved_object_attributes": {
                        "fontname": "Verdana"
                    },
                    "text": "p createMenu"
                }
            },
            {
                "box": {
                    "bgcolor": [ 0.635294, 0.803922, 0.490196, 1.0 ],
                    "bgfillcolor_angle": 270.0,
                    "bgfillcolor_color": [ 0.635294, 0.803922, 0.490196, 1.0 ],
                    "bgfillcolor_color1": [ 0.376471, 0.384314, 0.4, 1.0 ],
                    "bgfillcolor_color2": [ 0.290196, 0.309804, 0.301961, 1.0 ],
                    "bgfillcolor_proportion": 0.39,
                    "bgfillcolor_type": "color",
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-23",
                    "items": [ "select...", ",", "BLTH", ",", "usbmodem14101", ",", "Bluetooth-Incoming-Port", ",", "HookeVerse", ",", "macMacBookPro", ",", "NS-83", ",", "F4", ",", "BigAirpod", ",", "usbmodem14201" ],
                    "labelclick": 1,
                    "maxclass": "umenu",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "int", "", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 120.5, 94.0, 149.0, 19.0 ],
                    "textcolor": [ 0.0, 0.0, 0.0, 1.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-24",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 185.5, 119.0, 68.0, 19.0 ],
                    "text": "prepend port"
                }
            },
            {
                "box": {
                    "id": "obj-26",
                    "maxclass": "toggle",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 31.5, 82.0, 19.0, 19.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-27",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 31.5, 107.0, 50.0, 19.0 ],
                    "text": "metro 33"
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-11",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 31.5, 277.0, 64.0, 19.0 ],
                    "text": "fromsymbol"
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-12",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "int" ],
                    "patching_rect": [ 31.5, 235.0, 40.0, 19.0 ],
                    "text": "itoa"
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-13",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "", "" ],
                    "patching_rect": [ 31.5, 210.0, 71.0, 19.0 ],
                    "text": "zl group 1000"
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-14",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 3,
                    "outlettype": [ "bang", "bang", "" ],
                    "patching_rect": [ 31.5, 172.0, 52.0, 19.0 ],
                    "text": "sel 10 13"
                }
            },
            {
                "box": {
                    "fontname": "Verdana",
                    "fontsize": 9.0,
                    "id": "obj-28",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "int", "" ],
                    "patching_rect": [ 31.5, 146.0, 103.0, 19.0 ],
                    "text": "serial f 115200 8 1 0"
                }
            }
        ],
        "lines": [
            {
                "patchline": {
                    "destination": [ "obj-32", 0 ],
                    "order": 0,
                    "source": [ "obj-1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-34", 0 ],
                    "order": 1,
                    "source": [ "obj-1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-33", 0 ],
                    "source": [ "obj-10", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-5", 1 ],
                    "source": [ "obj-11", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-11", 0 ],
                    "order": 1,
                    "source": [ "obj-12", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-88", 0 ],
                    "order": 0,
                    "source": [ "obj-12", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-12", 0 ],
                    "source": [ "obj-13", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-13", 0 ],
                    "midpoints": [ 74.0, 203.0, 41.0, 203.0 ],
                    "source": [ "obj-14", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-13", 0 ],
                    "source": [ "obj-14", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 1 ],
                    "source": [ "obj-15", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-23", 0 ],
                    "midpoints": [ 214.0, 201.0, 288.0, 201.0, 288.0, 87.0, 130.0, 87.0 ],
                    "source": [ "obj-16", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-78", 0 ],
                    "source": [ "obj-17", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-83", 0 ],
                    "order": 1,
                    "source": [ "obj-18", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-91", 0 ],
                    "order": 0,
                    "source": [ "obj-18", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-22", 0 ],
                    "source": [ "obj-19", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-51", 0 ],
                    "source": [ "obj-21", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-19", 0 ],
                    "source": [ "obj-22", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-21", 0 ],
                    "order": 0,
                    "source": [ "obj-22", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-94", 0 ],
                    "order": 1,
                    "source": [ "obj-22", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-24", 0 ],
                    "source": [ "obj-23", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-28", 0 ],
                    "midpoints": [ 195.0, 140.0, 41.0, 140.0 ],
                    "source": [ "obj-24", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-71", 1 ],
                    "midpoints": [ 74.5, 926.0, 202.0, 926.0 ],
                    "source": [ "obj-25", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-27", 0 ],
                    "source": [ "obj-26", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-28", 0 ],
                    "source": [ "obj-27", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 0 ],
                    "source": [ "obj-28", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-16", 0 ],
                    "source": [ "obj-28", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-25", 0 ],
                    "source": [ "obj-29", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-85", 0 ],
                    "source": [ "obj-3", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-86", 0 ],
                    "source": [ "obj-3", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-33", 1 ],
                    "source": [ "obj-31", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-31", 0 ],
                    "order": 1,
                    "source": [ "obj-32", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-33", 2 ],
                    "order": 0,
                    "source": [ "obj-32", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-30", 1 ],
                    "midpoints": [ 842.1000061035156, 303.1999969482422, 682.5, 303.1999969482422 ],
                    "order": 1,
                    "source": [ "obj-33", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-30", 0 ],
                    "order": 1,
                    "source": [ "obj-33", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-35", 1 ],
                    "midpoints": [ 842.1000061035156, 291.1999969482422, 863.3999938964844, 291.1999969482422, 863.3999938964844, 123.19999694824219, 925.6818147139116, 123.19999694824219 ],
                    "order": 0,
                    "source": [ "obj-33", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-35", 0 ],
                    "midpoints": [ 667.5, 300.1999969482422, 863.3999938964844, 300.1999969482422, 863.3999938964844, 132.1999969482422, 886.5, 132.1999969482422 ],
                    "order": 0,
                    "source": [ "obj-33", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-7", 0 ],
                    "order": 0,
                    "source": [ "obj-34", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-8", 0 ],
                    "order": 1,
                    "source": [ "obj-34", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-1", 0 ],
                    "source": [ "obj-36", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-81", 0 ],
                    "source": [ "obj-37", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-54", 2 ],
                    "source": [ "obj-38", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-79", 0 ],
                    "source": [ "obj-39", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-80", 0 ],
                    "source": [ "obj-4", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-54", 1 ],
                    "source": [ "obj-40", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-60", 2 ],
                    "source": [ "obj-41", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-60", 1 ],
                    "source": [ "obj-42", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-59", 1 ],
                    "source": [ "obj-46", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-37", 4 ],
                    "order": 1,
                    "source": [ "obj-47", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-39", 4 ],
                    "order": 0,
                    "source": [ "obj-47", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-71", 0 ],
                    "source": [ "obj-48", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-71", 0 ],
                    "source": [ "obj-48", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-3", 0 ],
                    "hidden": 1,
                    "source": [ "obj-51", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-70", 0 ],
                    "hidden": 1,
                    "source": [ "obj-51", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-51", 0 ],
                    "hidden": 1,
                    "source": [ "obj-52", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-87", 0 ],
                    "source": [ "obj-53", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-87", 2 ],
                    "source": [ "obj-54", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-37", 3 ],
                    "source": [ "obj-55", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-53", 0 ],
                    "midpoints": [ 387.5, 602.0, 340.5, 602.0 ],
                    "source": [ "obj-56", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-63", 0 ],
                    "source": [ "obj-56", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-65", 0 ],
                    "source": [ "obj-56", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-37", 0 ],
                    "source": [ "obj-59", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-86", 0 ],
                    "midpoints": [ 101.5, 1087.5, 188.5, 1087.5 ],
                    "source": [ "obj-6", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-87", 1 ],
                    "source": [ "obj-60", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-64", 0 ],
                    "source": [ "obj-61", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-54", 0 ],
                    "midpoints": [ 401.5, 592.0, 535.5, 592.0 ],
                    "order": 0,
                    "source": [ "obj-62", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-60", 0 ],
                    "midpoints": [ 401.5, 592.0, 401.5, 592.0 ],
                    "order": 1,
                    "source": [ "obj-62", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-68", 0 ],
                    "source": [ "obj-63", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-77", 0 ],
                    "source": [ "obj-64", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-62", 0 ],
                    "order": 0,
                    "source": [ "obj-65", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-63", 1 ],
                    "order": 1,
                    "source": [ "obj-65", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-65", 1 ],
                    "order": 1,
                    "source": [ "obj-67", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-72", 0 ],
                    "midpoints": [ 419.5, 512.5, 433.5, 512.5 ],
                    "order": 0,
                    "source": [ "obj-67", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-87", 0 ],
                    "source": [ "obj-68", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 0 ],
                    "source": [ "obj-69", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-10", 0 ],
                    "source": [ "obj-7", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-9", 0 ],
                    "source": [ "obj-7", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-17", 0 ],
                    "hidden": 1,
                    "source": [ "obj-70", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-3", 0 ],
                    "order": 1,
                    "source": [ "obj-71", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-85", 0 ],
                    "order": 0,
                    "source": [ "obj-71", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-29", 0 ],
                    "source": [ "obj-73", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-17", 0 ],
                    "source": [ "obj-74", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-86", 0 ],
                    "source": [ "obj-76", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-23", 0 ],
                    "source": [ "obj-77", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-15", 0 ],
                    "midpoints": [ 297.0, 563.0, 139.5, 563.0 ],
                    "order": 1,
                    "source": [ "obj-78", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-39", 0 ],
                    "midpoints": [ 297.0, 517.0, 223.5, 517.0 ],
                    "order": 0,
                    "source": [ "obj-78", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-56", 0 ],
                    "source": [ "obj-78", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-59", 0 ],
                    "midpoints": [ 297.0, 517.0, 74.5, 517.0 ],
                    "order": 2,
                    "source": [ "obj-78", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-80", 1 ],
                    "source": [ "obj-79", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-33", 0 ],
                    "source": [ "obj-8", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-87", 0 ],
                    "midpoints": [ 74.5, 711.0, 237.0, 711.0, 237.0, 646.0, 267.5, 646.0 ],
                    "source": [ "obj-80", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-69", 0 ],
                    "source": [ "obj-81", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-86", 0 ],
                    "midpoints": [ 78.5, 1075.0, 188.5, 1075.0 ],
                    "source": [ "obj-83", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-86", 1 ],
                    "source": [ "obj-85", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-71", 0 ],
                    "source": [ "obj-87", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-22", 0 ],
                    "source": [ "obj-88", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-33", 0 ],
                    "source": [ "obj-9", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-3", 0 ],
                    "source": [ "obj-91", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-95", 0 ],
                    "source": [ "obj-94", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-48", 0 ],
                    "source": [ "obj-95", 0 ]
                }
            }
        ],
        "autosave": 0
    }
}