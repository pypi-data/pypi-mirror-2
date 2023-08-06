$( document )
 .ready( function() {
    var fb_display_opts = { overlayOpacity:
                             0.7,
                            overlayColor:
                             "#555555",
                            scrolling:
                             "no",
                            enableArrowKeys:
                             false,
                            padding:
                             30 };

    var action_success = function( data,
                                   status,
                                   xhr ) {
      var show_message = function() {
        $.fancybox( $.extend( { content:
                                 $( "<div />" )
                                  .html( data )
                                  .find( ".message" ),
                                closeOnKeypress:
                                 true },
                              fb_display_opts ));
        $( "#tabs" )
         .unbind( "tabsload",
                  show_message );
      };

      $( "#tabs" )
       .bind( "tabsload",
              show_message );
      $( "#tabs" )
       .tabs( "load",
              $( "#tabs" )
               .tabs( "option",
                      "selected" ));
    };

    var action_error = function() {
      $.fancybox( $.extend( { content:
                               $( [ "<div class='message failed'>",
                                        "Update failed.",
                                    "</div>" ]
                                   .join( "" )),
                              closeOnKeypress:
                               true },
                            fb_display_opts ));
    };

    var _sortablize = function( $cols ) {
      $cols
       .sortable( { update:
                     function( event,
                               ui ) {
                       $.ajax( { type:
                                  "POST",
                                 url:
                                  ui.item
                                    .find( "form.reorder" )
                                    .attr( "action" ),
                                 data:
                                  { other:
                                     ui.item
                                       .next()
                                       .length
                                      && ui.item
                                           .next()
                                           .attr( "id" )
                                           .slice( ui.item
                                                     .next()
                                                     .attr( "id" )
                                                     .lastIndexOf( "_" )
                                                    + 1 )
                                      || "last" },
                                 success:
                                  action_success,
                                 error:
                                  action_error } );
                       $.fancybox
                        .showActivity();
                     },
                    axis:
                     "y",
                    handle:
                     ".reorderHandle",
                    opacity:
                     0.8 } );
      $( ".reorder",
         $cols )
       .hide();
    };

    $( "#tabs" )
     .tabs();

    var pickerize = function() {
        $( ".date" )
         .datepicker();
        $( ".time" )
         .timePicker( { show24Hours:
                         false,
                        step:
                         15 } );
    };

    var _focus = function() {
        $( "#fancybox-inner form:first :input:visible:first" )
         .focus();
    };

    var _activate = function() {
        pickerize();
        _focus();
    };

    var sortablize = function() {
      var $branchCols = $( ".col" )
                         .not( function() {
                                 return $( this )
                                         .has( ".col" )
                                         .length;
                               } );
      _sortablize( $branchCols );
      $( "li",
         $branchCols )
       .css( "listStyleType",
             "none" );
      $( ".reorderHandle" )
       .hide();
      $( ".reorderHandle",
         $branchCols )
       .show();
    };

    $( ".itemsShow" )
     .live( "click",
            function() {
              $( this )
               .parent()
               .next( ".col" )
               .children()
               .show();
              $( this )
               .hide()
               .next( ".itemsHide" )
               .show();
            } );

    $( ".itemsHide" )
     .live( "click",
            function() {
              $( this )
               .parent()
               .next( ".col" )
               .children()
               .hide();
              $( this )
               .hide()
               .prev( ".itemsShow" )
               .show();
            } );

    var addItemsToggle = function() {
      $( ".col" )
       .before( [ "<div class='itemsToggle'>",
                      "<span class='itemsShow'>",
                          "[Show]",
                      "</span>",
                      "<span class='itemsHide'>",
                          "[Hide]",
                      "</span>",
                  "</div>" ]
                 .join( "" ));
      $( ".itemsShow" )
       .hide();
    };

    $( "#tabs" )
     .bind( "tabsload",
            function() {
              sortablize();
              addItemsToggle();
            } );

    $( "a.edit, a.add, a.resurrect" )
     .live( "click",
            function() {
              $.get( this.href,
                     function( data ) {
                       var $data = $( data );
                       var do_fb = function() {
                         $.fancybox( $.extend( { content:
                                                  $data,
                                                 onComplete:
                                                  _activate },
                                               fb_display_opts ));
                       };
                       var $img = $( "img.res",
                                     $data );
                       if ( $img.length ) {
                         $img.imagesLoaded( do_fb );
                       } else {
                         do_fb();
                       }
                     } );
              $.fancybox
               .showActivity();
              return false;
            } );

    $( "form" )
     .live( "submit",
            function() {
                $( this )
                 .ajaxSubmit( { success:
                                 action_success,
                                error:
                                 action_error } );
                $.fancybox
                 .showActivity();
                return false;
            } );
 } );
