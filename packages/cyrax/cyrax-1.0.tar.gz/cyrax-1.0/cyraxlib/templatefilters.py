import jinja2


def markdown(value):
    try:
        from markdown import Markdown
        md = Markdown(extensions=['footnotes'])
    except ImportError:
        try:
            from markdown2 import Markdown
            md = Markdown(extras=['footnotes', 'code-friendly'])
        except ImportError:
            raise jinja2.TemplateError('Markdown is not installed!')

    return md.convert(value)


def rst(value):
    try:
        import docutils.core
    except ImportError:
        raise jinja2.TemplateError('docutils are not installed!')

    try:
        import cyraxlib.highlight.rst
    except ImportError:
        pass # Pygments not installed

    settings = {'footnote_references': 'superscript'}
    parts = docutils.core.publish_parts(source=value, writer_name='html',
                                        settings_overrides=settings)
    return parts['fragment']


def textile(value):
    try:
        import textile
    except ImportError:
        raise jinja2.TemplateError('textile is not installed!')

    return textile.textile(value)


def rfc3339(date):
    tz = date.strftime('%Z') or 'Z'
    return date.isoformat() + tz


filters = [markdown, rst, textile, rfc3339]
