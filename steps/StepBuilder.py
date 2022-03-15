from steps.MapMetricStep import MapMetricStep


class StepBuilder:
    @staticmethod
    def build_multi_direct_map_steps(var_list):
        new_steps = []
        for var in var_list:
            new_steps.append(MapMetricStep(var, var))
        return new_steps
