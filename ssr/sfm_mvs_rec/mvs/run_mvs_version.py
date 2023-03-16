import importlib
from ssr.utility.logging_extension import logger


class RunMVSVersion:
    def __init__(self, pm):
        self.pm = pm

    def run(self, mvs_version_py_path, run=True):
        logger.vinfo(
            "Running multi-view-stereo processing using following version",
            mvs_version_py_path,
        )
        adapter_file = importlib.import_module(mvs_version_py_path)
        adapter = getattr(adapter_file, "MVSVersion")(self.pm)
        adapter.run(run)
