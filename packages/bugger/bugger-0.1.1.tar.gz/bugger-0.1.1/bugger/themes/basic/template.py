from bugger.themes.basic import css, javascript

BASE_TEMPLATE = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>

<title>%(title)s</title>

<!-- CSS -->
%(base_css)s
%(extended_css)s

<!-- JavaScript -->
<script type="text/javascript">
%(base_javascript)s
%(extended_javascript)s
</script>
<body>
    <div id="wrapper">
        <div id="header">
            <h1 id="title">%(title)s</h1>
        </div>
        <div id="content">
%(content)s
        </div>
    </div>
</body>
</head>
"""

def base_template(title='', css='', javascript='', content='',
                  base_javascript=javascript.BASE_JAVASCRIPT, base_css=css.BASE_STYLE):
    """Return a base template with the parameters filled in as specified"""
    return BASE_TEMPLATE % (title=title,
                            base_css=base_css,
                            extended_css=css,
                            base_javascript=javascript,
                            extended_javascript=extended_javascript,
                            content=content)