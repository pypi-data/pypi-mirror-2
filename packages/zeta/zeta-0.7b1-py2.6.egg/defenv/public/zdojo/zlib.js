// This file is subject to the terms and conditions defined in
// file 'LICENSE', which is part of this source code package.
//       Copyright (c) 2009 SKR Farms (P) LTD.

// TODO :
//  1. Refactor all form widget creation. (mostly done)
//  2. Javascript code should not compose the urls. All url composition should
//     be confined to few files, preferrably python.
// Gotcha :
//  1. Dojo data store item's "attributes" are qutomatically converted to
//     array type, even if the server returns the attribute as a scalar type.

/**************  Publish-Subscribe pattern for toaster messages ********/

//toaster = null;
//function toasterhandler( type, msg, duration ) {
//    var pos     = 'bl-up';
//    
//    toaster.positionDirection = pos;
//    toaster.setContent( msg, type, duration );
//    toaster.show();
//}

/**************  Publish-Subscribe pattern for flash messages ********/

function flashmsghandler( type, msg, timeout ) {
    var n_divblk = dojo.query( 'div#flashblk' )[0];
    var n_div    = dojo.query( 'div#flashmsg' )[0];
    
    if ( type == 'hide' ) {
        n_divblk.style.display = 'none';
    } else if ( type == 'error' ) {
        dojo.forEach(
            dojo.query( 'div.flash' ),
            function (n) { dojo.removeClass( n, 'bgyellow' ); dojo.addClass( n, 'bgLSalmon' ); }
        );
        if( n_divblk.style.display == 'none' )  {
            n_div.innerHTML = msg;
            n_divblk.style.display = 'block';
        } else {
            n_div.innerHTML = n_div.innerHTML + ' ; ' + msg;
        }
    } else if ( type == 'message' ) {
        if( dojo.hasClass( n_div, 'bgLSalmon' ) && n_divblk.style.display == 'block' ) {
            n_div.innerHTML = n_div.innerHTML + ' ; ' + msg;
        } else {
            dojo.forEach(
                dojo.query( 'div.flash' ),
                function (n) { dojo.removeClass( n, 'bgLSalmon' ); dojo.addClass( n, 'bgyellow' ); }
            );
            n_div.innerHTML = msg;
            n_divblk.style.display = 'block';
        }
    }
    if ( timeout ) {
        dojo.fx.wipeOut({ node : n_divblk, delay : timeout, duration: 1000 }).play();
    }
}

/********************* Form helpers ****************************/
function submitform( formnode, e ) {
    if ( formnode ) {
        var dijitform = dijit.byId( dojo.attr( formnode, 'id' ));

        dojo.publish( 'flash', [ 'message', 'Please wait ...' ] );
        if ( dijitform && dijitform.validate()) {
            dojo.xhrPost({
                url  : dojo.attr( formnode, 'action' ),
                form : dojo.attr( formnode, 'id' ),
                sync : true,
                load : function( resp ) {
                        dojo.publish( 'flash', [ 'hide' ]);
                       },
                error: function( resp ) {
                        errmsg = resp.responseText;
                        dojo.publish( 'flash', [ 'error', errmsg, 2000 ] );
                       }
            });
        } else {
            dojo.publish( 'flash', [ 'error', "Invalid form fields", 2000 ]);
            dojo.stopEvent( e );
        }
    } else {
        console.log( 'Form '+formid+'not found !!' );
    }
}

