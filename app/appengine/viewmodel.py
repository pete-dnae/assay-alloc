import math

class ViewModel:
    """
    Provides the top level model (in the MVC sense) for html view templates to
    consume. Provides methods to create a baseline model from an incoming
    html form request, plus methods to augment this model with data from a
    completed allocation in the form of an ExperimentReporter object.
    """

    _DISPLAY_COLUMNS = 4

    def __init__(self):
        # See _init_to_defaults for attribute default values.
        self._init_to_defaults()


    @classmethod
    def initialise_from_request_form(cls, request):
        """
        A factory function that creates and initialises a ViewModel based only
        on data available from an incoming URL request. I.e. reflects only the
        input conditions.
        """
        mdl = ViewModel()
        mdl._init_to_defaults()
        mdl._override_from_form(request.form)
        return mdl

    def populate_with_experiment_results(self, experiment_reporter):
        # Make available the enumerated assays and dontmix pairs chosen
        self._add_notes_to_augment_input_fields(experiment_reporter)


        # Make available the main allocation table data.
        self.alloc_table = {}
        self.alloc_table["rows"] = []
        num_chambers = experiment_reporter.design.num_chambers
        num_rows = int(math.ceil(num_chambers / float(self._DISPLAY_COLUMNS)))
        for row_index in range(num_rows):
            next_row = self._make_alloc_table_row(
                experiment_reporter, row_index)
            self.alloc_table['rows'].append(next_row)

        # Make available the firing statistics table
        self.firing_stats = {}
        self.firing_stats["firing_assays"] = \
            experiment_reporter.format_assays_in_chambers_that_fired()
        self.firing_stats["rows"] = experiment_reporter.firing_row_stats_rows()

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

        # Augmentation for the input parameters that become available, only
        # once the form has been submitted.
        self.input_params['assays_enumerated'] = ''
        self.input_params['dontmix_enumerated'] = ''
        self.input_params['targets_enumerated'] = ''

        # For rendering the table that reprsents allocations.
        # E.g. the grid size, and the assays presentin a given chamber.
        self.alloc_table = None

        # For rendering the table of firing statistics
        self.firing_stats = None


    def _override_from_form(self, form):
        """
        For all the keys present in the given form dictionary, override the
        same-named attribute in this view model's input_params dictionary.

        For example, if the request form has an entry {assays: 24}, then set
        self.assays = 24.
        """
        for key in form:
            self.input_params[key] = form[key]

    def _add_notes_to_augment_input_fields(self, experiment_reporter):
        """
        Creates strings to go next to the input table fields, for example
        the assays chosen once how many is known ABCDEF...
        """
        self.input_params['assays_enumerated'] = \
            experiment_reporter.design.all_assay_types_as_single_string()
        self.input_params['dontmix_enumerated'] = \
            experiment_reporter.design.dontmix_as_single_string()
        self.input_params['targets_enumerated'] = \
            experiment_reporter.design.targets_as_single_string()

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
        elements = []
        for assay_type in assay_types:
            letter = assay_type
            is_target = (letter in experiment_reporter.design.targets_present)
            element = {'letter': letter, 'is_target': is_target}
            elements.append(element)
        fired = experiment_reporter.did_this_chamber_fire(chamber_number)
        cell = {
            'chamber': '%02d' % chamber_number,
            'assay_types': elements,
            'fired': fired}
        return cell

