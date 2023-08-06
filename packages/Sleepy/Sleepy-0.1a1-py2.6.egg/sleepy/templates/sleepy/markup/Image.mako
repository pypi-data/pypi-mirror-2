<%inherit
        file="File.mako" />
<%def
        name="_show_content( path,
                             obj,
                             **kwargs )">
    <img
            class="res"
            src="${ path.s3_uri( obj ) }" />
</%def>
