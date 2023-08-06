<%inherit
        file="Tipe.mako" />
<%def
        name="new_input( path,
                         class_='',
                         tag=None )">
    ${ ( tag
          or tags.text )( path.tip
                              .name,
                          id=self.form_id( path ),
                          class_=tags.css_classes((( class_,
                                                     True ),
                                                   ( path.tipe
                                                         .name,
                                                     True ),
                                                   ( path.tip
                                                         .name,
                                                     True ),
                                                   ( path.names_str,
                                                     True )))) }
</%def>
<%def
        name="text( col,
                    path,
                    obj )">
    ${ obj }
</%def>
<%def
        name="_show_content( path,
                             obj,
                             **kwargs )">
    ${ ( obj._obj
          if obj._obj
          else "[None]" ) }
</%def>
<%def
        name="create_xml( col,
                          path,
                          obj,
                          **kwargs )"
        filter="trim">
    ${ obj }
</%def>
<%def
        name="edit_fields( path,
                           class_='',
                           tag=None )">
    ${ ( tag
          or tags.text )( path.tip
                              .name,
                          path.tip
                              .read_obj( path )._obj
                           or "",
                          class_=tags.css_classes((( class_,
                                                     True ),
                                                   ( path.tipe
                                                         .name,
                                                     True ),
                                                   ( path.tip
                                                         .name,
                                                     True ),
                                                   ( path.names_str,
                                                     True )))) }
</%def>
