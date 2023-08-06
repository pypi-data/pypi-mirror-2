<%inherit
        file="base.mako" />

<a
        id="logout"
        href="${ url( "logout" ) }">
    Logout
</a>
<div
        id="tabs">
    <ul
            class="clearfix">
        % for root in filter( lambda r: r.updatable, c.roots.values()):
            <li>
                <a
                        title="panel"
                        id="tab_${ root.name }"
                        href="${ url( root.name ) }">
                    ${ root.name.capitalize() }
                </a>
            </li>
        % endfor
    </ul>
    <div
            id="panel"
            class="clearfix">
    </div>
</div>
