// This file is subject to the terms and conditions defined in
// file 'LICENSE', which is part of this source code package.
//       Copyright (c) 2009 SKR Farms (P) LTD.

// Gotcha : 
//  1. Some of the properties in widget-declare are magically defined and used
//     by dijit._Widget base class (like 'id' property). Beware !
//  2. Dojo data store item's "attributes" are qutomatically converted to
//     array type, even if the server returns the attribute as a scalar type.
// Notes :
//  1. Implements, Form, Attachments, Tags, ConfigTabs, Menu, MenuItem widgets.
//

/*************************************************************************************
*********************************** Form widget
**************************************************************************************/

/****************************** Zeta classes ********************************/
dojo.declare(
'ZFavorite',
'',
{
  constructor : function( n_interface, n_form, n_field ) {
      this.n_interface = n_interface;
      this.n_form      = n_form;
      this.n_field     = n_field;
      if( dojo.attr( n_field, 'name' ) == 'addfavuser' ) {
          dojo.toggleClass( n_interface, 'favselected', false );
          dojo.toggleClass( n_interface, 'favdeselected', true );
      } else {
          dojo.toggleClass( n_interface, 'favdeselected', false );
          dojo.toggleClass( n_interface, 'favselected', true );
      }
      dojo.connect( n_interface, 'onclick', this, this.onclick );
  },

  onclick : function( e ) {
      if ( dojo.attr( this.n_field, 'name' ) == 'addfavuser' ) {
          dojo.publish( 'flash', [ 'message', 'Adding as favorite ...' ] );
      } else {
          dojo.publish( 'flash', [ 'message', 'Deleting favorite ...' ] );
      }
      dojo.xhrPost({
          url      : dojo.attr( this.n_form, 'action' ),
          form     : dojo.attr( this.n_form, 'id' ),
          method   : 'post',
          load     : dojo.hitch(
                      this,
                      function( resp ) {
                          dojo.publish( 'flash', [ 'hide' ] );
                          if ( dojo.attr( this.n_field, 'name' ) == 'addfavuser' ) {
                              dojo.attr( this.n_field, 'name', 'delfavuser' )
                              dojo.toggleClass( this.n_interface, 'favdeselected', false );
                              dojo.toggleClass( this.n_interface, 'favselected', true );
                          } else {
                              dojo.attr( this.n_field, 'name', 'addfavuser' )
                              dojo.toggleClass( this.n_interface, 'favselected', false );
                              dojo.toggleClass( this.n_interface, 'favdeselected', true );
                          }
                      }
                     ),
          error    : dojo.hitch(
                      this,
                      function( errresp ) {
                          dojo.publish( 'flash', [ 'error', 'Failed in favorites !!', 2000 ] );
                      }
                     )
      });
      dojo.stopEvent( e );
  }
}
);

dojo.declare(
'ZSelect',
'',
{
  constructor : function( n_select, publishname, onchange ) {
      this.n_select    = n_select;
      this.publishname = publishname;
      if ( publishname ) {
          dojo.subscribe( publishname, null, dojo.hitch( this, '_updatelist' ));
      }
      if ( onchange ) {
          dojo.connect( n_select, 'onchange', onchange );
      }
  },

  _updatelist : function( options, selected ) {
      this.n_select.innerHTML = ''

      dojo.forEach(
          options,
          dojo.hitch( 
              this,
              function( opt ) { 
                  if ( opt.val == selected ) {
                      option = dojo.create( 
                                      'option',
                                      { value: opt.val, selected: "selected" } );
                  } else {
                      option = dojo.create( 'option', { value: opt.val } );
                  }
                  option.innerHTML = opt.txt;
                  dojo.place( option, this.n_select, 'last' );
              }
          )
      );
  }
}
);

/******************************* Widgets ********************************/ 
dojo.declare( 'zeta.Form',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  formid: "",         // String that identifies the form node-tree.

  formnode: null,     // dojo node representing the form.

  onsubmit: null,     // Handler to be invoked while submiting the form.

  allfields: false,   // Special case handling for form elements

  normalsub: false,   // Normal form submition.

  templateString: "<div></div>", // Gotcha : Dummy template, to avoid widget crash.

  postCreate : function() {
      if ( this.formid ) {       // When the widget is instantiated with 'formid'
          this.formnode = dojo.byId( this.formid );
      } else if ( this.formnode ) { // When the widget is instantiated with 'form-node'
          this.formid = dojo.attr( this.formnode, "id" );
      }

      // Mandatory Properties
      var props    = { action   : dojo.attr( this.formnode, 'action' ),
                       method   : dojo.attr( this.formnode, 'method' ),
                       onSubmit : dojo.hitch( this, '_subhandler' )
                     }
      // Optional Properties
      var name     = dojo.attr( this.formnode, 'name' );
      var enctype  = dojo.attr( this.formnode, 'enctype' );
      if ( name )    { props.name = name; }
      if ( enctype ) { props.enctype = enctype; }

      x = new dijit.form.Form( props, this.formnode );

      this.formnode  = x.domNode;
      this.dijitform = x;

      // Widgetify Form 'input' elements.
      if ( this.allfields ) {
          /* Some times we need to massage the input fields that
           * are not structured like other forms. */
          dojo.forEach( dojo.query( 'textarea', this.formnode ),
                        dojo.hitch( this, '_maketextarea' ));
      } else {
          dojo.forEach( dojo.query( 'div.ftbox input', this.formnode ),
                        dojo.hitch( this, '_maketextbox' ));
          dojo.forEach( dojo.query( 'div.fdtbox input', this.formnode ),
                        dojo.hitch( this, '_makedatetextbox' ));
          dojo.forEach( dojo.query( 'div.fpass input', this.formnode ),
                        dojo.hitch( this, '_makepassbox' ));
          dojo.forEach( dojo.query( 'div.fradio input', this.formnode ),
                        dojo.hitch( this, '_makeradio' ));
          dojo.forEach( dojo.query( 'div.ftarea textarea', this.formnode ),
                        dojo.hitch( this, '_maketextarea' ));
      }

      // widgetify submit / reset / button elements.
      dojo.query( 'input[type=submit]', this.formnode ).forEach( 
          function( n ) { new dijit.form.Button( { label : n.value, type : 'submit' }, n ); },
          this
      )
      dojo.query( 'input[type=reset]', this.formnode ).forEach( 
          function( n ) { new dijit.form.Button( { label : n.value, type : 'reset' }, n ); },
          this
      )
      dojo.query( 'input[type=button]', this.formnode ).forEach( 
          function( n ) { new dijit.form.Button( { label : n.value, type : 'button' }, n ); },
          this
      )

      // Globalize the widget.
      dojo.setObject( 'form_'+this.formid, this.formnode );    // form-node
      dojo.setObject( 'zw_'+this.formid, this.dijitform );     // form-widget
  },

  _maketextbox : function( inp ) {
      var div    = inp.parentNode;
      var rgexp  = dojo.attr( div, 'regExp' );
      var value  = dojo.attr( inp, 'value' );
      var size   = dojo.attr( inp, 'size' );
      var style  = dojo.attr( inp, 'style' );
      var props  = { required : dojo.attr( div, 'required' ) == 'true' ? true : false,
                     name     : dojo.attr( inp, 'name' )
                   }
      if ( rgexp ) { props.regExp = rgexp }
      if ( value ) { props.value  = value }
      if ( size )  { props.size   = size }
      if ( style ) { props.style  = style }
      new dijit.form.ValidationTextBox( props, inp );
  },

  _makedatetextbox : function( inp ) {
      var div    = inp.parentNode;
      var value  = dojo.attr( inp, 'value' );
      var size   = dojo.attr( inp, 'size' );
      var style  = dojo.attr( inp, 'style' );
      var props  = { required : dojo.attr( div, 'required' ) == 'true' ? true : false,
                     name     : dojo.attr( inp, 'name' ),
                     constraints : { datePattern : 'dd/MM/yyyy', formatLength : 'short',
                                     selector : 'date' }
                   }
      if ( value ) { props.value  = new Date(value) }
      if ( size )  { props.size   = size }
      if ( style ) { props.style  = style }
      x = new dijit.form.DateTextBox( props, inp );
  },

  _maketextarea : function( inp ) {
      var div    = inp.parentNode;
      var value  = dojo.attr( inp, 'value' );
      var rows   = dojo.attr( inp, 'rows' );
      var cols   = dojo.attr( inp, 'cols' );
      var style  = dojo.attr( inp, 'style' );
      var tatype = dojo.attr( inp, 'tatype' );
      var props  = { required : dojo.attr( div, 'required' ) == 'true' ? true : false,
                     name     : dojo.attr( inp, 'name' )
                   }

      // Gotcha : The value is not propery updated from the innerHTML,
      // if the widget is already created (which is what seem to be happening 
      // on a refresh). May be we should clean the widget on moving out of the
      // page or on refresh.
      if ( value ) {
          props.value  = value;
      } else if ( inp.innerHTML ) {
          props.value = inp.innerHTML;
      }

      if ( rows )  { props.rows   = rows }
      if ( cols )  { props.cols   = cols }
      if ( style ) { props.style  = style }
      if ( tatype == 'simpletextarea' ) {
          ta = new dijit.form.SimpleTextarea( props, inp );
      } else {
          ta = new dijit.form.Textarea( props, inp );
          ta.resize();
      }
  },

  _makeradio    : function( inp ) {
      var div     = inp.parentNode;
      var value   = dojo.attr( inp, 'value' );
      var checked = dojo.attr( inp, 'checked' );
      var style   = dojo.attr( inp, 'style' );
      var props   = { required : dojo.attr( div, 'required' ) == 'true' ? true : false,
                      name     : dojo.attr( inp, 'name' )
                    }
      if ( value ) { props.value  = value }
      if ( checked ) { props.checked  = 'true' }
      if ( style ) { props.style  = style }
      new dijit.form.RadioButton( props, inp );
  },
                  
  _makepassbox : function( inp ) {
      var div = inp.parentNode;
      new dijit.form.TextBox( 
                  { type : 'password',
                    required : dojo.attr( div, 'required' ) == 'true' ? true : false,
                    name : dojo.attr( inp, 'name' )
                  }, inp );
  },

  _subhandler : function( e ) {
      if( this.onsubmit ) {
          this.onsubmit( e );
      } else if( this.normalsub ) {
          submitform( this.formnode, e );
          dojo.stopEvent( e );
      }
  }

}
);

