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

        # Input parameters. e.g. number of chambers
        self.input_params = {}
        self.input_params["assays"] = 24
        self.input_params["replicas"] = 3
        self.input_params["dontmix"] = 2
        self.input_params["chambers"] = 24
        self.input_params["targets"] = 2

        # Rendering the table that reprsents alloctions.
        # E.g. the grid size, and the assays presentin a given chamber.
        self.alloc_table = {}
        rows = []
        self.alloc_table['rows'] = rows
        for row in range(6):
            row_cells = []
            rows.append(row_cells)
            for col in range(4): 
                row_cells.append('cell %d %d' % (row, col))


    def _override_from_form(self, key, form):
        """
        For all the keys present in the given form dictionary, override the
        same-named attribute in this view model instance.

        For example, if the request form has an entry {assays: 24}, then set
        self.assays = 24.
        """

        for key in form:
            self.input_params[key] = form[key]
