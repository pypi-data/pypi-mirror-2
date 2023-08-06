<%inherit
        file="Atomic.mako" />
<%def
        name="new_input( path,
                         class_='',
                         tag=None )">
    ${ parent.new_input( path,
                         class_=path.tipe
                                    .size,
                         tag=tags.textarea
                              if path.tipe
                                     .size in ( "para", )
                              else tags.text ) }
</%def>
<%def
        name="edit_fields( path,
                           class_='',
                           tag=None )">
    ${ parent.edit_fields( path,
                           class_=path.tipe
                                      .size,
                           tag=tags.textarea
                                if path.tipe
                                       .size in ( "para", )
                                else tags.text ) }
</%def>
