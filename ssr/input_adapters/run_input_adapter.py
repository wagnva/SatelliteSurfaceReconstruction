import importlib
from ssr.utility.logging_extension import logger


class RunInputAdapterPipeline:
    def __init__(self, pm):
        self.pm = pm

    def run(self, dataset_adapter, run_input_adapter=True):
        logger.vinfo(
            "Running dataset preprocessing using the following adapter",
            dataset_adapter,
        )
        adapter_file = importlib.import_module(dataset_adapter)
        adapter = getattr(adapter_file, "InputAdapter")(self.pm)
        adapter.run(run_input_adapter)
