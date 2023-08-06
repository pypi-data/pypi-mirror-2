<%inherit
        file="Atomic.mako" />
<%def
        name="new_input( path )">
    ${ tags.file( path.tip
                      .name,
                  id=self.form_id( path )) }
</%def>
<%def
        name="create_xml( col,
                          path,
                          obj,
                          **kwargs )"
        filter="trim">
    ${ obj[ "filename" ] }
</%def>
<%def
        name="edit_fields( path )">
    ${ tags.file( path.tip
                      .name,
                  id=self.form_id( path )) }
</%def>
