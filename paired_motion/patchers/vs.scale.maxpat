{
	"patcher" : 	{
		"fileversion" : 1,
		"rect" : [ 219.0, 44.0, 460.0, 272.0 ],
		"bglocked" : 0,
		"defrect" : [ 219.0, 44.0, 460.0, 272.0 ],
		"openrect" : [ 0.0, 0.0, 0.0, 0.0 ],
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 0,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 0,
		"toolbarvisible" : 1,
		"boxanimatetime" : 200,
		"imprint" : 0,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"boxes" : [ 			{
				"box" : 				{
					"maxclass" : "message",
					"text" : ";\rmax launchbrowser http://www.giri.it",
					"linecount" : 2,
					"hidden" : 1,
					"outlettype" : [ "" ],
					"id" : "obj-15",
					"fontsize" : 12.0,
					"numinlets" : 2,
					"numoutlets" : 1,
					"patching_rect" : [ 293.0, 277.0, 203.0, 32.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "ubutton",
					"outlettype" : [ "bang", "bang", "", "int" ],
					"id" : "obj-16",
					"handoff" : "",
					"numinlets" : 1,
					"numoutlets" : 4,
					"patching_rect" : [ 371.0, 250.0, 65.0, 21.0 ]
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "message",
					"text" : ";\rmax launchbrowser http://www.virtual-sound.com",
					"linecount" : 2,
					"hidden" : 1,
					"outlettype" : [ "" ],
					"id" : "obj-17",
					"fontsize" : 12.0,
					"numinlets" : 2,
					"numoutlets" : 1,
					"patching_rect" : [ 19.0, 277.0, 272.0, 32.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "ubutton",
					"outlettype" : [ "bang", "bang", "", "int" ],
					"id" : "obj-18",
					"handoff" : "",
					"numinlets" : 1,
					"numoutlets" : 4,
					"patching_rect" : [ 140.0, 250.0, 130.0, 20.0 ]
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "comment",
					"text" : "VirtualSound Macros - www.virtual-sound.com - (c) Maurizio Giri - www.giri.it",
					"textcolor" : [ 0.168627, 0.305882, 0.721569, 1.0 ],
					"id" : "obj-19",
					"frgb" : [ 0.168627, 0.305882, 0.721569, 1.0 ],
					"fontsize" : 12.0,
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 18.0, 250.0, 419.0, 20.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "newobj",
					"text" : "1",
					"outlettype" : [ "int" ],
					"id" : "obj-1",
					"fontsize" : 12.0,
					"numinlets" : 2,
					"numoutlets" : 1,
					"patching_rect" : [ 308.0, 85.0, 32.5, 20.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "newobj",
					"text" : "sel 0",
					"outlettype" : [ "bang", "" ],
					"id" : "obj-2",
					"fontsize" : 12.0,
					"numinlets" : 2,
					"numoutlets" : 2,
					"patching_rect" : [ 308.0, 59.0, 54.0, 20.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "newobj",
					"text" : "loadmess #5",
					"outlettype" : [ "" ],
					"id" : "obj-3",
					"fontsize" : 12.0,
					"numinlets" : 1,
					"numoutlets" : 1,
					"patching_rect" : [ 308.0, 31.0, 79.0, 20.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "inlet",
					"outlettype" : [ "" ],
					"id" : "obj-4",
					"numinlets" : 0,
					"numoutlets" : 1,
					"patching_rect" : [ 268.0, 53.0, 25.0, 25.0 ],
					"comment" : "exp"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "inlet",
					"outlettype" : [ "" ],
					"id" : "obj-5",
					"numinlets" : 0,
					"numoutlets" : 1,
					"patching_rect" : [ 238.0, 53.0, 25.0, 25.0 ],
					"comment" : "max out"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "inlet",
					"outlettype" : [ "" ],
					"id" : "obj-6",
					"numinlets" : 0,
					"numoutlets" : 1,
					"patching_rect" : [ 210.0, 53.0, 25.0, 25.0 ],
					"comment" : "min out"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "inlet",
					"outlettype" : [ "" ],
					"id" : "obj-7",
					"numinlets" : 0,
					"numoutlets" : 1,
					"patching_rect" : [ 120.0, 53.0, 25.0, 25.0 ],
					"comment" : "max in"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "inlet",
					"outlettype" : [ "" ],
					"id" : "obj-8",
					"numinlets" : 0,
					"numoutlets" : 1,
					"patching_rect" : [ 86.0, 53.0, 25.0, 25.0 ],
					"comment" : "min in"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "inlet",
					"outlettype" : [ "" ],
					"id" : "obj-9",
					"numinlets" : 0,
					"numoutlets" : 1,
					"patching_rect" : [ 52.0, 53.0, 25.0, 25.0 ],
					"comment" : "float"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "outlet",
					"annotation" : "scaled output",
					"id" : "obj-10",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 52.0, 198.0, 25.0, 25.0 ],
					"comment" : ""
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "newobj",
					"text" : "scale 0. 1. #3 #4",
					"outlettype" : [ "" ],
					"id" : "obj-11",
					"fontsize" : 12.0,
					"numinlets" : 6,
					"numoutlets" : 1,
					"patching_rect" : [ 52.0, 159.0, 99.0, 20.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "newobj",
					"text" : "pow 0.",
					"outlettype" : [ "float" ],
					"id" : "obj-12",
					"fontsize" : 12.0,
					"numinlets" : 2,
					"numoutlets" : 1,
					"patching_rect" : [ 52.0, 128.0, 46.0, 20.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "newobj",
					"text" : "scale #1 #2 0. 1.",
					"outlettype" : [ "" ],
					"id" : "obj-13",
					"fontsize" : 12.0,
					"numinlets" : 6,
					"numoutlets" : 1,
					"patching_rect" : [ 52.0, 93.0, 99.0, 20.0 ],
					"fontname" : "Arial"
				}

			}
, 			{
				"box" : 				{
					"maxclass" : "comment",
					"text" : "create an exponential curve independent of the output range",
					"linecount" : 2,
					"id" : "obj-14",
					"fontsize" : 12.0,
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 82.0, 188.0, 320.0, 34.0 ],
					"fontname" : "Arial"
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"source" : [ "obj-18", 0 ],
					"destination" : [ "obj-17", 0 ],
					"hidden" : 1,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-16", 0 ],
					"destination" : [ "obj-15", 0 ],
					"hidden" : 1,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-9", 0 ],
					"destination" : [ "obj-13", 0 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-13", 0 ],
					"destination" : [ "obj-12", 0 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-12", 0 ],
					"destination" : [ "obj-11", 0 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-11", 0 ],
					"destination" : [ "obj-10", 0 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-4", 0 ],
					"destination" : [ "obj-12", 1 ],
					"hidden" : 0,
					"color" : [ 1.0, 0.360784, 0.682353, 1.0 ],
					"midpoints" : [ 277.5, 117.0, 88.5, 117.0 ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-1", 0 ],
					"destination" : [ "obj-12", 1 ],
					"hidden" : 0,
					"midpoints" : [ 317.5, 121.0, 88.5, 121.0 ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-2", 1 ],
					"destination" : [ "obj-12", 1 ],
					"hidden" : 0,
					"midpoints" : [ 352.5, 121.0, 88.5, 121.0 ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-8", 0 ],
					"destination" : [ "obj-13", 1 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-7", 0 ],
					"destination" : [ "obj-13", 2 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-6", 0 ],
					"destination" : [ "obj-11", 3 ],
					"hidden" : 0,
					"midpoints" : [ 219.5, 125.0, 109.5, 125.0 ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-5", 0 ],
					"destination" : [ "obj-11", 4 ],
					"hidden" : 0,
					"midpoints" : [ 247.5, 140.0, 125.5, 140.0 ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-3", 0 ],
					"destination" : [ "obj-2", 0 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
, 			{
				"patchline" : 				{
					"source" : [ "obj-2", 0 ],
					"destination" : [ "obj-1", 0 ],
					"hidden" : 0,
					"midpoints" : [  ]
				}

			}
 ]
	}

}
