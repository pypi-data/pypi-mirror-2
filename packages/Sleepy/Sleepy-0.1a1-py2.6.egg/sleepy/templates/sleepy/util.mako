<%def
        name="css( name=None )">
    <%
        if not name:
            name = c.page.name
    %>
    <link
            rel="stylesheet"
            href="/css/${ name }.css"
            type="text/css" />
</%def>
<%def
        name="script( name=None )">
    <%!
        from pylons import config
    %>
    <%
        debug = config[ "debug" ]
    %>
    % if name == "jquery":
        % if debug:
            <script
                    src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js"
                    type="text/javascript"></script>
        % else:
            <script
                    src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"
                    type="text/javascript"></script>
        % endif
    % elif name == "jquery-ui":
        % if debug:
            <script
                    src="https://ajax.googleapis.com/ajax/libs/jqueryui/1/jquery-ui.js"
                    type="text/javascript"></script>
        % else:
            <script
                    src="https://ajax.googleapis.com/ajax/libs/jqueryui/1/jquery-ui.min.js"
                    type="text/javascript"></script>
        % endif
    % else:
        <script
                src="/js/${ name or c.page.name }.js"
                type="text/javascript"></script>
    % endif
</%def>
<%def
        name="yt_flash( uri,
                        width=480,
                        height=385 )">
        <object
                class="youtube"
                width="${ width }"
                height="${ height }">
            <param
                    name="movie"
                    value="${ h.literal( uri ) }"></param>
            <param
                    name="allowFullScreen"
                    value="true"></param>
            <param
                    name="allowscriptaccess"
                    value="always"></param>
            <param
                    name="wmode"
                    value="transparent"></param>
            <embed
                    src="${ h.literal( uri ) }"
                    type="application/x-shockwave-flash"
                    allowscriptaccess="always"
                    allowfullscreen="true"
                    wmode="transparent"
                    width="${ width }"
                    height="${ height }"></embed>
        </object>
</%def>
<%def
        name="yt_ago( video )">
    <a
            href="${ video.watch_url }"
            class="feedLink">
        <img
                class="youtubeIcon icon"
                src="/images/youtube_icon.png" />
        <span
                class="feedDate">
            Posted ${ video.ago }
        </span>
    </a>
</%def>
<%def
        name="yt_video( video,
                        width=480,
                        height=385,
                        date=True,
                        title=False,
                        thumb=False )">
    ${ yt_ago( video ) }
    % if thumb:
        <a
                class="videoThumb"
                href="${ video.watch_url }">
            <span
                    class="thumb">
                <img
                        alt="${ video.title } (thumbnail)"
                        src="${ video.thumbnail }" />
                <span
                        class="duration">
                    ${ video.duration }
                </span>
            </span>
        </a>
    % else:
        ${ yt_flash( video.flash_url,
                     width,
                     height ) }
    % endif
    % if title:
        <h3
                class="youtube">
            ${ video.title }
        </h3>
    % endif
    % if video.description:
        <p
                class="description">
            ${ shorties.urlize( video.description ) }
        </p>
    % endif
</%def>
<%def
        name="date_str( date )">
    ${ date.month }/${ date.day }\
    % if shorties.now().year != date.year:
/${ str( date.year )[ -2 : ] }
    % endif
</%def>
<%def
        name="time_str( dt )">
    ${ dt.hour % 12 }\
    % if dt.minute:
:${ dt.strftime( "%M" ) }
    % endif
    ${ dt.strftime( "%p" ) }
</%def>
<%def
        name="lorem_ipsum( count=1 )">
    % for num in range( count ):
            Lorem ipsum dolor sit amet, consectetur adipisicing
            elit, sed do eiusmod tempor incididunt ut labore et
            dolore magna aliqua. Ut enim ad minim veniam, quis
            nostrud exercitation ullamco laboris nisi ut aliquip
            ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore
            eu fugiat nulla pariatur. Excepteur sint occaecat
            cupidatat non proident, sunt in culpa qui officia
            deserunt mollit anim id est laborum.
    % endfor
</%def>
<%def
        name="xspf( album )">
    <object
            type="application/x-shockwave-flash"
            class="xspf"
            width="329"
            height="170"
            data="${ xspf_player_uri( album ) }">
        <param
                name="movie"
                value="${ xspf_player_uri( album ) }" />
    </object>
</%def>
<%def
        filter="trim"
        name="xspf_player_uri( album )">
    /swf/xspf_player.swf?playlist_url=${ url( s( "playlist_{{ album.path.names_path }}",
                                                 album=album ),
                                              **dict( format="xspf",
                                                      **album.path
                                                             .kwargs_dict())) | u }
