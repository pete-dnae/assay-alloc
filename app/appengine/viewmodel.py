import math

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
        num_chambers = experiment_reporter.design.num_chambers
        num_rows = int(math.ceil(num_chambers / self._DISPLAY_COLUMNS))
        for row_index in range(num_rows):
            next_row = self._make_alloc_table_row(
                experiment_reporter, row_index)
            self.alloc_table['rows'].append(next_row)



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
        same-named attribute in this view model's input_params dictionary.

        For example, if the request form has an entry {assays: 24}, then set
        self.assays = 24.
        """

        for key in form:
            self.input_params[key] = form[key]

    def _make_alloc_table_row(self, experiment_reporter, row_index):
        cells = []
        start_of_chamber_range = row_index * self._DISPLAY_COLUMNS
        end_of_chamber_range = min(
            start_of_chamber_range + self._DISPLAY_COLUMNS,
            experiment_reporter.design.num_chambers)
        for i in range(start_of_chamber_range, end_of_chamber_range):
            chamber_number = i + 1
            cell = self._make_table_cell(chamber_number, experiment_reporter)
            cells.append(cell)
        return cells

    def _make_table_cell(self, chamber_number, experiment_reporter):
        alloc = experiment_reporter.alloc
        assay_types = alloc.assay_types_present_in(chamber_number)
        assay_types = list(assay_types)
        assay_types.sort()
        assay_types = ''.join(assay_types)
        return {'chamber': '%02d' % chamber_number, 'assay_types': assay_types}

