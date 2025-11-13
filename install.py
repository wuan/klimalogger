#!/usr/bin/env python3
import logging
import os.path
import pathlib
import shutil

base_path = "./"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

target_path = "/Volumes/CIRCUITPY"
package_name = "klimalogger"

if __name__ == "__main__":
    main_code = os.path.join(target_path, "code.py")
    if os.path.exists(main_code):
        os.remove(main_code)

    src_path = pathlib.Path(__file__).parent.resolve()
    shutil.rmtree(os.path.join(target_path, "lib", package_name), ignore_errors=True)
    shutil.copytree(
        src_path / package_name, os.path.join(target_path, "lib", package_name)
    )
    shutil.copyfile(src_path / "main_cpy.py", main_code)
