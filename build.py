import os
import shutil
import sys

from setuptools_rust import Binding, RustExtension  # the import order is intentional to ensure distutils monkeypatching
from distutils.core import Distribution


def build(setup_kwargs):

    # build Rust extension if POETRY_EXTENSIONS set
    build_extensions = os.getenv("POETRY_EXTENSIONS", False)
    if build_extensions:
        extensions = [RustExtension("poetry._poetry_ext", path="poetry-pubgrub-rs/Cargo.toml", binding=Binding.PyO3)]

        distribution = Distribution({"name": "poetry", "rust_extensions": extensions})
        distribution.run_command("build_rust")
        cmd_build_rust = distribution.get_command_obj("build_rust")


        # copy built extensions into wheel
        cmd_build_ext = distribution.get_command_obj("build_ext")
        for ext in cmd_build_rust.extensions:
            ext_file = cmd_build_ext.get_ext_fullpath(ext.name)
            if not os.path.exists(ext_file):
                continue

            relative_ext_file = os.path.relpath(ext_file, cmd_build_ext.build_lib)
            shutil.copyfile(ext_file, relative_ext_file)
            # win32(cygwin)-dll's need X bits
            if sys.platform in ("win32", "cygwin"):
                mode = os.stat(relative_ext_file).st_mode
                mode |= (mode & 0o444) >> 2  # copy R bits to X
                os.chmod(relative_ext_file, mode)

    return setup_kwargs


if __name__ == "__main__":
    build({})
