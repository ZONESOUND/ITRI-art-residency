{
	"name" : "paired_motion",
	"version" : 1,
	"creationdate" : 0,
	"modificationdate" : 0,
	"viewrect" : [ 60.0, 100.0, 320.0, 600.0 ],
	"autoorganize" : 1,
	"hideprojectwindow" : 0,
	"showdependencies" : 1,
	"autolocalize" : 0,
	"contents" : 	{
		"patchers" : 		{
			"main.maxpat" : 			{
				"kind" : "patcher",
				"local" : 1,
				"toplevel" : 1
			}
,
			"abstractions/sub_auto_detect.maxpat" : 			{
				"kind" : "patcher",
				"local" : 1
			}
,
			"abstractions/sub_tof.maxpat" : 			{
				"kind" : "patcher",
				"local" : 1
			}
,
			"abstractions/sub_pressure.maxpat" : 			{
				"kind" : "patcher",
				"local" : 1
			}
,
			"abstractions/sub_piezo.maxpat" : 			{
				"kind" : "patcher",
				"local" : 1
			}

		}
,
		"code" : 		{
			"code/bootstrap.js" : 			{
				"kind" : "javascript",
				"local" : 1
			}
,
			"code/auto_detect.js" : 			{
				"kind" : "javascript",
				"local" : 1
			}
,
			"code/who_probe.js" : 			{
				"kind" : "javascript",
				"local" : 1
			}

		}

	}
,
	"layout" : 	{

	}
,
	"searchpath" : 	{

	}
,
	"detailsvisible" : 0,
	"amxdtype" : 1633771873,
	"readonly" : 0,
	"devpathtype" : 0,
	"devpath" : ".",
	"sortmode" : 0,
	"viewmode" : 0
}
