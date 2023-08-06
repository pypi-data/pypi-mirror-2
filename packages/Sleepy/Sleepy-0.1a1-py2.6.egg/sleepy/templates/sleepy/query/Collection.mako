<%inherit
        file="Tipe.mako" />

<%def
        name="create( col,
                      path,
                      obj,
                      yd )">
    <%
        stamp = shorties.rfc3339_now()
    %>
    insert nodes
    <${ ( path.tipe
              .item
              .name ) }
            yd="${ yd }"
            created="${ stamp }"
            updated="${ stamp }"
        % if path.tipe.item.uuid or path.tipe.item.tipe.uuid:
            uuid="${ shorties.uuid4() }"
        % endif
       >${ ( path.tipe
                 .item
                 .tipe
                 .create_xml( path,
                              obj,
                              yd=yd,
                              created=stamp )) }</${ ( path.tipe
                                                           .item
                                                           .name ) }>
    as last into
    ${ self.xpath( path ) }
</%def>
<%def
        name="new_yd( col,
                      path )">
    if ( ${ self.yds( col,
                      path ) } )
    then
        fn:max( ${ self.yds( col,
                             path ) }
                 /xs:integer( . ))
        + 1
    else
        1
</%def>
<%def
        name="yds( col,
                   path )">
    ${ self.xpath( path ) }
     /*
     /@yd
</%def>
