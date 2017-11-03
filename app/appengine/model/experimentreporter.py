from jinja2 import Template

class ExperimentReporter:
    """
    Is able to format a plain text report about the results from an allocation.
    """

    def __init__(self, experiment_design, allocation):
        self.alloc = allocation
        self.design = experiment_design

    def report(self):
        report_data = self._make_template_data()
        template = Template(_TEMPLATE)
        report_text = template.render(report_data)
        return report_text

    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------

    def _make_template_data(self):
        res = {}
        res['assays'] = self.design.all_assay_types_as_single_string()
        res['num_chambers'] = self.design.num_chambers
        res['dontmix'] = self.design.dontmix_as_single_string()
        res['max_targets'] = self.design.sim_targets

        res['chamber_table'] = self.alloc.format_chambers(columns=6)
        res['calling_table'] = self.alloc.format_calling_table_for(
                self.design.assay_types_in_priority_order())

        return res


_TEMPLATE = """

ALLOCATION SETTINGS
--------------------

              Assays: {{assays}}
            Chambers: {{num_chambers}}
      Dont mix pairs: {{dontmix}}
         Max targets: {{max_targets}} (*)

                      (*) The allocation guarantees that false
                      positives cannot happen, provided there are no
                      more than <{{max_targets}}> targets present at the 
                      same time.

CHAMBER POPULATION
------------------

{{chamber_table}}

CALLING
-------

{{calling_table}}
"""








