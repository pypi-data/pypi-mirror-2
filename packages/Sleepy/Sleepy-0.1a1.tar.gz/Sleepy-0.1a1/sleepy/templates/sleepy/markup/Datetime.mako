<%inherit
        file="Atomic.mako" />

<%def
        name="new_input( path )">
    ${ tags.text( s( "{{ name }}.date",
                     name=path.tip
                              .name ),
                  shorties.today()
                          .strftime( "%m/%d/%Y" ),
                  class_="date" ) }
    ${ tags.text( s( "{{ name }}.time",
                     name=path.tip
                              .name ),
                  "12:00 PM",
                  class_="time" ) }
</%def>
<%def
        name="edit_fields( path,
                           class_='' )">
    ${ tags.text( s( "{{ name }}.date",
                     name=path.tip
                              .name ),
                  path.tip
                      .read_obj( path )
                      .strftime( "%m/%d/%Y" ),
                  class_="date" ) }
    ${ tags.text( s( "{{ name }}.time",
                     name=path.tip
                              .name ),
                  path.tip
                      .read_obj( path )
                      .strftime( "%I:%M %p" ),
                  class_="time" ) }
</%def>
<%def
        name="_show_content( path,
                             obj,
                             **kwargs )">
    ${ obj.strftime( "%m/%d/%y %I:%M %p" ) }
</%def>
