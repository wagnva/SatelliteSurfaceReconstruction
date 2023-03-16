from ssr.config.ssr_config import SSRConfig
from ssr.path_manager import PathManager
from ssr.sfm_mvs_rec.vissat_pipeline import VisSatPipeline
import glob
import os
import numpy as np

class MVSVersion:
    def __init__(self, pm: PathManager):
        self.pm = pm

    def run(self, run=True):

        from osgeo import gdal

        # todo move this to the config
        output_dp = os.path.join(self.pm.vissat_mvs_workspace_dp, "dsm", "dsm_tif")
        nerf_depth_maps_dp = "/mnt/Data-2TB-3/Eval_output/nerf/eval/pretrained_jax_004_ds_sc_ba/all/dsm"
        nerf_bbox_fp = "/mnt/Data-2TB-3/NeRF/dataset/DFC2019/Track3-Truth/JAX_004_DSM.txt"

        if not run:
            return

        # read in metada
        dsm_metadata = np.loadtxt(nerf_bbox_fp)
        xoff, yoff = dsm_metadata[0], dsm_metadata[1]
        xsize, ysize = int(dsm_metadata[2]), int(dsm_metadata[2])
        resolution = dsm_metadata[3]

        ulx, uly, lrx, lry = xoff, yoff + ysize * resolution, xoff + xsize * resolution, yoff

        # copy over dms
        # scale them to be the same size using gdal
        for tif_fp in glob.glob(os.path.join(nerf_depth_maps_dp, "*.tif")):
            output_fp = os.path.join(output_dp, os.path.basename(tif_fp))

            ds = gdal.Open(tif_fp)
            ds = gdal.Translate(output_fp, ds, projWin=[ulx, uly, lrx, lry])
            ds = None
            print("Finished copying over:", os.path.basename(output_fp))

        # gdal creates unnecessary .aux.xml files
        # remove them
        for xml_fp in glob.glob(os.path.join(output_dp, "*.xml")):
            os.remove(xml_fp)