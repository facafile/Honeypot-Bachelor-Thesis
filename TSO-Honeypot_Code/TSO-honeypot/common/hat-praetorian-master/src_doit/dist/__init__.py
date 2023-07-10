from pathlib import Path
import subprocess
import sys

from hat.doit import common


__all__ = ['task_dist']


def _get_commit():
    p = subprocess.run(['git', 'rev-parse', 'HEAD'],
                       capture_output=True, check=True)
    return p.stdout.decode('utf-8').strip()[:8]


def _get_dist_identifier():
    version = common.get_version()
    if 'dev' not in version:
        return version

    commit = _get_commit()
    return f'{version}_{commit}'


dist_name = f'hat_praetorian-{_get_dist_identifier()}'

build_dir = Path('build')
requirements_path = Path('requirements.pip.runtime.txt')

build_dist_dir = build_dir / 'dist'
build_py_dir = build_dir / 'py'
dist_path = build_dist_dir / f'{dist_name}.tar.gz'

package_path = Path(__file__).parent
relay_conf_path = package_path / 'relay.yaml'
commander_conf_path = package_path / 'commander.yaml'
relay_install_sh_path = package_path / 'install_relay.sh'
commander_install_sh_path = package_path / 'install_commander.sh'
readme_path = package_path / 'README.txt'

praet_logger_path = build_dist_dir / dist_name / 'praet_logger.tar.gz'
command_attack_path = build_dist_dir / dist_name / 'command_attack.tar.gz'


def task_dist():
    """Build distribution"""
    return {'actions': [_build_dist],
            'task_dep': ['wheel']}


def _build_dist():
    dist_dir = build_dist_dir / dist_name
    packages_dir = dist_dir / 'packages'

    common.rm_rf(build_dist_dir)

    subprocess.run([sys.executable, '-m', 'pip', 'wheel', '-q',
                    '-r', str(requirements_path),
                    '-w', packages_dir],
                   check=True)

    for path in (build_py_dir / 'dist').glob('*.whl'):
        common.cp_r(path, packages_dir / path.name)

    common.cp_r(relay_conf_path, dist_dir)
    common.cp_r(commander_conf_path, dist_dir)
    common.cp_r(relay_install_sh_path, dist_dir)
    common.cp_r(commander_install_sh_path, dist_dir)
    common.cp_r(readme_path, dist_dir)

    # praetorian logger script
    subprocess.run(['tar', '-c', '-z',
                    '-f', str(praet_logger_path),
                    '-C', str(package_path),
                    'praet_logger'],
                   check=True)

    # command attack script
    subprocess.run(['tar', '-c', '-z',
                    '-f', str(command_attack_path),
                    '-C', str(package_path),
                    'command_attack'],
                   check=True)

    (dist_dir / 'VERSION.txt').write_text(f'{common.get_version()}\n')

    commit = _get_commit()
    (dist_dir / 'COMMIT.txt').write_text(f'{commit}\n')

    subprocess.run(['tar', '-c', '-z',
                    '-f', str(dist_path),
                    '-C', str(build_dist_dir),
                    dist_name],
                   check=True)
