class ViewModel:
    """
    Provides a model (in the MVC sense) for html view templates to consume, 
    including default values, and a factory method to initialise the model 
    from a form belonging to an incoming http request.
    """

    _DISPLAY_COLUMNS = 4

    def __init__(self):
        # See _init_to_defaults for attribute default values.
        self._init_to_defaults()


    @classmethod
    def initialise_from_request_form(cls, request):
        mdl = ViewModel()
        mdl._init_to_defaults()
        mdl._override_from_form('assays', request.form)
        return mdl

    def populate_with_experiment_results(self, experiment_reporter):
        self.alloc_table = {}
        self.alloc_table["rows"] = []
        chambers = experiment_reporter.design.num_chambers

        for i in range(chambers):
            chamber_number = i + 1
            row_index = i / self._DISPLAY_COLUMNS
            col_index = i - (row_index * self._DISPLAY_COLUMNS)
            if row_index == len(self.alloc_table["rows"]):
                self.alloc_table["rows"].append([])
            self.alloc_table["rows"][row_index].append(
                'Chamber number: %d' % chamber_number)


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

        # Fro rendering the table that reprsents allocations.
        # E.g. the grid size, and the assays presentin a given chamber.
        self.alloc_table = None


    def _override_from_form(self, key, form):
        """
        For all the keys present in the given form dictionary, override the
        same-named attribute in this view model instance.

        For example, if the request form has an entry {assays: 24}, then set
        self.assays = 24.
        """

        for key in form:
            self.input_params[key] = form[key]