/*********************** Generic Helpers *************************/
function create_anchor( href, text ) {
    return dojo.string.substitute(
               '<a href="${href}">${text}</a>', { href: href, text: text }
           );
}
function create_span( style, text ) {
    return dojo.string.substitute(
               '<span style="${style}">${text}</span>', { style: style, text: text }
           );
}
function select_goto( n_selectgoto ) {
    if (n_selectgoto) {
        dojo.connect( n_selectgoto,
                      'onchange',
                      function( e ) {
                        window.location = n_selectgoto.value;
                        dojo.stopEvent(e) 
                      } 
                    );
    }
}
function create_ifrs_store( options ) {
    var items = []
    for( i = 0; i < options.length ; i++ ) {
        items[items.length] = { name : options[i] }
    }
    var store = new dojo.data.ItemFileReadStore(
                    { data : { identifier : 'name', items : items } }
                );
    return store
}
function keys( props ) {
    var keys = []
    for( k in props ) { keys[keys.length] = k }
    return keys
}
function values( props ) {
    var values = []
    for( k in props ) { values[values.length] = props[k] }
    return values
}
function keyforvalue( props, value ) {
    for( k in props ) {
        if( props[k] == value ) {
            return k
        }
    }
}
function curvybox1( brdclass, bgclass, attrs, cont ) {
    brdclass = brdclass ? brdclass : "";
    bgclass  = bgclass ? bgclass : "";
    var d  = dojo.create( "div", attrs );
    var c4 = dojo.create( "div", { class: "curvy4 "+brdclass }, d, "last" );
    var c2 = dojo.create( "div", { class: "curvy2 "+brdclass }, d, "last" );
    var c1 = dojo.create( "div", { class: "curvy1 "+brdclass }, d, "last" );
    var c  = dojo.create( "div", { class: brdclass }, d, "last" );
    var cc = dojo.create( "div", { class: "p3 "+bgclass, style : { margin : "0px 1px 0px 1px" } },
                          c, "last" );
    dojo.create( "div", { class: bgclass, style : { height: "1px", margin: "0px 2px 0px 2px" } },
                 c2, "last" );
    dojo.create( "div", { class: bgclass, style : { height: "1px", margin: "0px 1px 0px 1px" } },
                 c1, "last" );
    if( cont ) { dojo.forEach( cont, function( n ) { dojo.place( n, cc, "last" ); } )}
    dojo.place( dojo.clone(c1), d, "last" );
    dojo.place( dojo.clone(c2), d, "last" );
    dojo.place( dojo.clone(c4), d, "last" );
    return d
}
function linkencode() {
    dojo.forEach( dojo.query( "div.wikiblk a[href]" ),
        function( n ) {
            if( dojo.attr( n, 'href' ).substr( 0, 7 ) == 'http://' ) {
                dojo.addClass( n, "extlink" );
            }
        }
    )
}
function toggler( n_trigger, n, v_text, h_text, hidden, onshow, onhidden ) {
    var _toggle = function( onshow, onhidden, e ) {
                        if(hidden) {
                            dojo.toggleClass( n, "dispnone", false );
                            hidden = false;
                            n_trigger.innerHTML = v_text;
                            onshow ?  onshow( n_trigger, n, v_text, h_text ) : null;
                        } else {
                            dojo.toggleClass( n, "dispnone", true );
                            hidden = true;
                            n_trigger.innerHTML = h_text;
                            onhidden ? onhidden( n_trigger, n, v_text, h_text ) : null;
                        }
                  }
    var _show   = function() {
                        dojo.toggleClass( n, "dispnone", false );
                        hidden = false;
                        n_trigger.innerHTML = v_text;
                        onshow ?  onshow( n_trigger, n, v_text, h_text ) : null;
                  }
    var _hide   = function() {
                        dojo.toggleClass( n, "dispnone", true );
                        hidden = true;
                        n_trigger.innerHTML = h_text;
                        onhidden ? onhidden( n_trigger, n, v_text, h_text ) : null;
                  }
    dojo.connect( n_trigger, 'onclick', dojo.partial( _toggle, onshow, onhidden ));
    n_trigger.toggle = dojo.partial( _toggle, onshow, onhidden, null );
    n.toggle         = dojo.partial( _toggle, onshow, onhidden, null );
    n.hide           = _hide;
    n.show           = _show;
}
function highlightbyclass( n, cls ) {
    dojo.connect( n, 'mouseover',
        function( e ) { dojo.toggleClass(e.currentTarget, cls, true) }
    );
    dojo.connect( n, 'mouseout',
        function( e ) { dojo.toggleClass(e.currentTarget, cls, false) }
    )
}
colorvalues = [
    "#000000", "#0000FF", "#8A2BE2", "#A52A2A", "#DEB887",
    "#5F9EA0", "#7FFF00", "#D2691E", "#FF7F50", "#6495ED",
    "#DC143C", "#00008B", "#008B8B", "#B8860B", "#A9A9A9",
    "#006400", "#BDB76B", "#8B008B", "#556B2F", "#FF8C00", "#9932CC",
    "#8B0000", "#E9967A", "#8FBC8F", "#483D8B", "#2F4F4F", "#00CED1",
    "#9400D3", "#FF1493", "#00BFFF", "#696969", "#1E90FF", "#B22222",
    "#228B22", "#FF00FF", "#FFD700",
    "#DAA520", "#808080", "#008000", "#FF69B4",
    "#CD5C5C", "#4B0082", "#ADD8E6", "#F08080", "#20B2AA", "#87CEFA",
    "#778899", "#B0C4DE", "#32CD32", 
    "#FF00FF", "#800000", "#66CDAA", "#0000CD", "#BA55D3", "#9370D8",
    "#3CB371", "#7B68EE", "#C71585", "#191970",
    "#808000", "#FFA500", "#FF4500", "#DA70D6", '#CD853F',
    "#800080", "#FF0000", "#BC8F8F",
    "#4169E1", "#8B4513", "#FA8072", "#F4A460", "#2E8B57", 
    "#A0522D", "#C0C0C0", "#87CEEB", "#6A5ACD", "#708090", 
    "#00FF7F", "#4682B4", "#D2B48C", "#008080", "#D8BFD8", "#FF6347",
    "#40E0D0", "#EE82EE", "#F5DEB3", "#9ACD32", "#FFE4C4", "#6B8E23"
]
function colormaps( literals ) {
    colormap = {}
    for( i=0 ; i < literals.length; i++ ) {
        colormap[literals[i]] = colorvalues[i%colorvalues.length];
    }
    return colormap;
}
function tckcolorcode( tdet, tckccodes ) {
    var color = tckccodes[0][2];
    for( i=1; i < tckccodes.length; i++ ) {
        var rules = tckccodes[i];
        var key   = rules[0];
        if( key == "" ) { continue; }
        if( tdet[key] == rules[1] ) {
            // Match found, pick the color code
            color = rules[2];
            break;
        }
    };
    return color
}