/*************************************************************************************
*********************************** Attachment widget
**************************************************************************************/

dojo.declare( "zeta.Attachments",
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  user: [],           // [ user_id, username ] who requested the operation.

  id: "",             // Attachment node id

  class: "ml10 mt5 posr floatl", // Class attribue.

  addform: [],        // [ form-id, suburl ] to use for adding attachments

  delform: [],        // [ form-id, suburl ] to use for deleting attachments

  attachon: [],       // Optional [ obj-id, obj-name ] to add or delete from

  attachs: {},        // Optional Attachment details

  url: "",            // url for fetching attachment details, for AJAX request

  editable: false,    // Whether it is possible to add / delete attachments

  parSpans: null,     // Node holding children of spans, one for each attachment

  attachbox: null,    // Node representing the popup attach box

  label: 'Upload',    // Name to display for triggering the upload event

  upload: null,       // Node representing the upload interface

  clsdisplayitem: 'dispinln',    // How to display each attachment items.

  templateString: "<div></div>", // Gotcha : Dummy template, to avoid widget crash.

  // Gotcha : OnBlur does not work !!
  postCreate : function() {
      dojo.place( this._makenode(), this.domNode, "last" ); // Instantiate the attachment view
      this.parSpans = dojo.query( 'div[name=attachspans]', this.domNode )[0];

      if( this.editable ) {
          var addform = dojo.byId( this.addform[0] );
          dojo.connect( this.upload, 'onclick', this, 
                        function( e ) {
                              dojo.toggleClass( this.attachbox, 'dispnone' );
                              dojo.stopEvent(e);
                        }
                      );
          // On file input, add the file as attachment
          dojo.connect( dojo.query( 'input[type=file]', addform )[0], 'onchange',
                        dojo.hitch( this, '_addattach' )
                      );
          //dojo.connect( this.domNode, 'onblur', this,
          //              function (e) {
          //                    dojo.toggleClass( this.attachbox, 'dispnone', true );
          //                    dojo.stopEvent(e);
          //              }
          //            );
      }
      this._refreshattachs( false );
  },

  _makeforms: function() {
      var fa    = dojo.create( "form",
                               { id: this.addform[0], action: this.addform[1], method: "post",
                               enctype: "multipart/form-data" },
                               dojo.create( "div", {} ),
                               "last"
                             );
      dojo.create( "input", { type: "hidden", name: "user_id", value: this.user[0] }, fa, "last" );
      this.attachon
          ? dojo.create( "input",
                         { type: "hidden", name: this.attachon[1], value: this.attachon[0] },
                         fa, "last"
                       )
          : null;
      dojo.create( "input", { type: "file", name: "attachfile" },
                   dojo.create( "span", {}, fa, "last" ),
                   "last"
                 );
      var fd    = dojo.create( "form",
                               { id: this.delform[0], action: this.delform[1], method: "post" },
                               dojo.create( "div", { class: "dispnone" } ),
                               "last"
                             );
      dojo.create( "input", { type: "hidden", name: "user_id", value: this.user[0] }, fd, "last" );
      this.attachon
          ? dojo.create( "input",
                         { type: "hidden", name: this.attachon[1], value: this.attachon[0] },
                         fd, "last"
                       )
          : null;
      dojo.create( "input", { type: "hidden", name: "attach_id", value: "" }, fd, "last" );
      return [ fa.parentNode, fd.parentNode ];
  },

  _makenode: function() {
      var divi = dojo.create( // iconize
                      "span",
                      { name: 'iconadd', class: "pl18 fggray pointer fntbold undrln",
                        style: { background : "transparent url(/zetaicons/attach.png) no-repeat scroll 0" },
                        innerHTML: this.label,
                      }
                 );
      var divs = dojo.create( "div", { class: "m2", name: "attachspans" } ); // Attach spans
      var divc = curvybox1( "bglsb", "bgaliceblue",
                            { class: "posa dispnone z99",
                              style: { top : "2.2em" },  name: "attachbox" },
                            this._makeforms()
                          )
      var div  = curvybox1( "bgwhite", "bggray1", {}, [ divi, divs, divc ] );
      this.attachbox = divc;
      this.upload    = divi;
      return div;
  },

  _refreshattachs : function( fetch ) {
      if( fetch ) {
          xhrget_obj(
              this.url, null, 'json', true, null, 
              dojo.hitch( this, function ( resp ) { this.attachs = resp; } ),
              null
          )
      }
      /* Remove attachments if absent in the fetched json object */
      var newattachs = dojo.clone( this.attachs );
      dojo.query( 'div', this.parSpans ).forEach(
          function( n ) {
              var id = Number(dojo.attr( n, 'attach_id' ));
              if( id in this.attachs ) {
                  newattachs[id] = null;
              } else {
                  this.parSpans.removeChild( n );
              }
          }, this
      );
      /* Add attachments that are newly found */
      for ( id in newattachs ) {
          if( newattachs[id] == null) { continue }
          a = this.attachs[id];
          var span   = dojo.create(
                          'div',
                          { class: this.clsdisplayitem + " fntsmall ml5 pl5",
                            attach_id: a[0], 
                            style: { borderLeft: '1px solid gray' }
                          } 
                       );
          var anchor = dojo.create( 'a', {class:"nodec mr2", href:a[1], title:a[3] } );
          span.innerHTML   = ' ('+a[0]+') '
          anchor.innerHTML = a[2] 
          dojo.place( anchor, span, 'first' );
          if ( this.editable ) {
              close = dojo.create( 'a', {class:"fntxsmall vsuper pointer"} );
              close.innerHTML = '&times; ';
              dojo.place( close, span, 'last' );
              dojo.connect( close, 'onclick', dojo.hitch( this, '_delattach', span ));
          }
          dojo.place( span, this.parSpans, 'first' );
      }
  },

  _addattach : function( e ) {
      var aform = dojo.byId( this.addform[0] );
      var i_file = dojo.query( 'input[type=file]', aform )[0];
      dojo.publish( 'flash', [ 'message', 'Adding attachment ...' ]);
      if ( i_file.value != '' ) {
          dojo.io.iframe.send({
              url      : dojo.attr( aform, 'action' ),
              form     : dojo.attr( aform, 'id' ),
              method   : 'post',
              enctype  : dojo.attr( aform, 'enctype' ),
              handleAs : 'json',
              load     : dojo.hitch(
                          this,
                          function( resp ) {
                              var i_file = dojo.query( 'input[type=file]', aform )[0];
                              this._refreshattachs( true );
                              i_file.value = '';
                              dojo.publish( 'flash', [ 'hide' ] );
                          }
                         ),
              error    : dojo.hitch(
                          this,
                          function( errresp ) {
                              i_file.value = '';
                              dojo.publish(
                                'flash', [ 'error', 'Fail adding attachment !!', 2000 ] );
                          }
                         )
          });
      }
      dojo.stopEvent( e );
  },

  _delattach : function( span, e ) {
      var dform = dojo.byId( this.delform[0] );
      var i_attachid   = dojo.query( 'input[name=attach_id]', dform )[0];

      dojo.publish( 'flash', [ 'message', 'Deleting attachment ...' ] );
      i_attachid.value = dojo.attr( span, 'attach_id' );
      dojo.xhrPost({
          url      : dojo.attr( dform, 'action' ),
          form     : dojo.attr( dform, 'id' ),
          method   : 'post',
          load     : dojo.hitch(
                      this,
                      function( resp ) {
                          this._refreshattachs( true );
                          dojo.publish( 'flash', [ 'hide' ] );
                      }
                     ),
          error    : dojo.hitch(
                      this,
                      function( errresp ) {
                          dojo.publish( 'flash', [ 'error', 'Fail removing attachment !!', 2000 ] );
                      }
                     )
      });
      dojo.stopEvent( e );
  },
}
);


/*************************************************************************************
*********************************** Tags widget
**************************************************************************************/

