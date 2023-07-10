from pathlib import Path
import subprocess

from hat.doit import common
from hat.doit.py import (build_wheel,
                         run_flake8)

from .dist import *  # NOQA
from . import dist


__all__ = (['task_clean_all',
            'task_version',
            'task_check',
            'task_wheel',
            'task_upload',
            *dist.__all__])


build_dir = Path('build')
pytest_dir = Path('test_pytest')
schemas_json_dir = Path('schemas_json')
src_py_dir = Path('src_py')
node_modules_dir = Path('node_modules')
license_key_path = Path('license.key.pub')

build_py_dir = build_dir / 'py'
py_version_path = src_py_dir / 'hat/praetorian/__init__.py'


def task_clean_all():
    """Clean all"""
    return {'actions': [(common.rm_rf, [build_dir,
                                        py_version_path])]}


def task_version():
    """Generate version files"""

    def generate_py(path):
        # TODO should we use PIP version
        version = common.get_version()
        path.write_text(f'__version__ = {repr(version)}\n')

    for action, path in [(generate_py, py_version_path)]:
        yield {'name': str(path),
               'actions': [(action, [path])],
               'file_dep': ['VERSION'],
               'targets': [path]}


def task_check():
    """Check"""
    return {'actions': [(run_flake8, [src_py_dir])],
            'task_dep': ['version']}


def task_wheel():
    """Build wheel"""

    def build():
        build_wheel(
            src_dir=src_py_dir,
            dst_dir=build_py_dir,
            name='hat-praetorian',
            description='Hat PRAETORIAN',
            url='https://www.koncar.hr/',
            license=common.License.PROPRIETARY,
            packages=['hat'],
            console_scripts=[
                'hat-praetorian-relay = hat.praetorian.relay.system:main',
                'hat-praetorian-commander = hat.praetorian.commander.system:main',  # NOQA
                ],
            gui_scripts=[])

    return {'actions': [build],
            'task_dep': []}


def task_upload():
    """Upload distribution"""

    def upload():
        subprocess.run(['scp',
                        '-P', '22',
                        '-o', 'StrictHostKeyChecking=no',
                        '-i', 'rtdist.key',
                        str(dist.dist_path),
                        'rtdist@185.252.233.141:/var/www/dist/praetorian'],  # NOQA
                       check=True)

    return {'actions': [upload],
            'task_dep': ['dist']}
