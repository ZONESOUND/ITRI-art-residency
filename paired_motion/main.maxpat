{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 9,
			"minor" : 1,
			"revision" : 4,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 60.0, 100.0, 900.0, 700.0 ],
		"gridsize" : [ 15.0, 15.0 ],
		"boxes" : [
			{
				"box" : 				{
					"id" : "obj-header",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 20.0, 800.0, 22.0 ],
					"text" : "PAIRED MOTION — main patch (skeleton). bootstrap.js auto-installs npm deps and loads auto_detect.js on patch load.",
					"fontsize" : 13.0
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-section1",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 60.0, 400.0, 22.0 ],
					"text" : "── 1. Bootstrap + auto-detect entry point ──"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-bootstrap",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 20.0, 90.0, 320.0, 22.0 ],
					"text" : "node.script bootstrap.js @autostart 1"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-print-bootstrap",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 360.0, 90.0, 200.0, 22.0 ],
					"text" : "print BOOTSTRAP @popup 1"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-section2",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 140.0, 400.0, 22.0 ],
					"text" : "── 2. Sensor abstractions (TODO) ──"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-todo-tof",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 170.0, 600.0, 22.0 ],
					"text" : "TODO: bpatcher abstractions/sub_auto_detect.maxpat → fan out tof / pressure / piezo / piezo_stream"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-todo-sensors",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 200.0, 700.0, 22.0 ],
					"text" : "TODO: bpatcher abstractions/sub_tof.maxpat / sub_pressure.maxpat / sub_piezo.maxpat (one inlet per sensor)"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-section3",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 250.0, 400.0, 22.0 ],
					"text" : "── 3. Audio output (TODO) ──"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-todo-audio",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 280.0, 600.0, 22.0 ],
					"text" : "TODO: mixer + dac~"
				}
			}
,
			{
				"box" : 				{
					"id" : "obj-help",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 20.0, 600.0, 850.0, 80.0 ],
					"text" : "First-time use:\n  1. Plug in all 3 ESP32s before opening this patch\n  2. Open this patch — bootstrap.js auto-installs npm deps if needed (~30-60s on first run)\n  3. After bootstrap completes, auto_detect.js runs and finds the three sensors\n  4. (TODO) Build sensor abstractions to actually do something with the data"
				}
			}

 ],
		"lines" : [
			{
				"patchline" : 				{
					"destination" : [ "obj-print-bootstrap", 0 ],
					"source" : [ "obj-bootstrap", 0 ]
				}
			}

 ]
	}

}
