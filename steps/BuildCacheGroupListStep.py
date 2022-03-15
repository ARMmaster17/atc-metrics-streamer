from dto.CacheGroupDTO import CacheGroupDTO
from etl.PipelineStep import PipelineStep


class BuildCacheGroupListStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['cdn_detail_list'], provides=['cache_group_list'])

    def run_step(self, pipeline_context):
        cache_groups = {}
        for cdn in pipeline_context.get_var('cdn_detail_list'):
            for cache_group in pipeline_context.get_var('cdn_detail_list')[cdn].get_cache_groups():
                cache_groups[cache_group['name']] = CacheGroupDTO(cache_group)
        pipeline_context.add_var('cache_group_list', cache_groups)