<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html
        xmlns="http://www.w3.org/1999/xhtml">
<%namespace
        name="u"
        file="/sleepy/util.mako" />
    <head>
        <title>
            Site Update :: Login
        </title>
        ${ u.css( "sleepy/reset" ) }
        ${ u.css( "sleepy/util" ) }
    </head>
    <body>
        <p>
            You have successfully logged out.
            <a
                    href="${ url( "login" ) }">
                Login
            </a>
        </p>
    </body>
</html>
