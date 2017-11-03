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
        return {}


_TEMPLATE = """
foo
bar
baz
"""