// Chart selection
function selectchart( n_select, charts ) {
    function sconchange( charts, e ) {
        var c = charts[e.target.value];
        dojo.toggleClass( charts.currcntnr, 'dispnone', true )
        charts.currchart.destroy();
        dojo.toggleClass( c.cntnr, 'dispnone', false )
        charts.currchart = c.init();
        charts.currcntnr = c.cntnr
        dojo.stopEvent(e) 
    }
    dojo.connect( n_select, 'onchange', dojo.partial( sconchange, charts ) );
}

// Chart zooming
function onchartclose( node, e ) {
    dojo.destination( node );
    dojo.stopEvent(e) 
}
function onchartzoomin(container, id, chartinit, e) {
    var n_d1    = dojo.create( "div", { class: "posa bggray1 p3 br5" } )
    var n_d1_d1 = dojo.create( "div", { class: "bgwhite" }, n_d1 );
    var n_c1    = dojo.create( "div", { class: "fgblue pointer", innerHTML: "close" },
                               n_d1_d1, "first" );

    dojo.create( "div", { id: id, class: "chart br5",
                          style: { width: "900px", height: "500px", margin: "0",
                                   border: "2px solid LightSteelBlue",
                                   top: "100px", left : "100px"
                                 },
                        },
                 n_d1_d1, "last" );

    dojo.place( n_d1, container, "first" );
    dojo.connect( n_c1, 'onclick', dojo.partial( onchartclose, n_d1 ) );
    chartinit(id);
    dojo.stopEvent(e);
}

/*********************** URL constructors ********************************/
function url_pgmap() {
    return '/siteadmin?jsonobj=pgmap&view=js'
}
function url_usernames() {
    return '/u?jsonobj=usernames&view=js'
}
function url_userperms() {
    return '/u?jsonobj=userperms&view=js'
}
function url_userstatus() {
    return '/u?jsonobj=userstatus&view=js'
}
function url_userconns() {
    return '/u?jsonobj=userconns&view=js'
}
function url_myprojects() {
    return '/p?jsonobj=myprojects&view=js'
}
function url_projectnames() {
    return '/p?jsonobj=projectnames&view=js'
}
function url_projectstatus() {
    return '/p?jsonobj=projectstatus&view=js'
}
function url_foruser( username ) {
    return '/u/' + username
}
function url_fortagname( tagname ) {
    return '/tag/' + tagname
}
function url_forproject( projectname ) {
    return '/p/' + projectname
}
function url_forpindex() {
    return '/p'
}

