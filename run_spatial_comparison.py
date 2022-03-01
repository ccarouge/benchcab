#!/usr/bin/env python

"""
Get CABLE, build the executables, setup the run directory, run CABLE ... this is
a wrapper around the actual scripts (see scripts directory)

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (09.03.2019)"
__email__ = "mdekauwe@gmail.com"

import os
import shutil
import sys
import glob
import datetime
import subprocess
import numpy as np
from argparse import ArgumentParser
from pathlib import Path


from user_options import *
from setup.cases_spatial import *
from setup.directory_structure import *
from setup.machine_inits import *
from setup.pbs_spatial import *
from setup.repo_init import *

from scripts.get_cable import GetCable
from scripts.build_cable import BuildCable
from scripts.set_spatial_config import SpatialConfig

from scripts.run_cable_spatial import RunCable


parser = ArgumentParser()
parser.add_argument(
    "--qsub", action="store_true", default=False, help="Run qsub script?"
)
parser.add_argument(
    "-s", "--skipsrc", action="store_true", default=False, help="Rebuild src?"
)

args = parser.parse_args()

if args.qsub == False and args.skipsrc == False:

    #
    ## Get CABLE ...
    #
    G = GetCable(src_dir=src_dir, user=user)
    G.main(repo_name=repos[0], trunk=trunk)  # Default is True
    G.main(repo_name=repos[1], trunk=False)  # integration branch

    #
    ## Build CABLE ...
    #
    B = BuildCable(
        src_dir=src_dir,
        NCDIR=NCDIR,
        NCMOD=NCMOD,
        FC=FCMPI,
        CFLAGS=CFLAGS,
        LD=LD,
        LDFLAGS=LDFLAGS,
        mpi=True,
    )
    B.main(repo_name=repos[0])
    B.main(repo_name=repos[1])


#
## Run CABLE for each science config, for each repo
#

if not os.path.exists(run_dir):
    os.makedirs(run_dir)
# os.chdir(run_dir)

# ------------- Change stuff ------------- #
tmp_ancillary_dir = "global_files"  # GSWP3 grid/mask file, temporarily

met_dir = "/g/data/wd9/MetForcing/Global/GSWP3_2017/"
met_dir = "/scratch/p66/yxw599/runcable-access-esm/gswp/system3/"
start_yr = 1901
end_yr = 1902
walltime = "0:30:00"
qsub_fname = "qsub_wrapper_script_simulation.sh"
# ------------- Change stuff ------------- #

cable_aux = os.path.join("../", aux_dir)
for repo_id, repo in enumerate(repos):
    cable_src = Path(Path.cwd(), src_dir, repo, "offline", "cable-mpi")
    for sci_id, sci_config in enumerate(sci_configs):

        sconf = SpatialConfig(sci_config, cable_src)
        sconf.clone_config()

        sconf.prepare_config()

        sconf.run()

        # R = RunCable(
        #     met_dir=met_dir,
        #     log_dir=log_dir,
        #     output_dir=output_dir,
        #     restart_dir=restart_dir,
        #     aux_dir=aux_dir,
        #     cable_src=cable_src,
        #     qsub_fname=qsub_fname,
        #     walltime=walltime,
        #     tmp_ancillary_dir=tmp_ancillary_dir,
        # )
        # R.initialise_stuff()
        # #        R.setup_nml_file()
        # R.run_qsub_script(start_yr, end_yr)

os.chdir(cwd)
