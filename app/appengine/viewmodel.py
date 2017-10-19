class ViewModel:
    """
    Provides a model (in the MVC sense) for html view templates to consume, 
    including default values, and a factory method to initialise the model 
    from a form belonging to an incoming http request.
    """

    def __init__(self):
        # See _init_to_defaults for attribute default values.
        self._init_to_defaults()


    @classmethod
    def make_from_request(cls, request):
        mdl = ViewModel()
        mdl._init_to_defaults()
        mdl._override_from_form('assays', request.form)
        return mdl


    #-------------------------------------------------------------------------
    # Private below
    #-------------------------------------------------------------------------

    def _init_to_defaults(self):
        self.assays = 24
        self.replicas = 3
        self.dontmix = 2
        self.chambers = 24
        self.targets = 2


    def _override_from_form(self, key, form):
        """
        For all the keys present in the given form dictionary, override the
        same-named attribute in this view model instance.

        For example, if the request form has an entry {assays: 24}, then set
        self.assays = 24.
        """
        for key in form:
            setattr(self, key, form[key])