dojo.declare( "zeta.Tags",
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  user: [],           // [ user_id, username ] who requested the operation.

  id: "",             // Tag node id

  class: "ml10 mt5 posr floatl", // Class attribute for widget

  addform: [],        // [ form-id, suburl ] to use for adding tags

  delform: [],        // [ form-id, suburl ] to use for deleting tags

  tagon: [],          // Optional [ obj-id, obj-name ] to add or delete from

  tags: {},           // Optional tags details

  url: "",            // url for fetching tag details, for AJAX request

  editable: false,    // Whether it is possible to add / delete tags

  parSpans: null,     // Node holding children of spans, one for each tag

  tagbox: null,       // Node representing the popup tag box

  tagit: null,        // Node representing the tagit interface.

  clsdisplayitem: 'dispinln',    // How to display each tag items.

  templateString: "<div></div>", // Gotcha : Dummy template, to avoid widget crash.

  postCreate : function() {
      dojo.place( this._makenode(), this.domNode, "last" ); // Instantiate the tag view
      this.parSpans = dojo.query( 'div[name=tagspans]', this.domNode )[0];

      if( this.editable ) {
          var i_text = dojo.query( "input[type=text]", dojo.byId( this.addform[0] ))[0];
          new zeta.Form({ formid: this.addform[0], onsubmit: dojo.hitch( this, '_addtag' ) });
          new zeta.Form({ formid: this.delform[0] });
          dojo.connect( this.tagit, 'onclick', this,
                        function (e) {
                            dojo.toggleClass( this.tagbox,'dispnone' );
                            i_text.focus();
                            dojo.stopEvent(e);
                        }
                      );
          dojo.connect( i_text, 'onblur', this,
                        function (e) {
                            dojo.toggleClass( this.tagbox,'dispnone' );
                            dojo.stopEvent(e);
                        }
                      );
      }
      this._refreshtags( false );
  },

  _makeforms: function( form, user, tagon ) {
      var fa    = dojo.create( "form",
                               { id: form[0], action: form[1], method: "post" },
                               dojo.create( "div", {} ),
                               "last"
                             );
      dojo.create( "input", { type: "hidden", name: "user_id", value: user[0] }, fa, "last" );
      tagon ?
          dojo.create( "input",
                       { type: "hidden", name: tagon[1], value: tagon[0] },
                       fa, "last"
                     )
          : null;
      dojo.create( "input", { type: "text", name: "tags", size: "16" },
                   dojo.create( "span", { class: "ftbox" }, fa, "last" ),
                   "last"
                 );
      return [ fa.parentNode ];
  },

  _makenode: function() {
      var divi = dojo.create( // iconize
                      "span",
                      { name: 'iconadd', class: "pl18 fggray fntbold pointer undrln",
                        style: { background : "transparent url(/zetaicons/tag_green.png) no-repeat scroll 0" },
                        innerHTML: 'Tag',
                      }
                 );
      var divs = dojo.create( "div", { class: "m2", name: "tagspans" } ); // Tag spans
      var diva = curvybox1( "bglsb", "bgaliceblue",
                            { class: "posa dispnone z99",
                              style: { top : "2.2em" },  name: "tagbox" },
                            this._makeforms( this.addform, this.user, this.tagon )
                          )
      var divd = curvybox1( "bglsb", "bgaliceblue",
                            { class: "posa dispnone z99",
                              style: { top : "2.2em" },  name: "tagbox" },
                            this._makeforms( this.delform, this.user, this.tagon )
                          )
      var div  = curvybox1( "bgwhite", "bggrn2", {}, [ divi, divs, diva, divd ] );
      this.tagbox = diva;
      this.tagit  = divi;
      return div;
  },

  _refreshtags: function( fetch ) {
      if( fetch ) {
          xhrget_obj(
              this.url, null, 'json', true, null, 
              dojo.hitch( this, function ( resp ) { this.tags = resp; } ),
              null
          );
      }
      /* Remove tags if absent in the fetched json object */
      var newtags = dojo.clone( this.tags );
      dojo.query( "div", this.parSpans ).forEach(
          function( n ) {
              var t = dojo.attr( n, 'tagname' );
              if( t in this.tags ) {
                  newtags[t] = null;
              } else {
                  this.parSpans.removeChild( n )
              }
          }, this
      );
      /* Add tags that are newly found */
      for ( t in this.tags ) {
          if ( newtags[t] == null ) { continue }
          href   = url_fortagname( t );
          span   = dojo.create(
                      'div',
                      { class: this.clsdisplayitem + " ml5 pl5",
                        tagname: t,
                        style: { borderLeft: '1px solid gray' }
                      } 
                   );
          anchor = dojo.create( 'a', {class:"fntsmall nodec mr2", href: href });
          anchor.innerHTML = t;
          dojo.place( anchor, span, 'first' );
          if ( this.editable ) {
              close = dojo.create( 'a', {class:"fntxsmall vsuper pointer"} );
              close.innerHTML = '&times; ';
              dojo.place( close, span, 'last' );
              dojo.connect( close, 'onclick', dojo.hitch( this, '_deltag', span ));
          }
          dojo.place( span, this.parSpans, 'first' );
      }
  },

  _addtag: function( e ) {
      var form   = dojo.byId( this.addform[0] );
      var i_tbox = dojo.query( "input[type=text]", form )[0];
      if ( i_tbox.value != '' ) {
          submitform( form, e );
          i_tbox.value = '';
          this._refreshtags( true );
          dojo.stopEvent( e );
      }
  },

  _deltag: function( span, e ) {
      var form    = dojo.byId( this.delform[0] );
      var i_tbox  = dojo.query( "input[type=text]", form )[0];
      var tagname = dojo.attr( span, 'tagname' )
      i_tbox.value = tagname
      submitform( form, e );
      i_tbox.value = '';
      this._refreshtags( true );
      dojo.stopEvent(e);
  }
}
);

/*************************************************************************************
*********************************** Config Tab Container
**************************************************************************************/
ct_template='\
<div class="bggrn2 pt10 pr5 pb5 pl5 br5">\
  <div name="content">\
      <div style="height: 1.4em;"></div>\
      <div class="bgwhite p10"></div>\
  </div>\
</div>\
'
dojo.declare( 'zeta.ConfigTabs',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  id: '',             // Id attribute the configuration tabs

  tabs: [],           // List of nodes to be contained as tabs

  currtab: null,      // Current tab that is being shown

  currtitle: null,    // Current title node that is being shown

  templateString: ct_template, 

  postCreate: function() {
      this.contnode = dojo.query( "[name=content]", this.domNode )[0];
      var titles = this.contnode.childNodes[1]
      var contnr = this.contnode.childNodes[3]
      dojo.forEach(
          this.tabs,
          function( tab ) {
              var tn = this._maketitle( tab  )
              dojo.toggleClass( tab, "dispnone", true )
              dojo.place( tn, titles, "last" );
              dojo.place( tab, contnr, "last" );
              if( (this.currtab==null) && dojo.hasAttr( tab, "selected" )) {
                  this._switchtab( tn, tab );
              }
          }, this
      );
  },

  _maketitle: function( tab ) {
      var title = dojo.attr( tab, "title" )
      var n = dojo.create(
                  "span",
                  { class: "p3 mr10 fntbold fntsmall fgblue pointer",
                    style: { MozBorderRadiusTopleft : '5px',  MozBorderRadiusTopright : '5px' },
                    innerHTML: title }
              )
      dojo.connect( n, "onclick", dojo.hitch( this, "_switchtab", n, tab ) )
      return n 
  },

  _switchtab: function( tn, tab, e ) {
      var contnr = this.contnode.childNodes[3];
      if( this.currtitle ) { 
          dojo.toggleClass( this.currtitle, "bgwhite", false );
          dojo.toggleClass( this.currtitle, "fgblue", true );
          dojo.toggleClass( this.currtab, "dispnone", true );
      }
      dojo.toggleClass( tn, "bgwhite", true );
      dojo.toggleClass( tn, "fgblue", false );
      dojo.toggleClass( tab, "dispnone", false );
      this.currtab     = tab;
      this.currtitle   = tn;
  }

}
);

/*************************************************************************************
*********************************** Menu Item
**************************************************************************************/

dojo.declare( "zeta.MenuItem",
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{  
  content: '',    // Menu item name, can also be a valid html string

  _style: { padding: "2px 5px" },

  style: {},    // style for menu item

  templateString: '<div dojoAttachEvent="onclick:onClick"></div>',

  postCreate: function() {
      var l     = this.content ? this.content : "...";
      var style = l == "..." ? { color: "gray" } : {};

      if( dojo.isString( l ) && (l[0] != '<') ) {
          this.domNode.innerHTML = l;
      } else {                                        // Is html ?
          dojo.place( l, this.domNode, "first" );
      }
      dojo.style( this.domNode, dojo.mixin( style, this._style, this.style ));
  },

  destroy: function() {
  },

  onClick: function( e ) { return; }
}
);

/*************************************************************************************
*********************************** Menu
**************************************************************************************/


dojo.declare( "zeta.Menu",
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  _items: [],         // List of items added to the Menu.

  title: "",          // Menu title

  _titlestyle: { background: "#f3f6f0" }, // Style attribute for title item.

  titlestyle: {},     // Style attribute for title item.

  targetNodes: [],    // Target nodes for which the menu should be activated

  style: {},          //

  _style: { position: "fixed", border: "2px solid #efefef",
            background: "#FFFFFF", paddingTop: "2px", paddingBottom: "2px" },

  _visible: false,

  templateString: '<div></div>',

  postCreate: function() {
      dojo.forEach(
          this.targetNodes,
          function( n ) {
              n = dojo.isString( n ) ? dojo.byId( n ) : n;
              dojo.connect( n, "onclick", this, "onClick" );
          },
          this
      );
      if( this.title ) {
          this.addItem( 
                  new zeta.MenuItem(
                      { content: this.title, 
                        style: dojo.mixin( {}, this._titlestyle, this.titlestyle )
                      })
          );
      }
      dojo.style( this.domNode, dojo.mixin( {}, this._style, this.style ));
      dojo.connect( this.domNode, "onblur", this, "onBlur" );
      dojo.fx.wipeOut({ node : this.domNode, duration : 0 }).play();
      dojo.place( this.domNode, dojo.body(), "last" );
  },

  addItem: function( w ) {
      var items = this._items;
      items[items.length] = w;
      dojo.place( w.domNode, this.domNode, "last" );
  },

  destroy: function() {
  },

  onClick: function( e ) {
      if( this._visible ) {
          dojo.fx.wipeOut({ node : this.domNode, duration : 20 }).play();
          this._visible = false;
      } else {
          box = dojo.coords( e.currentTarget );
          dojo.marginBox(this.domNode, { l: box.x, t: (box.y+box.h+3) });
          dojo.style( this.domNode, { minWidth: box.w })
          dijit.focus( this.domNode );
          dojo.fx.wipeIn({ node : this.domNode, duration : 20 }).play();
          this._visible = true;
      }
      dojo.stopEvent( e );
  },

  onBlur: function() {
      dojo.fx.wipeOut({ node : this.domNode, duration : 20 }).play();
      this._visible = false;
  }
}
);

/*************************************************************************************
*********************************** Source Explorer
**************************************************************************************/


dir_template = '\
<div name="dir" class="ml5">\
  <div class="fntsmall pt2 pb2">\
      <div class="fgblue dispinln pointer"></div>\
      <span class="dispnone fntxsmall fntitalic">Loading ...</span>\
  </div>\
  <ul class="dispnone" \
      style="border-left: 1px dotted #d6d6d6; margin : 0px;\
             list-style: none outside none; padding-left : 5px"></ul>\
</div>\
'

