<%inherit
        file="Tipe.mako" />
<%def
        name="create_xml( col,
                          path,
                          obj,
                          **kwargs )"
        filter="trim">
</%def>
<%def
        name="new( col,
                   path )">
    ${ tags.form( url( s( "create_{{ p.names_path }}",
                          p=path ),
                       **path.kwargs_dict()),
                  id=s( "new_{{ p.names_str }}",
                        p=path ),
                  multipart=path.tipe
                                .has_multipart ) }
        ${ ( path.tipe
                 .item
                 .new_fields( path )) }
    ${ tags.submit( "submyt",
                    "Add" ) }
    ${ tags.end_form() }
</%def>
<%def
        name="new_fields( col,
                          path )">
</%def>
<%def
        name="text( col,
                    path,
                    obj )">
    % for item_obj in obj:
        ${ ( path.tipe
                 .item
                 .tipe
                 .text( path.add( chunk=item_obj.yd ),
                        item_obj )) }
    % endfor
</%def>
<%def
        name="_show( path,
                     obj,
                     links=True,
                     **kwargs )">
    % if links and path.tip.mutable:
        <a
                class="add"
                href="${ url( s( "new_{{ p.names_path }}",
                                 p=path ),
                              **path.kwargs_dict()) }">
            <img
                    class="add"
                    src="/images/sleepy/green_plus.png" />
            Add new
            ${ ( path.tipe
                     .item
                     .label ) }
        </a>
        % if len( path.tip.read_obj( path, deleted=True )):
            <a
                    class="resurrect"
                    href="${ url( s( "resurrection_{{ p.names_path }}",
                                     p=path ),
                                  **path.kwargs_dict()) }">
                <img
                        class="resurrect"
                        src="/images/sleepy/purple_cross.gif" />
                Resurrect deleted
                ${ ( path.tipe
                         .item
                         .label ) }
            </a>
        % endif
    % endif
    % if len( obj ):
        <ol
                class="col">
            % for item_obj in obj:
                <li
                        class="item"
                        id="${ path.add( chunk=item_obj.yd ).chunk_str }">
                    ${ ( path.tipe
                             .item
                             .tipe
                             .show( path.add( chunk=item_obj.yd ),
                                    item_obj,
                                    links=links )) }
                    % if path.tip.mutable and path.tipe.item.reorderable and links:
                        ${ self._reorder_form( path.add( chunk=item_obj.yd ),
                                               item_obj,
                                               obj ) }
                    % endif
                </li>
            % endfor
        </ol>
    % else:
        <div>
            [ No items ]
        </div>
    % endif
</%def>
<%def
        name="_reorder_form( path,
                             item_obj,
                             obj )">
    <span
            title="Drag up/down &amp; drop to change position"
            class="reorderHandle">
        &#8597;
    </span>
    <span
            class="reorder">
        Move up/down to position:
    </span>
    ${ tags.form( url( s( "reorder_{{ p.names_path }}",
                          p=path ),
                       **path.kwargs_dict()),
                  class_="reorder",
                  id=s( "reorder_{{ p.chunk_str }}",
                        p=path )) }
        ${ tags.select( "other",
                        None,
                        [ ( _item_obj.yd,
                            s( "Before #{{ pos }}",
                               pos=num + 1 ))
                          for ( num, _item_obj )
                          in enumerate( obj )
                          if not ( _item_obj.yd == item_obj.yd
                                    or ( num > 0
                                          and obj[ num - 1 ].yd == item_obj.yd )) ]
                         + ( [ ( "last",
                                 "Last" ) ] if obj[ -1 ].yd != item_obj.yd
                                            else [] ),
                        id=None ) }
    ${ tags.submit( "submit",
                    "Move" ) }
    ${ tags.end_form() }
</%def>
<%def
        name="created( col,
                       path )">
    <div
            class="message">
        Item created.
    </div>
    ${ self._continue( path ) }
</%def>
<%def
        name="reordered( col,
                         path )">
    <div
            class="message">
        Item moved.
    </div>
    ${ self._continue( path ) }
</%def>
