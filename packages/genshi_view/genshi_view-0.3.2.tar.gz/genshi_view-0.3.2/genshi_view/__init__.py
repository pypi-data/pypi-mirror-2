from paste.script import templates

var = templates.var

class GenshiViewTemplate(templates.Template):
    _template_dir = 'template'
    summary = "a simple view with webob + genshi"
    vars = [
        var('description', 'One-line description of the package'),
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        var('url', 'URL of homepage'),
        var('port', 'port to serve paste')
        ] 