/*********************** Data Read Stores ********************************/
function ddr_onBegin( size, req ) {
}
function ddr_onComplete( items, req ) {
    dojo.publish( 'flash', [ 'hide' ] );
    this.items = items
}
function ddr_onError( errorData, req ) {
    console.log( errorData );
}
function ddr_fetch( args ) {
    // Fetch via url.
    dojo.publish( 'flash', [ 'message', "Fetching ..." ] );
    var params = { scope      : this,
                   onBegin    : ddr_onBegin,
                   onComplete : ddr_onComplete,
                   onError    : ddr_onError
                 };
    dojo.mixin( params, args );
    this.store.fetch( params );
}
function ddr_staticfetch( args ) {
    // Fetch from static data store.
    dojo.publish( 'flash', [ 'message', "Fetching ..." ] );
    var params = { scope      : this,
                   onBegin    : ddr_onBegin,
                   onComplete : ddr_onComplete,
                   onError    : ddr_onError
                 };
    dojo.mixin( params, args );
    this.staticstore.fetch( params );
}
function ddr_itembyID( idval, attr_id ) {
    // Due to data store optimization (by-passing fetch()) for the initial
    // data load, the internal variables of the data store are not set
    // properly.
    if ( attr_id ) {
        for( i = 0 ; i < this.items.length ; i++ ) {
            var id = this.store.getValue( this.items[i], attr_id );
            if ( id == idval ) {
                return this.items[i];
            }
        }
    } else {
        for( i = 0 ; i < this.items.length ; i++ ) {
            if ( this.store.getIdentity( this.items[i] ) == idval ) {
                return this.items[i];
            }
        }
    }
}
function ddr_itemValues( attrs ) {
    return dojo.map(
                this.items,
                function( item ) { 
                    return dojo.map( 
                                attrs,
                                function( attr ) { return this.store.getValue( item, attr ); },
                                this
                           )
                },
                this
           )
}

//usernames  = {
//    store      : new dojo.data.ItemFileReadStore({
//                         url             : url_usernames(),
//                         clearOnClose    : true,
//                         urlPreventCache : true
//                      }),
//    fetch      : ddr_fetch,
//    itembyID   : ddr_itembyID,
//    itemValues : ddr_itemValues,
//    items      : null
//}
//userconns  = {
//    store      : new dojo.data.ItemFileReadStore({
//                         url             : url_userconns(),
//                         clearOnClose    : true,
//                         urlPreventCache : true
//                      }),
//    fetch      : ddr_fetch,
//    itembyID   : ddr_itembyID,
//    itemValues : ddr_itemValues,
//    items      : null
//}
//myprojects = {
//    store      : new dojo.data.ItemFileReadStore({
//                         url             : url_myprojects(),
//                         clearOnClose    : true,
//                         urlPreventCache : true
//                      }),
//    fetch      : ddr_fetch,
//    itembyID   : ddr_itembyID,
//    itemValues : ddr_itemValues,
//    items      : null
//}
//projectnames = {
//    store      : new dojo.data.ItemFileReadStore({
//                         url             : url_projectnames(),
//                         clearOnClose    : true,
//                         urlPreventCache : true
//                      }),
//    fetch      : ddr_fetch,
//    itembyID   : ddr_itembyID,
//    itemValues : ddr_itemValues,
//    items      : null
//}