dojo.declare( "zeta.VcsDir",
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  w_explorer : null,  // VcsExplorer widget object

  dirlist: null,      // dojo.data store object

  dirname: '',        // Dirname to display

  repos_path: '',     // Relative path to repository root
 
  closed: true,       // Whether the folder is closed

  listurl:'',         // URL to fetch the directory listing.

  subdirs: null,      // Subdir widgets.

  h_onclick: null,    // OnClick connection handle

  templateString: dir_template,

  postCreate: function() {
      this.subdirs = new Array();
      this.div  = this.domNode.childNodes[1].childNodes[1];
      this.span = this.domNode.childNodes[1].childNodes[3];
      this.ul   = this.domNode.childNodes[3];
      this.strclosed = '&#8330; '+this.dirname;
      this.stropened = '&#8331; '+this.dirname;
      this.strdirname= '&ensp '+this.dirname;
      this.div.innerHTML = this.strdirname;
      
      // Fetch the listing.
      this.dirlist = {
          store      : new dojo.data.ItemFileReadStore({
                           url             : this.listurl,
                           clearOnClose    : true,
                           urlPreventCache : true
                       }),
          fetch      : ddr_fetch,
          itembyID   : ddr_itembyID,
          itemValues : ddr_itemValues,
          items      : null
      };
  },

  onComplete: function( items, req ) {
      this.dirlist.items   = items;

      dojo.publish( 'flash', [ 'hide' ] );
      dojo.toggleClass( this.span, "dispnone", true );  // Loading ...

      // Setup Directory view
      this.widgetifydirs( this.dirlist.store.getValues( items[0], 'dirs' ));
      if( this.closed == true ) {
          this.div.innerHTML = this.subdirs.length ? this.strclosed : this.strdirname;
      }
      if(! this.h_onclick ) {
          this.h_onclick = dojo.connect( this.div, 'onclick', this, 'onClick' );
      }
  },

  onClick: function( e ) {
      // List subdirs.
      if( this.closed && this.subdirs.length ) {
          this.div.innerHTML = this.stropened;
          this.closed = false;
          dojo.toggleClass( this.ul, 'dispnone', false );

          // Fetch subdirectories.
          dojo.forEach(
              this.subdirs,
              function( d ) {
                  d.dirlist.store.close();
                  d.dirlist.fetch({ onComplete: dojo.hitch( d, 'onComplete' ) });
                  dojo.toggleClass( d.span, "dispnone", false ); // Loading ...
              },
              this
          );
      } else {
          this.div.innerHTML = this.subdirs.length ? this.strclosed : this.strdirname;
          this.closed = true;
          dojo.toggleClass( this.ul, 'dispnone', true );
      }

      // List files in directory ...
      var items = this.dirlist.items;
      var files = items ? this.dirlist.store.getValues( items[0], 'files' ) : null;
      this.w_explorer.highltdir( this );
      if( files ) {
          dojo.publish( 'listthesefiles', [ files, this.repos_path ] );
      }

      // save this directory
      this.w_explorer.savestate(
            this.fragmentize( this.w_explorer.rootdir, this.repos_path )
      )
      dojo.stopEvent( e );
  },

  widgetifydirs: function( subdirlist ) {
      // Widgetify only if the subdirectories are fetched new.
      if( this.subdirs.length == 0 ) {
          dojo.forEach(
              subdirlist,
              function( dir ) {
                  var w_dir   = new zeta.VcsDir({
                                      w_explorer: this.w_explorer,
                                      dirname: dir[0],
                                      listurl: dir[1],
                                      repos_path: dir[2]
                                });
                  this.subdirs[ this.subdirs.length ] = w_dir;
                  dojo.place( w_dir.domNode, this.ul, "last" );
              },
              this
          );
      }
  },

  taildirs: function( walkdirs ) {
      var head = walkdirs ? walkdirs[0] : null;
      var tail = new Array();

      if( walkdirs.length > 1 ) {
          for( i=1; i < walkdirs.length; i++ ) {
              tail[tail.length] = walkdirs[i];
          }
      }
      return tail
  },

  fragmentize: function() {
      var arr = new Array();
      for( i=0; i < arguments.length; i++ ) {
          arg = arguments[i];
          if( arg ) {
            arr[ arr.length ] = arg
          }
      }
      return arr.join('/')
  },

  onCompleteWalk: function( walkdirs, view, save, items, req ) {
      this.dirlist.items   = items;

      // Visual toasters
      dojo.publish( 'flash', [ 'hide' ] );
      dojo.toggleClass( this.span, "dispnone", true );  // Loading ...

      // Setup Directory view
      this.widgetifydirs( this.dirlist.store.getValues( items[0], 'dirs' ));
      if( view ) {
          this.closed = false;
          dojo.toggleClass( this.ul, 'dispnone', false );
          if( this.subdirs.length ) {
              this.div.innerHTML = this.stropened;
          }
      } else {
          this.div.innerHTML = this.subdirs.length ? this.strclosed : this.strdirname;
          this.closed = true;
          dojo.toggleClass( this.ul, 'dispnone', true );
          dojo.toggleClass( this.ul, 'dispnone', true );
      }
    
      // Walk remaining dirs, along with simple subdir fetches.
      walkdirs = this.taildirs( walkdirs );
      dojo.forEach(
          this.subdirs,
          function( d ) {
              if(! d.h_onclick ) {
                  d.h_onclick = dojo.connect( d.div, 'onclick', d, 'onClick' );
              }
              dojo.toggleClass( d.span, "dispnone", false ); // Loading ...
              d.dirlist.store.close();
              if( view && walkdirs.length && d.dirname == walkdirs[0] ) {
                  d.dirlist.fetch({
                        onComplete: dojo.hitch( d, 'onCompleteWalk',
                                                walkdirs, true, save
                                              )
                  });
              } else if( view )  {
                  d.dirlist.fetch({
                        onComplete: dojo.hitch( d, 'onCompleteWalk',
                                                walkdirs, false, save
                                              )
                  });
              }
          },
          this
      );
      
      if( view && walkdirs.length == 0 ) {
          // List files in directory ...
          var items = this.dirlist.items;
          var files = items ? this.dirlist.store.getValues( items[0], 'files' ) : null;
          this.w_explorer.highltdir( this );
          if( files ) {
              dojo.publish( 'listthesefiles', [ files, this.repos_path ] );
          }
          if( save ) {
              this.w_explorer.savestate(
                    this.fragmentize( this.w_explorer.rootdir, this.repos_path )
              )
          }
      }
  },

}
);


ve_template='\
<div>\
  <div class="bggrn1" style="height : 1px ; margin: 0px 4px 0px 4px;" ></div>\
  <div class="bggrn1" style="height : 1px ; margin: 0px 2px 0px 2px;" ></div>\
  <div class="bggrn1" style="height : 1px ; margin: 0px 1px 0px 1px;"></div>\
  <div class="bggrn1">\
      <div class="posr bggrn1 p5" name="content" style="height: 500px;">\
          <div name="header" class="mb5" style="height: 20px">\
              <div class="floatr"></div>\
              <div>\
                  <span name="path"></span>\
                  <span name="mount">\
                        <span class="ml5 fgblue pointer"></span> \
                        <span class="posa z99" style="top: 2em;"></span> \
                  </span>\
              </div>\
          </div>\
          <div class="posa bgwhite overa" style="width: 30%; height: 480px;" name="dircol">\
              <table style="width: 100%;">\
                  <tr class="fntbold bggrn2">\
                      <th style="padding: 2px 5px 2px 2px;">Directories</th>\
                  </tr>\
                  <tr class="bgwhite">\
                      <td><ul style="list-style : none outside none; padding-left: 10px;"></ul></td>\
                  </tr>\
              </table>\
          </div>\
          <div class="posa bgwhite overa ml10" style="left:30%; width: 69%; height: 480px" name="filecol">\
              <table style="width: 100%;">\
                  <tr class="fntbold bggrn2">\
                      <th style="padding: 2px 5px 2px 2px; border-left : 1px solid gray;">\
                          Filename</th>\
                      <th style="padding: 2px 5px 2px 2px; border-left : 1px solid gray; width: 4em;">\
                          Revision</th>\
                      <th style="padding: 2px 5px 2px 2px; border-left : 1px solid gray; width: 4em;">\
                          Size</th>\
                      <th style="padding: 2px 5px 2px 2px; border-left : 1px solid gray; width: 6em;">\
                          Date</th>\
                      <th style="padding: 2px 5px 2px 2px; border-left : 1px solid gray; width: 18em;">\
                          Author</th>\
                  </tr>\
              </table>\
          </div>\
      </div>\
  </div>\
  <div class="bggrn1" style="height : 1px ; margin: 0px 1px 0px 1px;"></div>\
  <div class="bggrn1" style="height : 1px ; margin: 0px 2px 0px 2px;" ></div>\
  <div class="bggrn1" style="height : 1px ; margin: 0px 4px 0px 4px;" ></div>\
</div>\
'

