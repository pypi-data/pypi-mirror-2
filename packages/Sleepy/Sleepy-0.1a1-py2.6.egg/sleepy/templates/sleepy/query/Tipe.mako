<%def
        name="xpath( path )">
    ${ path[ 0 ].res.dbxml.collection.fn_col() }
    /${ path.xpath }
</%def>
<%def
        name="root_uuid( col,
                         path )">
    ${ self.xpath( path ) }
     /@uuid
</%def>
<%def
        name="add_uuid( col,
                        path,
                        uuid )">
    insert nodes
    attribute uuid
              { '${ uuid }' }
    into ${ self.xpath( path ) }
</%def>
<%def
        name="resurrect( col,
                         path )">
    delete nodes
    ${ self.xpath( path ) }
     /@deleted
</%def>
<%def
        name="delete( col,
                      path )">
    insert nodes
    attribute deleted
              { 1 }
    into ${ self.xpath( path ) }
</%def>
<%def
        name="add_node( col,
                        path )">
    insert nodes
    <${ path.tip.name } />
    as last into
    ${ self.xpath( path[ : -1 ] ) }
</%def>
<%def
        name="insert_last( col,
                           nodes,
                           path )">
    insert nodes
    ${ nodes }
    as last into
    ${ self.xpath( path ) }
</%def>
<%def
        name="insert_before( col,
                             nodes,
                             path )">
    insert nodes
    ${ nodes }
    before
    ${ self.xpath( path ) }
</%def>
<%def
        name="read( col,
                    path )">
    ${ self.xpath( path ) }
</%def>
<%def
        name="remove( col,
                      path )">
    delete nodes
    ${ self.xpath( path ) }
</%def>
<%def
        name="update( col,
                      path,
                      obj )">
    let
        $u := ${ self.xpath( path ) }
    return
        replace node
        $u
        with
        <${ path.tip.name }
                updated="${ shorties.rfc3339_now() }">{ $u/@*[ not( local-name() = "updated" ) ]
        }${ path.tipe.create_xml( path,
                                  obj,
                                  add_path=False ) }</${ path.tip.name }>
</%def>
