dojo.require("dojo.fx");

dojo.require("dijit._Templated");
dojo.require("dijit.layout.ContentPane");

up_template = '<div class="${baseClass} mb10"><div class="bggreen" dojoAttachEvent="onclick:toggle, onkeypress:_onTitleKey, onfocus:_handleFocus, onblur:_handleFocus, onmouseenter:_onTitleEnter, onmouseleave:_onTitleLeave" tabindex="0" waiRole="button" class="dijitTitlePaneTitle" dojoAttachPoint="titleBarNode,focusNode"> <div class="curvy4 bggreen"></div> <div class="curvy2 bggreen"> <div class="bggrn1 ml2 mr2" style="height : 1px;"></div> </div> <div class="curvy1 bggreen"> <div class="bggrn1 ml1 mr1" style="height : 1px;"></div> </div> <div class="bggreen"> <div class="bggrn1 ml1 mr1 pl5 pb2"> <span class="fntsmall" style="margin-left : 5px;" dojoAttachPoint="arrowNodeInner" class="dijitArrowNodeInner"></span> <span class="fntbold" dojoAttachPoint="titleNode" class="dijitTitlePaneTextNode"></span> <span class="fntxsmall upclose pointer" dojoAttachEvent="onclick:_onClose">&times;</span> </div> </div> </div> <div class="dijitTitlePaneContentOuter" dojoAttachPoint="hideNode"> <div class="dijitReset" dojoAttachPoint="wipeNode"> <div class="dijitTitlePaneContentInner" dojoAttachPoint="containerNode" waiRole="region" tabindex="-1"> <!-- nested divs because wipeIn()/wipeOut() doesnt work right on node w/padding etc.  Put padding on inner div. --> </div> </div> </div> </div>'

