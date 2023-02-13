from pathlib import Path
import os
import shutil

import benchcab.internal as internal


def directory_tree_exists(root_dir=internal.CWD) -> bool:
    paths = [Path(root_dir, internal.SRC_DIR), Path(root_dir, internal.RUN_DIR)]
    return any([path.exists() for path in paths])


def validate_directory_tree(fluxnet: bool, world: bool, root_dir=internal.CWD):
    paths = [Path(root_dir, internal.SRC_DIR), Path(root_dir, internal.RUN_DIR)]

    if fluxnet:
        paths += [
            Path(root_dir, internal.SITE_RUN_DIR),
            Path(root_dir, internal.SITE_LOG_DIR),
            Path(root_dir, internal.SITE_OUTPUT_DIR),
            Path(root_dir, internal.SITE_RESTART_DIR),
            Path(root_dir, internal.SITE_NAMELIST_DIR),
        ]

    if world:
        pass

    if not all([path.exists() for path in paths]):
        raise EnvironmentError("Invalid directory structure in current working directory.")


def clean_directory_tree(root_dir=internal.CWD):
    src_dir = Path(root_dir, internal.SRC_DIR)
    if src_dir.exists():
        shutil.rmtree(src_dir)

    run_dir = Path(root_dir, internal.RUN_DIR)
    if run_dir.exists():
        shutil.rmtree(run_dir)


def setup_directory_tree(fluxnet: bool, world: bool, root_dir=internal.CWD, clean=False):
    if clean:
        clean_directory_tree(root_dir)

    src_dir = Path(root_dir, internal.SRC_DIR)
    os.makedirs(src_dir)

    run_dir = Path(root_dir, internal.RUN_DIR)
    os.makedirs(run_dir)

    if fluxnet:
        site_run_dir = Path(root_dir, internal.SITE_RUN_DIR)
        os.makedirs(site_run_dir)

        site_log_dir = Path(root_dir, internal.SITE_LOG_DIR)
        os.makedirs(site_log_dir)

        site_output_dir = Path(root_dir, internal.SITE_OUTPUT_DIR)
        os.makedirs(site_output_dir)

        site_restart_dir = Path(root_dir, internal.SITE_RESTART_DIR)
        os.makedirs(site_restart_dir)

        site_namelist_dir = Path(root_dir, internal.SITE_NAMELIST_DIR)
        os.makedirs(site_namelist_dir)

    if world:
        pass


class BenchTree(object):
    """Manage the directory tree to run the benchmarking for CABLE"""

    def __init__(self, curdir: Path):

        self.src_dir = curdir/"src"
        self.aux_dir = curdir/"src/CABLE-AUX"
        self.plot_dir = curdir/"plots"
        # Run directory and its sub-directories
        self.runroot_dir = curdir/"runs"
        self.site_run = {
            "site_dir": self.runroot_dir/"site",
            "log_dir": self.runroot_dir/"site/logs",
            "output_dir": self.runroot_dir/"site/outputs",
            "restart_dir": self.runroot_dir/"site/restart_files",
            "namelist_dir": self.runroot_dir/"site/namelists",
        }

        self.clean_previous()

    def clean_previous(self):
        """Clean previous benchmarking runs as needed. 
        Archives previous rev_number.log"""

        revision_file = Path("rev_number.log")
        if revision_file.exists():
            revision_file.replace(self.next_path("rev_number-*.log"))

        return

    @staticmethod
    def next_path(path_pattern, sep="-"):
        """
        Finds the next free path in a sequentially named list of files with the following pattern:
            path_pattern = 'file{sep}*.suf':

        file-1.txt
        file-2.txt
        file-3.txt
        """

        loc_pattern = Path(path_pattern)
        new_file_index = 1
        common_filename, _ = loc_pattern.stem.split(sep)

        pattern_files_sorted = sorted(Path('.').glob(path_pattern))
        if len(pattern_files_sorted):
            common_filename, last_file_index = pattern_files_sorted[-1].stem.split(sep)
            new_file_index = int(last_file_index) + 1

        return f"{common_filename}{sep}{new_file_index}{loc_pattern.suffix}"

    def create_minbenchtree(self):
        """Create the minimum directory tree needed to run the CABLE benchmarking.
        At least, we need:
           - a source directory to checkout and compile the repository branches
           - a run directory to run the testcases."""

        dir_to_create = [
            self.src_dir,
            self.runroot_dir,
        ]
        for mydir in dir_to_create:
            if not Path.is_dir(mydir):
                os.makedirs(mydir)

    def create_sitebenchtree(self):
        """Create directory tree for site benchmark"""

        # Make sure the default directories are created
        self.create_minbenchtree()

        # Create the sub-directories in the run directory
        for mydir in self.site_run.values():
            if not mydir.is_dir():
                os.makedirs(mydir)

        # Copy namelists from the namelists/ directory
        nml_dir = Path.cwd()/"namelists"
        try:
            shutil.copytree(nml_dir, self.site_run["site_dir"], dirs_exist_ok=True)
        except:
            raise
