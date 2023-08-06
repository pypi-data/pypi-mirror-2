<%inherit
        file="Tipe.mako" />

<%def
        name="new_input( path,
                         class_='' )">
    ${ tags.select( path.tip
                        .name,
                    None,
                    [ ( opt[ "yds" ],
                        opt[ "text" ] )
                       for opt
                       in path.tipe
                              .opts() ],
                    id=None,
                    class_=class_ ) }
    ${ self._new_link( path.tipe
                           .path ) }
</%def>
<%def
        name="edit_fields( path,
                           class_='' )">
    ${ tags.select( path.tip
                        .name,
                    path.tipe
                        .concrete( path )
                        .tip
                        .read_obj( path.tipe
                                       .concrete( path ))
                        .yd,
                    [ ( opt[ "yds" ],
                        opt[ "text" ] )
                       for opt
                       in path.tipe
                              .opts() ],
                    id=None,
                    class_=class_ ) }
    ${ self._new_link( path.tipe
                           .path ) }
</%def>
<%def
        name="_new_link( path )">
    % if path.tip.mutable:
        <a
                class="add"
                href="${ url( s( "new_{{ names_path }}",
                                 names_path=path[ : -1 ]
                                                .names_path )) }">
            Add new ${ ( path.tip
                             .label ) }
        </a>
    % endif
</%def>
<%def
        name="create_xml( col,
                          path,
                          obj,
                          **kwargs )"
        filter="trim">
    % for item in path.tipe.item_names():
        <${ item }
           >${ obj.pop() }</${ item }>
    % endfor
</%def>
<%def
        name="_show_content( path,
                             obj,
                             concrete,
                             **kwargs )">
    ${ concrete.tip.text( concrete ) }
</%def>
