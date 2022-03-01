#!/usr/bin/env python

" Get a science configuration for spatial benchmarking from Github"

__author__ = "Claire Carouge"
__version__ = "1.0 (02.12.2021)"
__email__ = "c.carouge@unsw.edu.au"

from git import Repo
from pathlib import Path
from scripts.cable_utils import remove_directories
import os
import yaml
import subprocess


class SpatialConfig(object):
    def __init__(self, config_info: tuple, exe_path: Path):
        """
        config_info: 2 elements tuple:
            - name of the Github repository with the payu config
            - number of yearly runs to do with payu
        exe_name: name of the CABLE branch to identify the CABLE exe.
        """

        self.config_loc = config_info[0]
        self.config_name = config_info[0].split("/")[1]

        # Payu number of runs
        self.payu_runs = config_info[1]

        # Name of the CABLE branch and path to the executable
        self.exe_path = exe_path
        self.case_name = exe_path.parts[-3]

        # Add name of the CABLE branch to the config name and create corresponding path
        self.config_name = "_".join([self.config_name, self.case_name])
        self.config_path = Path(Path.cwd(), "runs", "spatial", "configs", self.config_name)

    @staticmethod
    def clone_repo(local_path, reponame):
        """Clone a Github repository to the specified local path"""
        # Remove directory if it already exists
        remove_directories(local_path)

        try:
            repo_path = f"git@github.com:{reponame}"
            conf_rep = Repo.clone_from(repo_path, to_path=local_path)
            print(conf_rep)
        except:
            repo_path = f"https::/github.com/{reponame}"
            conf_rep = Repo.clone_from(repo_path, to_path=local_path)

    def clone_config(self):
        """Clone the config repository from Github into the run directory"""

        self.clone_repo(self.config_path, self.config_loc)

    def prepare_config(self):
        """Update config with:
        - proper path to exe file
        - proper path to inputs
        """

        # Read in the config.yaml and modify the inputs and exe
        yaml_path = self.config_path / "config.yaml"
        with open(yaml_path, "r") as fin:
            conf = yaml.safe_load(fin)

        conf["exe"] = str(self.exe_path)
        conf["input"].append(str(self.config_path / "inputs"))

        with open(yaml_path, "w") as fout:
            yaml.dump(conf, fout)

    def run(self):
        """Go to the config directory and run with payu"""

        subprocess.run(
            ["/home/561/ccc561/.local/bin/payu", "sweep"], cwd=self.config_path
        )

        subprocess.run(
            ["/home/561/ccc561/.local/bin/payu", "run", self.payu_runs], cwd=self.config_path
        )
