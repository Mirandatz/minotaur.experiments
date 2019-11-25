import platform
from pathlib import Path
from typing import Dict

_PC_NAME = platform.node()

if _PC_NAME == 'TCHON':
    _base_dir = Path('c:/') / 'source'
    _DATASETS_BASE_DIR = _base_dir / 'minotaur.datasets'
    _OUTPUT_BASE_DIR = _base_dir / 'minotaur.output'
    _MINOTAUR_PATH = _base_dir / 'minotaur' / 'minotaur' / 'minotaur' / 'bin' / 'x64' / 'release' / 'netcoreapp3.0'
    _MINOTAUR_PATH /= 'Minotaur.exe'
elif _PC_NAME == "bioinfo02":
    _base_dir = Path.home() / 'minotaur'
    _DATASETS_BASE_DIR = _base_dir / 'minotaur.datasets'
    _OUTPUT_BASE_DIR = _base_dir / 'minotaur.output'
    _MINOTAUR_PATH = _base_dir / 'minotaur.src' / 'minotaur' / 'Minotaur' / 'Minotaur' / 'bin' / 'x64' / 'Release'
    _MINOTAUR_PATH = _MINOTAUR_PATH / 'netcoreapp3.0' / 'Minotaur'
else:
    raise Exception("Unknown computer / paths.")


def get_minotaur_path() -> Path:
    return Path(_MINOTAUR_PATH)


def get_datasets_paths(dataset_name: str, fold_nr: int) -> Dict[str, Path]:
    dataset_dir = _DATASETS_BASE_DIR / dataset_name / '2-ready-for-minotaur'
    return {'train_data': dataset_dir / f'fold-{fold_nr}' / 'train-data.csv',
            'train_labels': dataset_dir / f'fold-{fold_nr}' / 'train-labels.csv',
            'test_data': dataset_dir / f'fold-{fold_nr}' / 'test-data.csv',
            'test_labels': dataset_dir / f'fold-{fold_nr}' / 'test-labels.csv'}


def get_minotaur_output_path(dataset_name: str, fold_nr: int, output_dir_name: str) -> Path:
    return _OUTPUT_BASE_DIR / output_dir_name / dataset_name / f"fold-{fold_nr}"


def get_stdout_redirection_path(dataset_name: str, fold_nr: int, output_dir_name: str) -> Path:
    return get_minotaur_output_path(dataset_name=dataset_name, fold_nr=fold_nr,
                                    output_dir_name=output_dir_name) / 'stdout_redirection.txt'
