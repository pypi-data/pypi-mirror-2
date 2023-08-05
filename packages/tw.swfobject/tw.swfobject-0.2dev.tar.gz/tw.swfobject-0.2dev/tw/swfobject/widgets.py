from tw.api import Widget, Link, JSLink, CSSLink, js_function

__all__ = ["SwfObject"]

class SwfObject(Widget):
    """
    """

    javascript = [
        JSLink(modname=__name__, filename='static/swfobject.js', javascript=[])
    ]

    params = {
        "swf": "The URL of the Flash content to embed (required)",
        "width": "The width of the flash object in the generated html (default: 300)",
        "height": "The height of the flash object in the generated html (default: 300)",
        "version": "The Shockwave Flash version required by the Flash content (default: 9.0.0)",
        "xi_swf": "The express install Flash content if version requirements are not met (default: static/expressInstall.swf)",
        "flashvars": "Dictionary of flash variable to pass to the Flash content",
        "objparams": "Dictionary of parameters to the embeded object",
        "script_access": "JavaScript access control: sameDomain, always, never (default: sameDomain)",
        "alternate": "Alternate text to display if Shockwave is not supported",
    }

    embed_swf = js_function("swfobject.embedSWF")

    def __init__(self, **kwargs):
        """Initialize the widget here. The widget's initial state shall be
        determined solely by the arguments passed to this function; two
        widgets initialized with the same args. should behave in *exactly* the
        same way. You should *not* rely on any external source to determine
        initial state."""
        super(SwfObject, self).__init__(**kwargs)

        if self.id is None:
                raise ValueError, "Swfobject is supposed to have id"
        # Load default parameter values
        if self.version is None:
            self.version = "10"

        if self.script_access is None:
            self.script_access = "sameDomain"

        if self.alternate is None:
            self.alternate = "Shockwave Flash Version ${version} Required",

        if self.xi_swf is None:
            self.xi_swf = Link(modname=__name__, filename='static/expressInstall.swf')

        if self.flashvars is None:
            self.flashvars = {}

        if self.objparams is None:
            self.objparams = {}

        # Update the object params with the appropriate AllowScriptAccess restriction
        self.objparams['AllowScriptAccess'] = self.script_access

        # Join alternate text/template data with the necessary div where the flash will be embedded
        self.template = """<div id="${id}">%s</div>""" % self.alternate

    def update_params(self, d):
        """This method is called every time the widget is displayed. It's task
        is to prepare all variables that are sent to the template. Those
        variables can accessed as attributes of d."""
        super(SwfObject, self).update_params(d)
        self.add_call(self.embed_swf(self.swf, self.id, self.width, self.height, \
                                     self.version, self.xi_swf.link, self.flashvars, self.objparams))