function make_ifrs_pgmap() {
    pgmap = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : url_pgmap(),
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'pgmap', pgmap );
}
function make_ifrs_userperms() {
    userperms  = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : url_userperms(),
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'userperms', userperms );
}
function make_ifrs_userstatus() {
    var userstatus = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : url_userstatus(),
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'userstatus', userstatus );
}
function make_ifrs_projectstatus() {
    var projectstatus = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : url_projectstatus(),
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'projectstatus', projectstatus );
}
function make_ifrs_pcomplist( jsonurl ) {
    var pcomplist = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                         }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'pcomplist', pcomplist );
}
function make_ifrs_mstnlist( jsonurl ) {
    var mstnlist = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                         }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'mstnlist', mstnlist );
}
function make_ifrs_verlist( jsonurl ) {
    var verlist = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'verlist', verlist );
}
function make_ifrs_projectteams( jsonurl ) {
    var projectteams = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'projectteams', projectteams );
}
function make_ifrs_teamperms( jsonurl ) {
    var teamperms = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'teamperms', teamperms );
}
function make_ifrs_prjperms( jsonurl ) {
    var prjperms = {
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    dojo.setObject( 'prjperms', prjperms );
}
function make_ifrs_wikicomments( jsonurl, data ) {
    var wikicomments = {
        staticstore: data ? 
                        new dojo.data.ItemFileReadStore({ data: data })
                        : null,
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true,
                          }),
        fetch      : ddr_fetch,
        staticfetch: ddr_staticfetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null,
    }
    dojo.setObject( 'wikicomments', wikicomments );
}
function make_ifrs_wikircomments( jsonurl, data ) {
    var wikircomments = {
        staticstore: data ? 
                        new dojo.data.ItemFileReadStore({ data: data })
                        : null,
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        staticfetch: ddr_staticfetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : data ? data.items : null
    }
    dojo.setObject( 'wikircomments', wikircomments );
}
function make_ifrs_tckcomments( jsonurl, data ) {
    var tckcomments = {
        staticstore: data ? 
                        new dojo.data.ItemFileReadStore({ data: data })
                        : null,
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        staticfetch: ddr_staticfetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : data ? data.items : null
    }
    dojo.setObject( 'tckcomments', tckcomments );
}
function make_ifrs_tckrcomments( jsonurl, data ) {
    var tckrcomments = {
        staticstore: data ? 
                        new dojo.data.ItemFileReadStore({ data: data })
                        : null,
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        staticfetch: ddr_staticfetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : data ? data.items : null
    }
    dojo.setObject( 'tckrcomments', tckrcomments );
}
function make_ifrs_revwrcomments( jsonurl, data ) {
    var revwrcomments = {
        staticstore: data ? 
                        new dojo.data.ItemFileReadStore({ data: data })
                        : null,
        store      : new dojo.data.ItemFileReadStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        staticfetch: ddr_staticfetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : data ? data.items : null
    }
    dojo.setObject( 'revwrcomments', revwrcomments );
}