dojo.declare( "zeta.VcsExplorer",
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  title: '',          // Menu title

  vcstype: '',        // VCS Type

  rootpath: '',       // files displayed under rootpath

  revno_p: '',        // Previous revision number

  revno: '',          // Revision number of the source to browse

  revno_n: '',        // Next revision number

  rootdir: '',        // Root dir.

  listrootdir: '',    // List root dir.

  w_root: '',         // Root dir widget.

  curdir: null,       // Current dir widget

  walkdirs: [],       // Walk directories

  mountpoints: [],    // Array of mountpoints for this repository

  curr_mountpath: '',

  curr_mountid: '',

  templateString: ve_template,

  postCreate: function() {
      this.n_cont   = dojo.query( 'div[name=content]', this.domNode )[0];
      this.n_hdr    = this.n_cont.childNodes[1];
      this.n_path   = this.n_hdr.childNodes[3].childNodes[1];
      this.n_mount  = this.n_hdr.childNodes[3].childNodes[3];
      this.n_dircol = this.n_cont.childNodes[3];
      this.n_filecol= this.n_cont.childNodes[5];
      this.n_rootdir= dojo.query( 'ul', this.n_dircol )[0];

      // Create pagination for previous and next revision
      if( this.revno_p[0] ) {
          dojo.create("a", { href: this.revno_p[1], 
                             innerHTML: '&#8249; '+this.revno_p[0], class: "mr5" },
                       this.n_hdr.childNodes[1], "last" )
      }
      dojo.create("strong", { innerHTML: this.revno, class: "ml2 mr2" },
                   this.n_hdr.childNodes[1], "last" )
      if( this.revno_n[0] )
      {
          dojo.create("a", { href: this.revno_n[1], 
                             innerHTML: this.revno_n[0]+' &#8250;', class: "ml5 mr2" },
                       this.n_hdr.childNodes[1], "last" )
      }

      // Create Header elements for the explorer window
      var a = '( ' + this.vcstype + ': ' + this.rootpath + ' ) ';
      dojo.create("strong", { innerHTML: a, class: "ml5" }, this.n_path, "first" )
      this.hl_path = dojo.create( "strong", { innerHTML: '/', class: "fggray fntbold ml5" },
                                  this.n_path, "last" )

      // Instantiate the root.
      this.w_root = new zeta.VcsDir({ w_explorer: this,
                                      dirname: this.rootdir,
                                      listurl: this.listrootdir,
                                      repos_path: ''
                                   })

      dojo.place( this.w_root.domNode, this.n_rootdir, "last" );

      // Subscribe to file listing.
      dojo.subscribe( 'listthesefiles', this, 'listfile' );

      // handle mounting
      dojo.place( this.n_mountpopup, this.n_mount.childNodes[3], 'last' );
      dojo.connect( this.n_mount.childNodes[1], 'onclick', this, this.onMount );
      dojo.connect( dojo.query( 'div[name=close]', this.n_mountpopup )[0],
                    'onclick',
                    this,
                    function(e) {
                      dojo.toggleClass( this.n_mountpopup, 'dispnone', true );
                    }
                  );
      dojo.subscribe( 'mounted', this, this.mounted );

      // Initialize Bookmarking and back/forward navigation !
      this.backinit( this.rootdir );
      this.checkurl( this.rootdir );
  },

  listfile: function( files, repos_path ) {
      var n_table = this.n_filecol.childNodes[1];
      var n_trs   = dojo.query( 'tr', n_table );

      this.hl_path.innerHTML = repos_path.replace( /\/\//, '/' ).replace( /\//g, ' /' );

      // Destory the previous file listing
      for( i=1; i < n_trs.length; i++ ) {
          dojo.destroy( n_trs[i] );
      }

      // Populate with new file listing
      dojo.forEach( files,
          function( file ) {
              dojo.place( this._make_filetr( file ), n_trs[0].parentNode, "last" );
          },
          this
      );

      // Check for mount points
      var mp = this.mountpoint( repos_path );
      if( mp.id ) {
        this.n_mount.childNodes[1].innerHTML = 'UnMount';
        this.curr_mountpath = mp.repospath
        this.curr_mountid   = mp.id
      } else {
        this.n_mount.childNodes[1].innerHTML = 'Mount';
        this.curr_mountpath = repos_path
      }
  },

  backinit: function( rootdir ) {
      var fetchdir = dojo.hitch( this, "fetchdir" );
      // Add the back function to the fetchdir using dojo.extend
      dojo.extend(
          this.backStateObject,
          { // Specify function to call when browser back button is pushed
            back: function() {
                // Can't use "this" in the function name, but can use it for func parameter
                fetchdir( false, this.dirpath );
            },
            forward: function(){
                // Use the same function to get back to page w forward button
                fetchdir( false, this.dirpath );
            }
          }
      );
      var initState = new this.backStateObject( '' );
      dojo.back.setInitialState( initState );
  },

  checkurl: function( rootdir ) {
      // Check for bookmark in the current URL and simply, navigate
      var appUrl = window.location.href; // bookmark starts with the # character
      var res    = new Array();
      var save   = false;
      res = appUrl.split("#");
      if( res.length == 2 ){
          frag = res[1].indexOf( '%' ) == -1 ? res[1] : decodeURIComponent(res[1]);
      } else if( rootdir ) {
          frag = rootdir.indexOf( '%' ) == -1 ? rootdir : decodeURIComponent(rootdir);
          save = true;
      }
      frag != null ? this.fetchdir( save, frag ) : null;
  },

  backStateObject: function( dirpath ) {
      this.dirpath  = dirpath;
      this.changeUrl = dirpath;
  },

  fetchdir : function( save, frag ) {
      var dirs = frag.split('/');
      this.w_root.dirlist.store.close();
      this.w_root.dirlist.fetch({
            onComplete: dojo.hitch(
                           this.w_root, 'onCompleteWalk', dirs, true, save
                        )
      });
  },

  savestate: function( repos_path ) {
      var navstate = new this.backStateObject( repos_path );
      dojo.back.addToHistory( navstate );
  },

  highltdir: function( w_vdir ) {
      this.curdir ? dojo.toggleClass( this.curdir.div.parentNode, 'bggrn2', false )
                  : null;
      dojo.toggleClass( w_vdir.div.parentNode, 'bggrn2', 'true' )
      this.curdir = w_vdir;
  },

  mountpoint: function( repos_path ) {
      var mountpoints  = this.mountpoints;
      var rc = { id : false, repospath: '' };
      for( i=0; i < mountpoints.length; i++ ){
          if( repos_path == mountpoints[i][1] ){
              rc = { id : mountpoints[i][0], repospath: mountpoints[i][1] };
              break;
          }
      }
      return rc
  },

  onMount: function( e ) {
      var n = e.currentTarget;
      if( n.innerHTML == 'Mount' ) {
          var i_name = dojo.byId( 'name' );
          var i_repospath = dojo.byId( 'repospath' );
          i_repospath.value = this.curr_mountpath;
          if( this.curr_mountpath ) {
              dojo.toggleClass( this.n_mountpopup, 'dispnone', false );
              i_name.focus();
          }
      } else {
          var i_mountid = dojo.byId( 'mount_id' );
          i_mountid.value = this.curr_mountid;
          submitform( this.n_unmountform, e );
          n.innerHTML = 'Mount'
      }
      dojo.stopEvent(e);
  },

  mounted: function() {
      this.n_mount.childNodes[1].innerHTML = 'UnMount';
  },

  _make_filetr: function( file ) {
      var n_tr    = dojo.create( "tr", {} );
      // Filename
      dojo.create( "a", {href: file[8], innerHTML: file[7]},
                   dojo.create( "td", { style: { padding: "2px 5px 2px 2px", 
                                                 borderBottom: "1px dotted gray" }},
                                n_tr, "last" ),
                   "last" );
      // Revision
      dojo.create( "td", {innerHTML: file[0], 
                          style: { padding: "3px 5px 3px 2px", borderBottom: "1px dotted gray" }},
                   n_tr, "last" )
      // Size
      dojo.create( "td", {innerHTML: file[4], 
                          style: { padding: "3px 5px 3px 2px", borderBottom: "1px dotted gray" }},
                   n_tr, "last" )
      // Date
      dojo.create( "td", {innerHTML: file[5], 
                          style: { padding: "3px 5px 3px 2px", borderBottom: "1px dotted gray" }},
                   n_tr, "last" )
      // Author
      dojo.create( "td", {innerHTML: file[3], 
                          style: { padding: "3px 5px 3px 2px", borderBottom: "1px dotted gray" }},
                   n_tr, "last" )
      return n_tr
  }
}
);


/*************************************************************************************
*********************************** Comments
**************************************************************************************/

zc_template = '\
<div class="comment mt5 mb10 mr2" style= "border-left : 3px solid #D6D6D6;"> \
   <div class="pl5 bggray1 cmthdr" \
        style="height: 1.5em; border-top: 1px solid #D6D6D6;"></div> \
   <div class="pl10 mr10 cmttext"></div>\
</div>\
'

dojo.declare( 'zeta.Comment',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  zcw: null,                      // Comments Wrapper Widget

  item: {},                       // An item from data store

  store: null,                    // dojo.data store for the item

  colormap: {},                   // Author color map

  inreply: false,                 // If the comment is shown as reply, 
                                  // provide a different styling

  templateString: zc_template,

  postCreate: function() {
      var n_header = this.domNode.childNodes[1];
      var n_text   = this.domNode.childNodes[3];
      var item     = this.item;

      var datestr      = this.store.getValue( item, 'datestr' );
      var version_id   = this.store.getValue( item, 'version_id' );
      var item_id      = this.store.getValue( item, this.zcw.identity );
      var commentbyurl = this.store.getValue( item, 'commentbyurl' );
      var commentby    = this.store.getValue( item, 'commentby' );
      var html         = this.store.getValue( item, 'html' );
      var replies      = this.store.getValues( item, 'replies' );

      var datestr  = version_id ?
                          ', on ' + datestr + ', for version ' + version_id
                          : ', on ' + datestr;

      // Comment header
      dojo.attr( this.domNode, 'cmtid', item_id );

      if ( this.inreply == false ) {
          var n_reply  = dojo.create( 'div', { class : 'posr floatr ml5 pointer fgblue',
                                                innerHTML: ' | Reply'},
                                      n_header, 'last' );
          var n_fold   = dojo.create( 'div',  { class: 'posr floatr ml5 pointer fgblue',
                                                innerHTML: 'Fold'},
                                      n_header, 'last' );
          dojo.connect( n_fold,  'onclick', dojo.hitch( this, this.onfold, this.zcw ));
          dojo.connect( n_reply, 'onclick', dojo.hitch( this, this.onreply, this.zcw ));
      }

      // Author
      dojo.create( 'a',    { href  : commentbyurl,
                             class : 'nodec fntbold',
                             style : { color : this.colormap[commentby] },
                             innerHTML: commentby },
                             n_header, 'last' );
      // Date string with version.
      dojo.create( 'span', { class : 'ml2 fntitalic', innerHTML: datestr },
                             n_header, 'last' );
      // And the actual comment text in html
      n_text.innerHTML = html;

      if( this.zcw.replyview ) {
          // Recursively build comment widgets for replies as well.
          this.replycntnr = dojo.create( "div", {}, n_text, "last" )
          dojo.forEach( replies,
              dojo.partial(
                  function( zcw, node, store, item ) {
                      var replycmt = dojo.create( "div", {}, node, "last" )
                      new zeta.Comment({
                              zcw: zcw,
                              item: item,
                              store: store,
                              colormap: zcw.colormap,
                              inreply: true
                          }, replycmt )
                  },
                  this.zcw, this.replycntnr, this.store
              )
          );
      }
  },

  onfold: function( zcw, e ) {
      var n_text = dojo.query( 'div.cmttext', this.domNode )[0];
      var n_hdr  = dojo.query( 'div.cmthdr', this.domNode )[0];
      var n_fold = n_hdr.childNodes[1];
      dojo.toggleClass( n_text, 'dispnone' );
      n_fold.innerHTML = n_fold.innerHTML == 'Fold' ? 'Unfold' : 'Fold';
      dojo.stopEvent( e );
  },

  onreply: function( zcw, e ) {
      if( e.target.innerHTML == ' | Reply' ) {
          e.target.innerHTML = ' | Cancel';
          // Revert the reply-cancel tigger for the previous comment.
          if( zcw.currnreply ) {
              zcw.currnreply.innerHTML = ' | Reply';
          }
          
          dojo.place( zcw.rpcntnr, this.domNode, 'last' );
          dojo.toggleClass( zcw.rpcntnr, 'dispnone', false );

          /* Set up the form */
          var inp_rply = dojo.query( 'input[name=replytocomment_id]', zcw.rpform )[0];
          if( inp_rply ) {
              inp_rply.value = dojo.attr( this.domNode, 'cmtid' )
          }
          dojo.query( 'textarea[name=text]', zcw.rpcntnr )[0].focus();
          zcw.currnreply = e.target;
      } else {
          e.target.innerHTML = ' | Reply';
          dojo.toggleClass( zcw.rpcntnr, 'dispnone', true );
          this.domNode.removeChild( zcw.rpcntnr );
          zcw.currnreply = null;
      }
      dojo.stopEvent( e );
  }

}
);


