from ssr.config.ssr_config import SSRConfig
from ssr.path_manager import PathManager
from ssr.sfm_mvs_rec.vissat_pipeline import VisSatPipeline


class MVSVersion:
    def __init__(self, pm: PathManager):
        self.pm = pm

    def run(self, run=True):
        if run:
            vissat_pipeline = VisSatPipeline(self.pm)
            vissat_pipeline.create_config_mvs()
            vissat_pipeline.run(run)