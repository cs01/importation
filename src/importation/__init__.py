import sys
import os.path
import importlib
from importlib.abc import MetaPathFinder
import subprocess
from pathlib import Path
import os

should_log = os.getenv("IMPORTATION_VERBOSE")


def log(*s):
    if should_log:
        print("importation>", *s)


class Importation(MetaPathFinder):
    def __init__(self):
        self.importing = False
        self.venv_path = Path("./__pypackages__/importation/").resolve()
        self.venv_python = Path(self.venv_path / "bin/python")
        self.venv_site_packages = Path(
            self.venv_path
            / f"lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
        ).resolve()

        self.running_in_venv = os.getenv("VIRTUAL_ENV") is not None

        if self.running_in_venv:
            log("Running in a virtual environment")
            self.python = Path("python")
        else:
            log("Not running in a virtual environment")
            log(f"adding site packages dir: {self.venv_site_packages}")
            sys.path.append(str(self.venv_site_packages))
            self.python = self.venv_python

    def ensure_venv(self):
        log("ensuring venv")
        if not self.running_in_venv:
            if not self.python.exists():
                self.create_venv()

    def create_venv(self):
        log(f"creating venv at {self.venv_path}")
        ret = subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                self.venv_path,
                "--prompt",
                "importation venv",
            ],
            capture_output=True,
        )
        if should_log:
            log(ret.stdout.decode())
            log(ret.stderr.decode())

    def find_spec(self, fullname, path, target=None):
        package_name = fullname.split(".")[0]
        if self.importing is True:
            return None

        if package_name in ["nt", "org", "winreg"]:
            return None

        try:
            log("trying to import", package_name)
            self.importing = True
            importlib.import_module(package_name)
        except ImportError:
            # not available, we need to try to install
            self.importing = False
            if not self.running_in_venv:
                self.ensure_venv()

            log("module", package_name, "not found, trying to install")
            ret = subprocess.run(
                [self.python, "-m", "pip", "install", package_name], capture_output=True
            )
            if should_log:
                log(ret.stdout.decode())
                log(ret.stderr.decode())
            if ret.returncode == 0:
                # it was successfully installed! We should be able to import it now.
                self.importing = True
                try:
                    importlib.invalidate_caches()
                    mod = importlib.import_module(package_name)
                    return mod
                except ImportError:
                    return None
                finally:
                    self.importing = False
            return None
        self.importing = False
        return None


sys.meta_path.append(Importation())
