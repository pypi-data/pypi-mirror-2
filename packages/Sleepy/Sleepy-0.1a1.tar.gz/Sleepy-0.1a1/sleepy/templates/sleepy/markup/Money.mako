<%inherit
        file="Decimal.mako" />
<%def
        name="edit_fields( path )">
    $
    ${ parent.edit_fields( path,
                           class_="money" ) }
</%def>
<%def
        name="new_input( path )">
    $
    ${ parent.new_input( path,
                         class_="money" ) }
</%def>
<%def
        name="_show_content( path,
                             obj,
                             **kwargs )">
    ${ ( shorties.moneyfmt( obj,
                            curr="$" )
        if obj._obj
        else "[None]" ) }
</%def>
