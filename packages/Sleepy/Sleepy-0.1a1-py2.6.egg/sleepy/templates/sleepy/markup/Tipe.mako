<%def
        name="form_id( path )"
        buffered="True"
        filter="trim">
    ${ path.names_str }
</%def>
<%def
        name="resurrection( col,
                            path,
                            obj )">
    % if len( obj ):
        <ol
                class="resurrection">
            % for item_obj in obj:
                <li>
                    ${ ( path.tipe
                             .item
                             .tipe
                             .show( path.add( chunk=item_obj.yd ),
                                    item_obj,
                                    links=False )) }
                    ${ self.resurrect_form( path.add( chunk=item_obj.yd )) }
                </li>
            % endfor
        </ol>
    % else:
        <div
                class="resurrection">
            [ No deleted items ]
        </div>
    % endif
</%def>
<%def
        name="resurrect_form( path )">
    ${ tools.button_to( s( "Resurrect {{ name }}",
                           name=path.tip
                                    .name ),
                        url( s( "resurrect_{{ p.names_path }}",
                                p=path ),
                             **path.kwargs_dict()),
                        class_="resurrect",
                        id=s( "resurrect_{{ p.names_str }}",
                              p=path )) }
</%def>
<%def
        name="new_fields( col,
                          path )">
    <fieldset>
        ${ tags.title( path.tip
                           .name
                           .capitalize(),
                       label_for=self.form_id( path )) }
        ${ self.new_input( path ) }
    </fieldset>
</%def>
<%def
        name="show( col,
                    path,
                    obj,
                    links=True,
                    labels=True,
                    **kwargs )">
    <div
            class="clearfix">
        % if path.tip.labels and labels:
            <label>
                ${ path.tip.label.capitalize() }:
            </label>
        % endif
        <div
                 class="${ tags.css_classes((( "showContent",
                                               True ),
                                             ( path.tipe
                                                   .name,
                                               True ),
                                             ( path.tip
                                                   .name,
                                               True ),
                                             ( path.names_str,
                                               True ))) }">
            ${ self._show( path,
                           obj,
                           links=links,
                           labels=labels,
                           **kwargs ) }
        </div>
        % if links and path.tip.deletable and path[ -2 ].res.mutable:
            ${ self._delete_link( path ) }
        % endif
    </div>
</%def>
<%def
        name="_show( path,
                     obj,
                     links=True,
                     **kwargs )">
    ${ self._show_content( path,
                           obj,
                           **kwargs ) }
    % if links and path.tip.mutable:
        <a
                class="edit"
                href="${ url( s( "edit_{{ p.names_path }}",
                                 p=path ),
                              **path.kwargs_dict()) }">
            Edit
        </a>
    % endif
</%def>
<%def
        name="_delete_link( path )">
    ${ tools.button_to( s( "Delete {{ name }}",
                           name=path.tip
                                    .name ),
                        url( s( "delete_{{ p.names_path }}",
                                p=path ),
                             **path.kwargs_dict()),
                        id=s( "delete_{{ p.chunk_str }}",
                              p=path ),
                        class_="delete",
                        method="delete" ) }
</%def>
<%def
        name="updated( col,
                       path )">
    <div
            class="message">
        Item updated.
    </div>
    ${ self._continue( path ) }
</%def>
<%def
        name="resurrected( col,
                           path )">
    <div
            class="message">
        Item resurrected.
    </div>
    ${ self._continue( path ) }
</%def>
<%def
        name="deleted( col,
                       path )">
    <div
            class="message">
        Item deleted.
    </div>
    ${ self._continue( path ) }
</%def>
<%def
        name="_continue( path )">
    <a
            href="${ url( path[ 0 ]
                              .name ) }">
        Continue editing
    </a>
</%def>
<%def
        name="edit( col,
                    path )">
    ${ tags.form( url( s( "update_{{ p.names_path }}",
                          p=path ),
                       **path.kwargs_dict()),
                  id=s( "edit_{{ p.names_str }}",
                        p=path ),
                  method="put",
                  multipart=path.tipe
                                .has_multipart ) }
        ${ self.edit_fields( path ) }
    ${ tags.submit( "submyt",
                    "Update" ) }
    ${ tags.end_form() }
</%def>