/*********************** Data Write Stores ********************************/
function ddw_onset( i, attr, oldval, newval ) {
    console.log( arguments );
}
function ddw_onnew( i ) {
    console.log( arguments );
}
function ddw_ondelete( i ) {
    console.log( arguments );
}
function make_ifws_wikilist( jsonurl, onset, onnew, ondelete ) {
    var wikilist = {
        store      : new dojo.data.ItemFileWriteStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    if( ! onset ) { onset = ddw_onset }
    if( ! onnew ) { onnew = ddw_onnew }
    if( ! ondelete ) { ondelete = ddw_ondelete }
    dojo.connect( wikilist.store, 'onSet',  wikilist, onset );
    dojo.connect( wikilist.store, 'onNew',  wikilist, onnew );
    dojo.connect( wikilist.store, 'onDelete',  wikilist, ondelete );
    dojo.setObject( 'wikilist', wikilist );
}

function make_ifws_ticketlist( jsonurl, onset, onnew, ondelete ) {
    var ticketlist = {
        store      : new dojo.data.ItemFileWriteStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true,
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    if( ! onset ) { onset = ddw_onset }
    if( ! onnew ) { onnew = ddw_onnew }
    if( ! ondelete ) { ondelete = ddw_ondelete }
    dojo.connect( ticketlist.store, 'onSet',  ticketlist, onset );
    dojo.connect( ticketlist.store, 'onNew',  ticketlist, onnew );
    dojo.connect( ticketlist.store, 'onDelete',  ticketlist, ondelete );
    dojo.setObject( 'ticketlist', ticketlist );
}

function make_ifws_vcslist( jsonurl, onset, onnew, ondelete ) {
    var vcslist = {
        store      : new dojo.data.ItemFileWriteStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    if( ! onset ) { onset = ddw_onset }
    if( ! onnew ) { onnew = ddw_onnew }
    if( ! ondelete ) { ondelete = ddw_ondelete }
    dojo.connect( vcslist.store, 'onSet',  vcslist, onset );
    dojo.connect( vcslist.store, 'onNew',  vcslist, onnew );
    dojo.connect( vcslist.store, 'onDelete',  vcslist, ondelete );
    dojo.setObject( 'vcslist', vcslist );
}

function make_ifws_revwlist( jsonurl, onset, onnew, ondelete ) {
    var revwlist = {
        store      : new dojo.data.ItemFileWriteStore({
                             url             : jsonurl,
                             clearOnClose    : true,
                             urlPreventCache : true
                          }),
        fetch      : ddr_fetch,
        itembyID   : ddr_itembyID,
        itemValues : ddr_itemValues,
        items      : null
    }
    if( ! onset ) { onset = ddw_onset }
    if( ! onnew ) { onnew = ddw_onnew }
    if( ! ondelete ) { ondelete = ddw_ondelete }
    dojo.connect( revwlist.store, 'onSet',  revwlist, onset );
    dojo.connect( revwlist.store, 'onNew',  revwlist, onnew );
    dojo.connect( revwlist.store, 'onDelete',  revwlist, ondelete );
    dojo.setObject( 'revwlist', revwlist );
}

/*********************** XHR helper functions *****************************/
function xhrget_obj( url, content, handleas, sync, objname, okhandler, failhandler ) {
    dojo.xhrGet({
        url      : url,
        content  : content,
        handleAs : handleas,
        sync     : sync,
        load     : function( response ) {
                        if ( objname ) { dojo.setObject( objname, response ); }
                        if ( okhandler ) { okhandler( response ); }
                    },
        error    : function( response ) {
                        errmsg = response.responseText;
                        if (errmsg) {
                            dojo.publish( 'flash', [ 'error', errmsg, 2000 ]);
                        }
                        if ( failhandler ) { failhandler( response ); }
                    }
    });
}    
function xhrpost_obj( url, content, handleas, sync, objname, okhandler, failhandler ) {
    dojo.xhrPost({
        url      : url,
        content  : content,
        handleAs : handleas,
        sync     : sync,
        load     : function( response ) {
                        if ( objname ) { dojo.setObject( objname, response ); }
                        if ( okhandler ) { okhandler( response ); }
                    },
        error    : function( response ) {
                        errmsg = response.responseText;
                        if (errmsg) {
                            dojo.publish( 'flash', [ 'error', errmsg, 2000 ]);
                        }
                        if ( failhandler ) { failhandler( response ); }
                    }
    });
}    

/************       Google Maps     **************/

function addrshorten( addr ) {  // Shorted the address based on , or space
    addr = addr.split( /,/ );
    addr.reverse();
    addr.pop();
    addr.reverse();
    return addr.join(', ') ;
}
function compute_marker( point, name, address ) {
    var marker = new GMarker( point, { title : (name + ' @ ' + address) } );
    return marker;
}
function setCenter( map, lat, lng, zoom ) {
    map.setCenter( new GLatLng( lat, lng ), zoom );
}
function addrhandler( name, fulladdress, address, point ) {
    if ( ! point ) {
        address = addrshorten( address );
        if( address ) {
            showAddress( name, fulladdress, address );
        } else {
            console.log( "Unable to spot address " + fulladdress );
        }
    } else {
        var marker = compute_marker( point, name, fulladdress )
        if( map ) {
            map.addOverlay( marker );
        }
    }
}
function showAddress( name, fulladdress, address ) {
    if( geocoder ) {
        geocoder.getLatLng(
            address, dojo.partial( addrhandler, name, fulladdress, address )
        );
    }
}
function creategmap( nodeid, h, w ) {
    var geocoder = null;
    if( GBrowserIsCompatible() ) {
        map = new GMap2(    
                document.getElementById( nodeid ),
                { size: new GSize(h,w) }
              );
        map.setUIToDefault();
        geocoder = new GClientGeocoder();
        //map.addControl( new GLargeMapControl);
        map.setCenter( new GLatLng( 0, 0 ), 1 );
    }
    return [map, geocoder]
}

/************       User Panes      **************/

function setup_userpanes() {
}

/************/

userpanes     = {};     // title : , wid :

function adjust_upheight() {
}