zcc_template = '\
<div class="commentcontainer">\
  <div class="posr floatr pointer fgblue p5"> | Conversation</div>\
  <div class="posr floatr pointer fgblue p5">AddComment</div>\
  <h3 class="p5 bggray1" style="border-top : 1px solid #D6D6D6";>\
      <a name="comments"></a>\
  </h3>\
  <div></div>\
</div>\
'

dojo.declare( 'zeta.CommentContainer',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  
  ifrs_comments: null,            // dojo.data read store for comments.

  ifrs_rcomments: null,           // dojo.data read store for reply-comments.

  crformid: null,                 // Form Id for Adding new comment

  rpformid: null,                 // Form Id for Reply to a comment

  edformid: null,                 // Form Id for Editing a comment

  sortby: '',                     // Sortby id.

  identity:'',                    // Identity property for each item.
                                  // Gotcha : This is required because of AJAX load optimizations.

  w_comments: [],                 // List of comments

  replyview: false,               // Initial view type

  colormap: {},                   // Author color map

  currnreply: null,               // Current comment being replied
  
  templateString: zcc_template,

  postCreate: function() {
      this.n_viewtype = this.domNode.childNodes[1];
      this.n_addcmt   = this.domNode.childNodes[3];
      this.n_title    = this.domNode.childNodes[5];
      this.n_cmtsport = this.domNode.childNodes[7];

      /* Comment forms - with allfields=true */
      new zeta.Form({ formid: this.crformid,
                      onsubmit: dojo.hitch( this, 'crcmt_onsubmit' ),
                      allfields: true });
      new zeta.Form({ formid: this.rpformid,
                      onsubmit: dojo.hitch( this, 'rpcmt_onsubmit' ),
                      allfields: true });
      new zeta.Form({ formid: this.edformid,
                      onsubmit: dojo.hitch( this, 'edcmt_onsubmit' ),
                      allfields: true });
      this.crform  = dojo.getObject( 'form_' + this.crformid );
      this.edform  = dojo.getObject( 'form_' + this.edformid );
      this.rpform  = dojo.getObject( 'form_' + this.rpformid );
      this.crcntnr = this.crform.parentNode;
      this.edcntnr = this.edform.parentNode;
      this.rpcntnr = this.rpform.parentNode;
      dojo.toggleClass( this.crcntnr, 'dispnone', true );
      dojo.toggleClass( this.edcntnr, 'dispnone', true );
      dojo.toggleClass( this.rpcntnr, 'dispnone', true );
      this.edcntnr.parentNode.removeChild( this.edcntnr );
      this.rpcntnr.parentNode.removeChild( this.rpcntnr );
      this.crcntnr.parentNode.removeChild( this.crcntnr );
      dojo.place( this.crcntnr, this.domNode, 6 );

      /* Create Comment */
      toggler(
          this.n_addcmt, this.crcntnr, "Cancel", "AddComment", true,
          dojo.hitch(
              this,
              function( n_trig, n, v_text, h_text ) {
                 dojo.query( 'textarea[name=text]', this.crcntnr )[0].focus();
              }
          )
      );

      /* View Type */
      dojo.connect( this.n_viewtype, 'onclick', this, this.onviewtype );
                    
      if( this.ifrs_comments.staticstore ) {
          this.ifrs_comments.staticfetch({
              onComplete : dojo.hitch( this.ifrs_comments, this.ifrs_oncomplete,
                                       this, this.ifrs_comments.staticstore ),
              sort : [ { attribute : this.sortby } ]
          });
      } else {
          this.ifrs_comments.fetch({
              onComplete : dojo.hitch( this.ifrs_comments, this.ifrs_oncomplete,
                                       this, this.ifrs_comments.store ),
              sort : [ { attribute : this.sortby } ]
          });
      }
  },

  refreshview: function( replyview ) {
      this.replyview = replyview ? true : false;
      // Hide the add comment form.
      this.crcntnr.hide();
      if( this.replyview ) {
          this.ifrs_rcomments.store.close();                      
          this.ifrs_rcomments.fetch({
              onComplete : dojo.hitch( this.ifrs_rcomments, this.ifrs_oncomplete,
                                       this, this.ifrs_rcomments.store ),
              sort : [ { attribute : this.sortby } ]
          })
          this.n_viewtype.innerHTML = ' | Normal';
      } else {
          this.ifrs_comments.store.close();                      
          this.ifrs_comments.fetch({
              onComplete : dojo.hitch( this.ifrs_comments, this.ifrs_oncomplete,
                                       this, this.ifrs_comments.store ),
              sort : [ { attribute : this.sortby } ]
          })
          this.n_viewtype.innerHTML = ' | Conversation';
      }
  },

  onviewtype: function( e ) {
      if( e.target.innerHTML == ' | Conversation' ) {
        this.refreshview( true );
      } else if( e.target.innerHTML == ' | Normal' ) {
        this.refreshview( false );
      }
  },

  crcmt_onsubmit: function( e ) {
      submitform( this.crform, e );
      this.refreshview( this.replyview );
      dojo.stopEvent( e );
  },

  rpcmt_onsubmit: function( e ) {
      submitform( this.rpform, e );
      dojo.stopEvent( e );
      this.refreshview( this.replyview );
  },

  edcmt_onsubmit : function( e ) {
      submitform( this.edform, e );
      this.refreshview( this.replyview );
      dojo.stopEvent( e );
  },

  ifrs_oncomplete : function( zcw, store, items, req ) {
      // This function executes under the ifrs_* object containing the
      // dojo.data store.
      var no_of_cmts = 0;
      dojo.publish( 'flash', [ 'hide' ] );
      this.items = items; // `this` refers to the ifrs_* object containing dojo.data store

      // Calculate author color and no of comments count.
      zcw.n_cmtsport.innerHTML = '';
      for( i=0; i < this.items.length; i++ ){
          var commentby = store.getValue( this.items[i], 'commentby' );
          var count_replies = store.getValues( this.items[i], 'replies' ).length;
          zcw.colormap[commentby] = '';
          no_of_cmts += 1;
          if( count_replies ) {
              no_of_cmts += count_replies
          }
      }
      zcw.colormap = colormaps(keys( zcw.colormap ));
      zcw.n_title.childNodes[1].innerHTML = no_of_cmts + ' Comments';

      dojo.forEach(
          this.items,
          dojo.partial(
              function( zcw, store, item ) {
                  var n_cmt = dojo.create( "div", {}, zcw.n_cmtsport, "last" );
                  var w     = new zeta.Comment({
                                      zcw: zcw,
                                      item: item,
                                      store: store,
                                      colormap: zcw.colormap
                                  }, n_cmt );
                  zcw.w_comments[zcw.w_comments.length] = w;
              },
              zcw, store 
          )
      );
      adjust_upheight();
      // Encode external links with a trailing icon.
      linkencode();
  }

}
);

/*************************************************************************************
*********************************** Voting
**************************************************************************************/

