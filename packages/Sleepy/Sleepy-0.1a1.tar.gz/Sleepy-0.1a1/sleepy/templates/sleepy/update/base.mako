<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html
        xmlns="http://www.w3.org/1999/xhtml">
<%namespace
        name="u"
        file="/sleepy/util.mako" />
    <head>
        <title>
            Site Update
        </title>
        ${ u.css( "sleepy/reset" ) }
        ${ u.css( "sleepy/util" ) }
        ${ u.css( "sleepy/tabbed" ) }
        ${ u.css( "jquery.ui.lightness" ) }
        ${ u.css( "jquery.fancybox" ) }
        ${ u.css( "timePicker" ) }
        ${ u.script( "jquery" ) }
        ${ u.script( "jquery.form" ) }
        ${ u.script( "jquery.imagesloaded" ) }
        ${ u.script( "jquery-ui" ) }
        ${ u.script( "jquery.fancybox.JR" ) }
        ${ u.script( "jquery.timePicker" ) }
        ${ u.script( "sleepy/tabbed" ) }
    </head>
    <body>
        ${ self.body() }
    </body>
</html>
