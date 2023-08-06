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
        ${ tags.form( "/login/submit" ) }
            <fieldset>
                ${ tags.title( "Username",
                               label_for="username" ) }
                ${ tags.text( "username" ) }
            </fieldset>
            <fieldset>
                ${ tags.title( "Password",
                               label_for="password" ) }
                ${ tags.password( "password" ) }
            </fieldset>
            ${ tags.submit( "submit",
                            "Login" ) }
        ${ tags.end_form() }
    </body>
</html>
