from watergrid.context import DataContext
from watergrid.steps import Step

from dto.CacheGroupDTO import CacheGroupDTO


class BuildCacheGroupListStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['cdn_detail_list'], provides=['cache_group_list'])

    def run(self, pipeline_context: DataContext):
        cache_groups = {}
        for cdn in pipeline_context.get('cdn_detail_list'):
            for cache_group in pipeline_context.get('cdn_detail_list')[cdn].get_cache_groups():
                cache_groups[cache_group['name']] = CacheGroupDTO(cache_group)
        pipeline_context.set('cache_group_list', cache_groups)