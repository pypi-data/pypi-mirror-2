dependencies = {
	layers: [
		{
			name: "dojo.js",
			dependencies: [
				"dojo.io.iframe",
				"dojo.number",
				"dojo.back",
				"dojo.currency",
				"dojo.cldr.monetary",
				"dojo.cldr.nls.en_us.currency",
				"dojo.cldr.nls.en_us.number",
                "dojo.data.ItemFileReadStore",
                "dojo.data.ItemFileWriteStore",
                "dojo.data.util.filter",
                "dojo.data.util.simpleFetch",
                "dojo.data.util.sorter",
                "dojo.date.stamp",
                "dojo.dnd.move",
                "dojo.fx",
                "dojo.fx.Toggler",
                "dojo.nls.dojo_en-us"
			]
		},
		{
			name: "../dijit/dijit.js",
			dependencies: [
				"dijit.dijit",
                "dijit._Widget",
                "dijit._Templated",
                "dijit._KeyNavContainer",
                "dijit.Menu",
                "dijit.form.Form",
                "dijit.form.ValidationTextBox",
                "dijit.form.CheckBox",
                "dijit.form.Textarea",
                "dijit.form.DateTextBox",
                "dijit.form.FilteringSelect",
                "dijit.form.ToggleButton",
                "dijit.form.Button",
                "dijit.form.TimeTextBox",
                "dijit.form.TimePicker",
                "dijit.form.NumberSpinner",
                "dijit.form.Spinner",
                "dijit.form.NumberTextBox",
                "dijit.form.CurrencyTextBox",
                "dijit.form.HorizontalSlider",
                "dijit.layout.ContentPane",
                "dijit.layout.TabContainer",
                "dijit.InlineEditBox",
                "dijit.Editor",
                "dijit.nls.dijit_en-us"
			]
		},
		{
			name: "../dojox/grid/DataGrid.js",
			dependencies: [
                "dojox.grid.DataGrid",
                "dojox.grid.cells.dijit"
			]
		}
    ],
    prefixes : [
        ['dijit', '../dijit' ],
        ['dojox', '../dojox' ]
    ]
}
