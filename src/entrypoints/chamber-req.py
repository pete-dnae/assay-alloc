import math

for assays in (20, 40, 80):
    for sim_targets in (3,4,5):
        # In n-choose-k notation
        n = assays
        k = sim_targets
        combis_required = math.factorial(n) / float((math.factorial(k) * math.factorial(n - k)))

        chambers_float = math.log(combis_required, 2)
        chambers_int = math.ceil(chambers_float)

        print('sim_targets: %d, assays %d, combis: %d, chamber required: %d' %
              (sim_targets, assays, combis_required, chambers_int))
