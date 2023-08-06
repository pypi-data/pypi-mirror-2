<%inherit
        file="Tipe.mako" />
<%def
        name="create_xml( col,
                          path,
                          obj,
                          created )"
        filter="trim">
    % for prop in path.tipe.props.values():
        <${ prop.name }
            % if created:
                created="${ created }"
                updated="${ created }"
            % endif
           >${ prop.tipe.create_xml( path,
                                     obj[ prop.name ],
                                     created=created ) }</${ prop.name }>
    % endfor
</%def>
<%def
        name="new_fields( col,
                          path )">
    <h5>
        ${ path.tip.name.capitalize() }:
    </h5>
    % for prop in path.tipe.props.values():
        ${ prop.new_fields( path ) }
    % endfor
</%def>
<%def
        name="_show( path,
                     obj,
                     **kwargs )">
    % for prop_name in path.tipe.show_props or obj:
        ${ ( path.tip
                 .child( prop_name )
                 .tipe
                 .show( path.add( name=prop_name ),
                        obj[ prop_name ],
                        **kwargs )) }
    % endfor
</%def>
<%def
        name="text( col,
                    path,
                    obj )">
    % for prop_name in path.tipe.text_props or obj:
        ${ ( path.tip
                 .child( prop_name )
                 .tipe
                 .text( path.add( name=prop_name ),
                        obj[ prop_name ] )) }
    % endfor
</%def>