voting_template = '\
  <span class="ml5 mr5">\
      <span name="upvote" class="upvote pointer fntserif" title="Up-vote"></span>\
      <span name="downvote" class="downvote pointer fntserif" title="Down-vote"></span>\
      <span name="upvotes" class="ml5 pl3 fggreen" style="border-left: 2px solid gray"></span>\
      <span name="downvotes" class="fgred"></span>\
  </span>\
'
dojo.declare( 'zeta.Voting',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  formid: '',         // Name of the form to use for submission.

  upvotes: 0,         // Number of up votes

  downvotes: 0,       // Number of up votes

  currvote: '',       // Number of up votes

  templateString: voting_template,

  postCreate: function() {
      new zeta.Form({ normalsub: true, formid: this.formid });

      this.n_form      = dojo.getObject( 'form_' + this.formid );
      this.i_votedas   = dojo.query( 'input[name="votedas"]', this.n_form )[0]
      this.n_upvote    = this.domNode.childNodes[1]
      this.n_downvote  = this.domNode.childNodes[3]
      this.n_upvotes   = this.domNode.childNodes[5]
      this.n_downvotes = this.domNode.childNodes[7]

      this.n_upvotes.innerHTML   = this.upvotes + ' upvotes, ';
      this.n_downvotes.innerHTML = this.downvotes + ' downvotes ';

      if( this.currvote == 'up' ) {
          dojo.toggleClass( this.n_upvote, 'upvoted', true );
      } else if( this.currvote == 'down' ) {
          dojo.toggleClass( this.n_downvote, 'downvoted', true );
      }
      dojo.connect( this.n_upvote, 'onclick', 
                    dojo.hitch( this, this.onclick, 'up' )
                  )
      dojo.connect( this.n_downvote, 'onclick', 
                    dojo.hitch( this, this.onclick, 'down' )
                  )
  },

  onclick: function( vote, e ) {
      if( this.currvote != vote ) {
          // Adjust the vote counts
          if( this.currvote == 'up' ) {
              this.upvotes -= 1;
          } else if( this.currvote == 'down' ) {
              this.downvotes -= 1;
          }
          // Setup form field and current vote status
          if( vote == 'up' ) {
              dojo.publish( 'flash', [ 'message', 'Voting up ...' ] );
              this.upvotes += 1;
              this.i_votedas.value = 'up';
              this.currvote = 'up';
          } else if ( vote == 'down' ) {
              dojo.publish( 'flash', [ 'message', 'Voting down ...' ] );
              this.downvotes += 1;
              this.i_votedas.value = 'down';
              this.currvote = 'down';
          }
          // Post the form
          dojo.xhrPost({
              url      : dojo.attr( this.n_form, 'action' ),
              form     : dojo.attr( this.n_form, 'id' ),
              method   : 'post',
              load     : dojo.hitch(
                          this,
                          function( resp ) {
                              dojo.publish( 'flash', [ 'hide' ] );
                              this.n_upvotes.innerHTML   = this.upvotes + ' upvotes, ';
                              this.n_downvotes.innerHTML = this.downvotes + ' downvotes ';
                              if( this.currvote == 'up' ) {
                                  dojo.toggleClass( this.n_downvote, 'downvoted', false );
                                  dojo.toggleClass( this.n_upvote, 'upvoted', true );
                              }else if( this.currvote == 'down' ) {
                                  dojo.toggleClass( this.n_upvote, 'upvoted', false );
                                  dojo.toggleClass( this.n_downvote, 'downvoted', true );
                              }
                          }
                         ),
              error    : dojo.hitch(
                          this,
                          function( errresp ) {
                              dojo.publish( 'flash', [ 'error', 'Voting failed !!', 2000 ] );
                          }
                         )
          });
      }
  }

}
);

/*************************************************************************************
*********************************** ToolTips
**************************************************************************************/

tt_template = '\
  <div class="ml50 mr50 dispnone">\
      <div class="bgyellow1 brbl5 brbr5" \
           style="font-family: Helvetica, sans-serif;"> \
          <div name="tabs" class="" style="border-bottom: 1px dotted #D6D6D6;"></div>\
          <div name="content" class="pt5 fntsmall"></div>\
      </div>\
  </div>\
'
dojo.declare( 'zeta.ToolTips',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  n_tooltip: null,    // Tool tip node.

  tooltips: [],       // Array of tooltips

  templateString: tt_template,

  postCreate: function() {
      
      var tt      = this.tooltips;
      var nt      = null;
      var nc      = null;

      this.n_tabs  = this.domNode.childNodes[1].childNodes[1]
      this.n_cont  = this.domNode.childNodes[1].childNodes[3]

      if( tt ) {
          for( i=0 ; i < tt.length; i++ ) {
              nt = dojo.create( "span", { class: "ml10 pl5 pr5 fntsmall fgblack fntbold fgblue pointer",
                                          innerHTML: tt[i][0]
                                        },
                                this.n_tabs, "last" )
              nc = dojo.create( "div", { class: "dispnone ml20", innerHTML: tt[i][1] },
                                this.n_cont, "last" )
              dojo.connect( nt, 'onclick', dojo.hitch( this, 'ontab', nt, nc ));
          }
          if( this.n_tooltip ) {
              // toggler( this.n_tooltip, this.domNode, 'Close', 'Tool-Tips', true )
              dojo.connect(
                this.n_tooltip,
                'onclick',
                this,
                function(e) {
                    dojo.toggleClass( this.domNode, 'dispnone' );
                }
              );
          }
          var deftab = this.n_tabs.childNodes[0];
          dojo.toggleClass( deftab, 'fgblue', false );
          dojo.toggleClass( this.n_cont.childNodes[0], 'dispnone', false );
          dojo.style( deftab, { borderBottom: "1px solid #FFFFB8",
                                borderLeft: "1px dotted #d6d6d6",
                                borderRight: "1px dotted #d6d6d6" 
                              }
                    );
      }
  },

  ontab: function( nt, nc, e ) {
      dojo.forEach( this.n_tabs.childNodes,
          function(n) {
              dojo.toggleClass( n, 'fgblue', 'true' );
              dojo.style( n, { borderBottom: "none", borderLeft: "none", borderRight: "none" } );
          }
      );
      dojo.forEach( this.n_cont.childNodes,
          function(n) {
              dojo.toggleClass( n, 'dispnone', 'true' );
          }
      );
      dojo.toggleClass( nt, 'fgblue', false );
      dojo.toggleClass( nc, 'dispnone', false );
      dojo.style( nt, { borderBottom: "1px solid #FFFFB8", 
                        borderLeft: "1px dotted #d6d6d6",
                        borderRight: "1px dotted #d6d6d6" 
                      }
                );
      dojo.stopEvent( e );
  }

}
);

/*************************************************************************************
*********************************** Shrink Node
**************************************************************************************/

dojo.declare( 'zeta.ShrinkNode',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  node: null,         // Node to shrink / expand

  n_trigg: null,      // Node to interface shrinking and expanding

  hexp: '100%',       // Expand-to-height.

  hshrink: '100%',    // Shrink-to-height.

  wexp: '100%',       // Expand-to-Width.

  wshrink: '100%',    // Shrink-to-Width.

  def: 'expand',      // By default do-what ?

  templateString: '<div><div dojoAttachPoint="containerNode"></div>' + 
                  '<span class="fgblue hoverhighlight pointer"></span></div>',

  postCreate: function() {
      this.node    = this.domNode.childNodes[0];
      this.n_trigg = this.domNode.childNodes[1];
      var n        = this.node
      dojo.toggleClass( n, 'overh', true );
      this.dovisibility( n, this.def );
      this.n_trigg.innerHTML = this.def == 'shrink' ? '...' : 'hide';
      dojo.connect( this.n_trigg, 'onclick', this, 'on_click' )
  },

  dovisibility: function( n, what ) {
      h = what == 'shrink' ? this.hshrink : this.hexp;
      w = what == 'shrink' ? this.wshrink : this.wexp;
      dojo.style( n, { maxHeight: h, width : w } );
  },

  on_click: function( e ) {
      var n = e.currentTarget;
      if( n.innerHTML == '...' ) {
          this.dovisibility( this.node, 'expand' );
          n.innerHTML = 'hide'
      } else if( n.innerHTML == 'hide' ) {
          this.dovisibility( this.node, 'shrink' );
          n.innerHTML = '...'
      }
  }
}
);

/*************************************************************************************
*********************************** Review Comments
**************************************************************************************/

zrc_template = '\
<div class="rcomments p5 mb5" \
   style="border-top: 2px solid gray; border-left: 1px solid gray; border-right: 1px solid gray">\
  <div>\
  <div class="hdr posr w100" style="height: 1.5em;">\
      <div class="reply fgblue pointer mr5 posa" style="left: 60em;"></div>\
      <div class="approved mr5 posa" style="width: 8em; left: 53em;"></div>\
      <div class="action mr5 posa" style="width : 11em; left: 40em;"></div>\
      <div class="nature mr5 posa" style="width : 11em; left: 28em;"></div>\
      <span class="commentor"></span>\
      <span class="createdon"></span>\
  </div>\
  <div class="comment">\
      <div class="position pl5"></div>\
      <div class="text pl5"></div>\
  </div>\
  </div>\
</div>\
'

zrc_reply_template = '\
<div class="hdr w100" style="height: 1.5em;">\
  <span class="commentor"></span>\
  <span class="createdon"></span>\
</div>\
<div class="text pl5"></div>\
'