</%def>
<%def
        name="xspf_button( track )">
    <object
            type="application/x-shockwave-flash"
            class="xspfButton"
            width="17"
            height="17"
            data="${ xspf_button_player_uri( track ) }">
        <param
                name="movie"
                value="${ xspf_button_player_uri( track ) }" />
    </object>
</%def>
<%def
        filter="trim"
        name="xspf_button_player_uri( track )">
    /swf/button_player.swf?song_url=${ ( track[ "file" ]
                                              .path
                                              .s3_uri( track[ "file" ] )) | u }
</%def>
<%def
        name="show_entry( entry )">
    <li
            class="unit clearfix">
        % if entry.__class__.__name__ == "Video":
            ${ yt_video( entry,
                         width=360,
                         height=288,
                         title=True ) }
        % elif entry.__class__.__name__ == "Album":
            ALBUM
            ${ album( entry ) }
        % elif hasattr( entry, "_obj" ):
            % if entry.tipe.__class__.__name__ == "Album":
                ${ album( entry ) }
            % else:
                % if entry[ "title" ]._obj:
                    <h3
                            class="entry">
                        ${ entry[ "title" ] }
                    </h3>
                % endif
                <span
                        class="feedDate entryFeedDate">
                    Posted ${ shorties.Ago( entry.published ) }
                </span>
                <p
                        class="message">
                    ${ entry[ "content" ] }
                </p>
            % endif
        % elif entry.__class__.__name__ == "Post":
            <a
                    href="http://www.facebook.com/${ config[ "facebook_user" ] }/posts/${ entry.id.split( "_" )[ -1 ] }"
                    class="feedLink">
                <img
                        class="facebookIcon icon"
                        src="/images/facebook_icon.png" />
                <span
                        class="feedDate">
                    Posted ${ entry.ago }
                </span>
            </a>
            % if entry.message:
                <p
                        class="message">
                    ${ shorties.urlize( entry.message ) }
                </p>
            % endif
            % if entry.tipe == "link":
                % if entry.event:
                    <a
                            href="${ entry.link }"
                            class="facebookEvent facebookLink clearfix">
                        % if entry.picture:
                            <img
                                    src="${ entry.picture }" />
                        % endif
                        <span
                                class="info">
                            <strong>
                                ${ entry.name }
                            </strong>
                            % for property in entry.properties:
                                % if property.get( "text" ):
                                    <em>
                                        ${ property[ "text" ] }
                                    </em>
                                % endif
                            % endfor
                        </span>
                    </a>
                % else:
                    <a
                            href="${ entry.link }"
                            class="facebookLink clearfix">
                        % if entry.picture:
                            <img
                                    src="${ entry.picture }" />
                        % endif
                        <span
                                class="info">
                            <strong>
                                ${ entry.name }
                            </strong>
                            <em>
                                ${ entry.description }
                            </em>
                        </span>
                    </a>
                % endif
            % elif entry.tipe == "photo":
                <a
                        href="${ entry.link }"
                        class="facebookLink clearfix">
                    <img
                            class="photo"
                            src="${ entry.picture }" />
                    <strong>
                        ${ entry.name }
                    </strong>
                </a>
            % elif entry.tipe == "video":
                % if entry.link.find( "youtube.com" ) > -1:
                    <div
                            class="objectWrap">
                        ${ yt_flash( entry.source.split( "&" )[ 0 ],
                                     width=360,
                                     height=288 ) }
                    </div>
                % else:
                    <a
                            href="${ entry.link }"
                            class="facebookLink clearfix">
                        <img
                                class="video"
                                src="${ entry.picture }" />
                        <span
                                class="info videoInfo">
                            <strong>
                                ${ entry.name }
                            </strong>
                            <em>
                                % for property in entry.properties:
                                    % if property.get( "name" ) == u"Length":
                                        Length:
                                        <span
                                                class="property">
                                            ${ property[ "text" ] }
                                        </span>
                                    % endif
                                % endfor
                                ${ entry.description }
                            </em>
                        </span>
                    </a>
                % endif
            % endif
        % endif
    </li>
</%def>
<%def
        name="album( album )">
    <h4
            class="album">
        ${ album[ "name" ] }
    </h4>
    <em
            class="album">
        Posted ${ shorties.Ago( album.published ) }
    </em>
    ${ xspf( album ) }
    % if album[ "comment" ]._obj:
        ${ shorties.markdown( album[ "comment" ] ) }
    % endif
</%def>
