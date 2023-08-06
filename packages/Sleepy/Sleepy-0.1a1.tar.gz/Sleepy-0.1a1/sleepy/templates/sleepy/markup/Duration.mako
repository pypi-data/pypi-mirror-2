<%inherit
        file="Atomic.mako" />

<%def
        name="create_xml( col,
                          path,
                          obj,
                          **kwargs )"
        filter="trim">
    ${ obj.days },${ obj.seconds },${ obj.microseconds }
</%def>
