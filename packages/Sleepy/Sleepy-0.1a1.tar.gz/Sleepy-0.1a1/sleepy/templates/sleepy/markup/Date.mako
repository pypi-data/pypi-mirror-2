<%inherit
        file="Atomic.mako" />

<%def
        name="edit_fields( path,
                           class_='' )">
    ${ tags.text( path.tip
                      .name,
                  path.tip
                      .read_obj( path )
                      .strftime( "%m/%d/%Y" ),
                  class_="date" ) }
</%def>
<%def
        name="_show_content( path,
                             obj,
                             **kwargs )">
    ${ obj.strftime( "%m/%d/%y" ) }
</%def>