dojo.declare( 'zeta.RComment',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  w_cntnr: null,      // container widget

  item: null,         // review comment data store item

  store: null,        // dojo.data store for the item

  colormap: {},       // Author color map

  n_rrcmt: null,      // Array of reply nodes [ n_hdr, n_comment ]

  templateString: zrc_template,

  postCreate: function() {
      var replies = this.store.getValues( this.item, 'replies' );
      dojo.hitch( this, this._make_commentnode )();
      // Compose replies
      this.n_rrcmt = Array()
      dojo.forEach(
          replies,
          function( replyitem ) {
              var n_reply = dojo.hitch( this, this._makereplynode, replyitem )();
              this.n_rrcmt[ this.n_rrcmt.length ] = n_reply;
              dojo.place( n_reply, this.domNode, 'last' );
          },
          this
      );
  },

  _make_commentnode: function() {
      var w_cntnr      = this.w_cntnr;
      var n_hdr        = this.domNode.childNodes[1].childNodes[1];
      var n_comment    = this.domNode.childNodes[1].childNodes[3];
      var hdr_children = n_hdr.childNodes;

      var item                = this.item;
      var review_comment_id   = this.store.getValue( item, 'review_comment_id' );
      var commentbyurl        = this.store.getValue( item, 'commentbyurl' );
      var commentby           = this.store.getValue( item, 'commentby' );
      var datestr             = this.store.getValue( item, 'datestr' );
      var html                = this.store.getValue( item, 'html' );
      var nature              = this.store.getValue( item, 'nature' );
      var action              = this.store.getValue( item, 'action' );
      var position            = this.store.getValue( item, 'position' );
      var approved            = this.store.getValue( item, 'approved' );

      dojo.attr( this.domNode, 'review_comment_id', review_comment_id );
      dojo.create( 'a',{ href  : commentbyurl,
                         class : 'nodec fntbold',
                         style : { color : this.colormap[commentby] },
                         innerHTML: commentby },
                         hdr_children[9], 'last' );
      hdr_children[11].innerHTML = 'on ' + datestr;
      // nature
      if( w_cntnr.revwcmtable ) {        // Nature, participants, moderator and author can change
          hdr_children[7].innerHTML = w_cntnr.ref_nature;
          if( nature ) {                 // Nature
              opt = dojo.query( 'option[value='+nature+']', hdr_children[7] )[0]
              if( opt ) {
                  dojo.attr( opt, 'selected', 'selected' )
              }
          } else {
              opts = dojo.query( 'option', hdr_children[7] );
              if( opts ) {
                  dojo.attr( opts[opts.length-1], 'selected', 'selected' )
              }
          }
      } else {
          hdr_children[7].innerHTML = nature ? nature : '<em>no nature</em>'
          dojo.style( hdr_children[7], { textAlign: 'center', borderBottom: '2px solid gray' });
      }
      // action
      if( w_cntnr.authored ) {        // Action, only the author can change
          hdr_children[5].innerHTML = w_cntnr.ref_action;
          if( action ) {
              opt = dojo.query( 'option[value='+action+']', hdr_children[5] )[0]
              if( opt ) {
                  dojo.attr( opt, 'selected', 'selected' )
              }
          } else {
              opts = dojo.query( 'option', hdr_children[5] );
              if( opts ) {
                  dojo.attr( opts[opts.length-1], 'selected', 'selected' )
              }
          }
      } else {
          hdr_children[5].innerHTML = action ? action : '<em>no action</em>'
          dojo.style( hdr_children[5], { textAlign: 'center', borderBottom: '2px solid gray' });
      }
      // approve
      if( w_cntnr.moderated ) {           // Approve, only the moderator can approve
          checked = approved ? 'checked="checked"' : '';
          hdr_children[3].innerHTML = 'Approve: <input type="checkbox" '+checked+'"></input>'
      } else {
          hdr_children[3].innerHTML = approved ?
                                          '<em class="fntbold fggray">Approved</em>' 
                                          : '<em class="fntbold fgcrimson">Pending</em>'
          dojo.style( hdr_children[3], { textAlign: 'center' });
      }
      // Connect to handlers, to submit nature, action and approve changes.
      dojo.connect( dojo.query( 'select', hdr_children[7] )[0], 'onchange',
                    dojo.hitch( w_cntnr, 'onselect_nature', review_comment_id )
                  );
      if( w_cntnr.authored ) {
          dojo.connect( dojo.query( 'select', hdr_children[5] )[0], 'onchange',
                        dojo.hitch( w_cntnr, 'onselect_action', review_comment_id )
                      );
      }
      if( w_cntnr.moderated ) {
          dojo.connect( dojo.query( 'input[type=checkbox]', hdr_children[3] )[0], 'onclick',
                        dojo.hitch( w_cntnr, 'oncheck_approve', review_comment_id )
                      );
      }

      // position and text
      n_comment.childNodes[1].innerHTML = '<span class="fggray">Position : ' + position + '</span>'
      n_comment.childNodes[3].innerHTML = html

      // Connect to hander, to submit a reply to review comment
      if( w_cntnr.revwcmtable ) {
          hdr_children[1].innerHTML = 'Reply'
          dojo.connect( hdr_children[1], 'onclick',
                        dojo.hitch( this, this.onreply, w_cntnr, review_comment_id ) );
      }
  },

  _makereplynode: function( replyitem ){
      var commentbyurl = this.store.getValue( replyitem, 'commentbyurl' );
      var commentby    = this.store.getValue( replyitem, 'commentby' );
      var datestr      = this.store.getValue( replyitem, 'datestr' );
      var html         = this.store.getValue( replyitem, 'html' );
      var n_reply = dojo.create( 'div', { class: 'replycomment ml10 mt10 pl5',
                                          innerHTML: zrc_reply_template,
                                          style: {borderLeft: '2px solid #D6D6D6'},
                                        }
                               )
      dojo.create( 'a',{ href  : commentbyurl,
                         class : 'nodec fntbold',
                         style : { color : this.colormap[commentby] },
                         innerHTML: commentby },
                         n_reply.childNodes[0].childNodes[1], 'last' );
      n_reply.childNodes[0].childNodes[3].innerHTML = datestr
      n_reply.childNodes[1].innerHTML = html
      return n_reply
  },

  onreply: function( w_cntnr, torcmt_id, e ) {
      if( e.target.innerHTML == 'Reply' ) {
          e.target.innerHTML = 'Cancel';

          // Revert the reply-cancel tigger for the previous comment.
          if( w_cntnr.currnreply ) {
              w_cntnr.currnreply.innerHTML = 'Reply';
          }

          dojo.place( w_cntnr.rpcntnr, this.domNode, 'last' );
          dojo.toggleClass( w_cntnr.rpcntnr, 'dispnone', false );

          /* Set up the form */
          var inp_rply = dojo.query( 'input[name=replytocomment_id]', w_cntnr.rpform )[0];
          if( inp_rply ) {
              inp_rply.value = torcmt_id;
          }
          dojo.query( 'textarea[name=text]', w_cntnr.rpcntnr )[0].focus();
          w_cntnr.currnreply = e.target;
      } else {
          e.target.innerHTML = 'Reply';
          dojo.toggleClass( w_cntnr.rpcntnr, 'dispnone', true );
          this.domNode.removeChild( w_cntnr.rpcntnr );
          w_cntnr.currnreply = null;
      }
      dojo.stopEvent( e );
  }

}
);

zrcc_template = '<div class="revwcomments ml10 mr10"></div>'

dojo.declare( 'zeta.RCommentContainer',
[ dijit._Widget, dijit._Templated, dijit._KeyNavContainer ],
{
  ifrs_rcomments : null,  // Data store for review comments and replies

  rpform:'',              // form-node to reply to a review comment

  prform:'',              // form-node to process a review comment

  rpcntnr: null,          // Container for reply form

  ref_nature: null,       // selection element for review comment natures.

  ref_waction: null,      // selection element for review comment actions.

  moderated: false,       // Whether the user is moderating the review

  authored: false,        // Whether the user is authoring the review

  revwcmtable: false,     // Whether the user can comment on a review

  w_comments: [],         // Array of review comments.

  colormap: {},           // Author color map

  currnreply: null,       // Current comment being replied

  templateString: zrcc_template,

  postCreate: function() {
      if( this.ifrs_rcomments.staticstore ) {
          this.ifrs_rcomments.staticfetch({
              onComplete : dojo.hitch( this.ifrs_rcomments, this.ifrs_oncomplete,
                                       this, this.ifrs_rcomments.staticstore )
          });
      } else {
          this.ifrs_rcomments.fetch({
              onComplete : dojo.hitch( this.ifrs_rcomments, this.ifrs_oncomplete,
                                       this, this.ifrs_rcomments.store )
          });
      }
      dojo.subscribe(
          'refreshrcomments',
          this,
          function( by, val ) {
              this.ifrs_rcomments.store.close();
              this.ifrs_rcomments.fetch({
                  onComplete : dojo.hitch( this.ifrs_rcomments, this.ifrs_oncomplete,
                                           this, this.ifrs_rcomments.store ),
              });
          }
      );
  },

  onselect_nature: function( review_comment_id, e ) {
      var n_select  = e.currentTarget;
      var n_rcmt_id = dojo.query( 'input[name=review_comment_id]', this.prform )[0];
      var n_nature  = dojo.query( 'input[name=reviewnature]', this.prform )[0];

      n_rcmt_id.value = review_comment_id;
      n_nature.value  = n_select.value
      submitform( this.prform, e );
      dojo.stopEvent( e );
  },
      
  onselect_action: function( review_comment_id, e ) {
      var n_select  = e.currentTarget;
      var n_rcmt_id = dojo.query( 'input[name=review_comment_id]', this.prform )[0];
      var n_action  = dojo.query( 'input[name=reviewaction]', this.prform )[0];

      n_rcmt_id.value = review_comment_id;
      n_action.value  = n_select.value
      submitform( this.prform, e );
      dojo.stopEvent( e );
  },

  oncheck_approve: function( review_comment_id, e ) {
      var n_inp     = e.currentTarget;
      var n_rcmt_id = dojo.query( 'input[name=review_comment_id]', this.prform )[0];
      var n_approve = dojo.query( 'input[name=approve]', this.prform )[0];

      n_rcmt_id.value = review_comment_id;
      n_approve.value = n_inp.checked ? 'true' : 'false';
      submitform( this.prform, e );
  },
      
  ifrs_oncomplete : function( w_cntnr, store, items, req ) {
      // This function executes under the ifrs_* object containing the
      // dojo.data store.
      var no_of_cmts = 0;

      dojo.publish( 'flash', [ 'hide' ] );
      this.items = items;         // `this` refers to the ifrs object

      // Calculate author color and no of comments count.
      w_cntnr.domNode.innerHTML = ''
      for( i=0; i < this.items.length; i++ ){
          var commentby     = store.getValue( this.items[i], 'commentby' );
          var count_replies = store.getValues( this.items[i], 'replies' ).length;
          w_cntnr.colormap[commentby] = '';
          no_of_cmts += 1;
          if( count_replies ) {
              no_of_cmts += count_replies;
          }
      }
      w_cntnr.colormap = colormaps(keys( w_cntnr.colormap ));

      dojo.forEach(
          this.items,
          dojo.partial(
              function( w_cntnr, store, item ) {
                  var n_cmt = dojo.create( "div", {}, w_cntnr.domNode, "last" );
                  var w     = new zeta.RComment({
                                      w_cntnr: w_cntnr,
                                      item: item,
                                      store: store,
                                      colormap: w_cntnr.colormap
                                  }, n_cmt );
                  w_cntnr.w_comments[w_cntnr.w_comments.length] = w;
              },
              w_cntnr, store
          )
      );
      // Encode external links with a trailing icon.
      linkencode();
  }
}
);