dojo.declare(
	"UserTitlePane",
	[dijit.layout.ContentPane, dijit._Templated],
{
	// summary:
	//		A pane with a title on top, that can be expanded or collapsed.
	//
	// description:
	//		An accessible container with a Title Heading, and a content
	//		section that slides open and closed. UserTitlePane is an extension to 
	//		`dijit.layout.ContentPane`, providing all the usesful content-control aspects from it.
	//
	// example:
	// | 	// load a UserTitlePane from remote file:
	// |	var foo = new dijit.TitlePane({ href: "foobar.html", title:"Title" });
	// |	foo.startup();
	//
	// example:
	// |	<!-- markup href example: -->
	// |	<div dojoType="dijit.TitlePane" href="foobar.html" title="Title"></div>
	// 
	// example:
	// |	<!-- markup with inline data -->
	// | 	<div dojoType="dijit.TitlePane" title="Title">
	// |		<p>I am content</p>
	// |	</div>

	// title: String
	//		Title of the pane
	title: "",

	// open: Boolean
	//		Whether pane is opened or closed.
	open: true,

	// duration: Integer
	//		Time in milliseconds to fade in/fade out
	duration: dijit.defaultDuration,

	// baseClass: String
	//		The root className to use for the various states of this widget.
	baseClass: "UserTitlePane",

    //templatePath : dojo.moduleUrl( '', 'templates/TitlePane.html' ),

	attributeMap: dojo.delegate(dijit.layout.ContentPane.prototype.attributeMap, {
		title: { node: "titleNode", type: "innerHTML" }
	}),

	postCreate: function(){
		if(!this.open){
			this.hideNode.style.display = this.wipeNode.style.display = "none";
		}
		this._setCss();
		dojo.setSelectable(this.titleNode, false);
		dijit.setWaiState(this.containerNode, "labelledby", this.titleNode.id);
		dijit.setWaiState(this.focusNode, "haspopup", "true");

		// setup open/close animations
		var hideNode = this.hideNode, wipeNode = this.wipeNode;
		this._wipeIn = dojo.fx.wipeIn({
			node: this.wipeNode,
			duration: this.duration,
			beforeBegin: function(){
				hideNode.style.display="";
			}
		});
		this._wipeOut = dojo.fx.wipeOut({
			node: this.wipeNode,
			duration: this.duration,
			onEnd: function(){
				hideNode.style.display="none";
			}
		});
		this.inherited(arguments);
	},

	_setOpenAttr: function(/* Boolean */ open){
		// summary:
		//		Hook to make attr("open", boolean) control the open/closed state of the pane.
		// open: Boolean
		//		True if you want to open the pane, false if you want to close it.
		if(this.open !== open){ this.toggle(); }
	},

	_setContentAttr: function(content){
		// summary:
		//		Hook to make attr("content", ...) work.
		// 		Typically called when an href is loaded.  Our job is to make the animation smooth.

		if(!this.open || !this._wipeOut || this._wipeOut.status() == "playing"){
			// we are currently *closing* the pane (or the pane is closed), so just let that continue
			this.inherited(arguments);
		}else{
			if(this._wipeIn && this._wipeIn.status() == "playing"){
				this._wipeIn.stop();
			}

			// freeze container at current height so that adding new content doesn't make it jump
			dojo.marginBox(this.wipeNode, { h: dojo.marginBox(this.wipeNode).h });

			// add the new content (erasing the old content, if any)
			this.inherited(arguments);

			// call _wipeIn.play() to animate from current height to new height
			if(this._wipeIn){
				this._wipeIn.play();
			}else{
				this.hideNode.style.display = "";
			}
		}
	},

	toggle: function(){
		// summary:
		//		Switches between opened and closed state
		dojo.forEach([this._wipeIn, this._wipeOut], function(animation){
			if(animation && animation.status() == "playing"){
				animation.stop();
			}
		});

		var anim = this[this.open ? "_wipeOut" : "_wipeIn"]
		if(anim){
			anim.play();
		}else{
			this.hideNode.style.display = this.open ? "" : "none";
		}
		this.open =! this.open;

		// load content (if this is the first time we are opening the TitlePane
		// and content is specified as an href, or href was set when hidden)
		this._onShow();

		this._setCss();
	},

	_setCss: function(){
		// summary:
		//		Set the open/close css state for the TitlePane
		var classes = ["dijitClosed", "dijitOpen"];
		var boolIndex = this.open;
		var node = this.titleBarNode || this.focusNode;
		dojo.removeClass(node, classes[!boolIndex+0]);
		node.className += " " + classes[boolIndex+0];

		// provide a character based indicator for images-off mode
		this.arrowNodeInner.innerHTML = this.open ? "&#8963;" : "&#8964;";
	},

	_onTitleKey: function(/*Event*/ e){
		// summary:
		//		Callback when user hits a key
		if(e.charOrCode == dojo.keys.ENTER || e.charOrCode == ' '){
			this.toggle();
		}else if(e.charOrCode == dojo.keys.DOWN_ARROW && this.open){
			this.containerNode.focus();
			e.preventDefault();
	 	}
	},
	
	_onTitleEnter: function(){
		// summary:
		//		Callback when someone hovers over my title
		dojo.addClass(this.focusNode, "dijitTitlePaneTitle-hover");
	},

	_onTitleLeave: function(){
		// summary:
		//		Callback when someone stops hovering over my title
		dojo.removeClass(this.focusNode, "dijitTitlePaneTitle-hover");
	},

    _onClose    : function(/*Event*/ e) {
        // summary :
        //      Close (actually hide) the user pane.
        this.hidden = true;
        dojo.fx.wipeOut({ node: this.domNode, duration: 200 }).play();
        if( this.addable_span ) {
            dojo.fx.wipeIn({ node: this.addable_span, duration: 200 }).play();
        }
        dojo.stopEvent( e );
    },

	_handleFocus: function(/*Event*/ e){
		// summary:
		//		Handle blur and focus for this widget
		
		// add/removeClass is safe to call without hasClass in this case
		dojo[(e.type == "focus" ? "addClass" : "removeClass")](this.focusNode, this.baseClass + "Focused");
	},

	setTitle: function(/*String*/ title){
		// summary:
		//		Deprecated.  Use attr('title', ...) instead.
		dojo.deprecated("dijit.TitlePane.setTitle() is deprecated.  Use attr('title', ...) instead.", "", "2.0");
		this.titleNode.innerHTML = title;
	}
});
