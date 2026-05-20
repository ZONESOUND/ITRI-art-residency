{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 9,
			"minor" : 1,
			"revision" : 1,
			"architecture" : "x64",
			"modernui" : 1
		},
		"classnamespace" : "box",
		"rect" : [ 100.0, 100.0, 720.0, 360.0 ],
		"boxes" : [
			{
				"box" : 				{
					"fontsize" : 13.0,
					"id" : "obj-header",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 20.0, 680.0, 25.0 ],
					"text" : "VISUALIZATION: 從 sub_auto_detect 接 r tof，餵給 node.script，瀏覽器開 http://localhost:8080"
				}
			},
			{
				"box" : 				{
					"id" : "obj-hint1",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 55.0, 680.0, 23.0 ],
					"text" : "啟動順序：① 等 sub_auto_detect 掃描完三顆 ESP32  ② 點 [script start]  ③ 瀏覽器開 :8080"
				}
			},
			{
				"box" : 				{
					"id" : "obj-start",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 20.0, 90.0, 80.0, 22.0 ],
					"text" : "script start"
				}
			},
			{
				"box" : 				{
					"id" : "obj-stop",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 110.0, 90.0, 80.0, 22.0 ],
					"text" : "script stop"
				}
			},
			{
				"box" : 				{
					"id" : "obj-restart",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 200.0, 90.0, 90.0, 22.0 ],
					"text" : "script restart"
				}
			},
			{
				"box" : 				{
					"id" : "obj-rtof",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 20.0, 140.0, 50.0, 22.0 ],
					"text" : "r tof"
				}
			},
			{
				"box" : 				{
					"id" : "obj-rtofhint",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 75.0, 142.0, 360.0, 20.0 ],
					"text" : "↑ 接 sub_auto_detect 內部 [s tof]（裸 list，無 /tof 前綴）"
				}
			},
			{
				"box" : 				{
					"id" : "obj-node",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "int" ],
					"patching_rect" : [ 20.0, 190.0, 260.0, 22.0 ],
					"text" : "node.script ../visualization/server.js"
				}
			},
			{
				"box" : 				{
					"id" : "obj-nodehint",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 285.0, 192.0, 350.0, 20.0 ],
					"text" : "↑ server.js 註冊 'list' handler，直接吃裸 list"
				}
			},
			{
				"box" : 				{
					"id" : "obj-console",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 240.0, 110.0, 22.0 ],
					"text" : "print viz"
				}
			},
			{
				"box" : 				{
					"id" : "obj-consolehint",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 135.0, 242.0, 500.0, 20.0 ],
					"text" : "↑ node.script 的 stdout / errors 會印到 Max console（prefix \"viz:\"）"
				}
			}
		],
		"lines" : [
			{
				"patchline" : 				{
					"destination" : [ "obj-node", 0 ],
					"source" : [ "obj-rtof", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-node", 0 ],
					"source" : [ "obj-start", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-node", 0 ],
					"source" : [ "obj-stop", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-node", 0 ],
					"source" : [ "obj-restart", 0 ]
				}
			},
			{
				"patchline" : 				{
					"destination" : [ "obj-console", 0 ],
					"source" : [ "obj-node", 0 ]
				}
			}
		]
	}
}
