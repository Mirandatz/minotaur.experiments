import platform
import subprocess
from pathlib import Path
from typing import Dict, List

if 'Windows' in platform.platform():
    MINOTAUR_PATH = Path('c:/') / 'source' / 'minotaur' / 'minotaur' / 'minotaur' / 'bin' / 'x64' / 'release'
    MINOTAUR_PATH = MINOTAUR_PATH / 'netcoreapp3.0' / 'Minotaur.exe'
elif 'Linux' in platform.platform():
    MINOTAUR_PATH = Path.home() / 'minotaur' / 'minotaur.src' / 'minotaur' / 'Minotaur' / 'Minotaur' / 'bin' / 'x64'
    MINOTAUR_PATH = MINOTAUR_PATH / 'Release' / 'netcoreapp3.0' / 'Minotaur'
else:
    raise NotImplemented


def get_dataset_paths(minotaur_args) -> Dict[str, Path]:
    datasets_dir = minotaur_args['datasets_dir']
    dataset_name = minotaur_args['dataset_name']
    fold_nr = minotaur_args['fold_nr']
    return {
        'train_data': datasets_dir / dataset_name / '2-ready-for-minotaur' / f'fold-{fold_nr}' / 'train-data.csv',
        'train_labels': datasets_dir / dataset_name / '2-ready-for-minotaur' / f'fold-{fold_nr}' / 'train-labels.csv',
        'test_data': datasets_dir / dataset_name / '2-ready-for-minotaur' / f'fold-{fold_nr}' / 'test-data.csv',
        'test_labels': datasets_dir / dataset_name / '2-ready-for-minotaur' / f'fold-{fold_nr}' / 'test-labels.csv',
    }


def get_experiment_output_directory(experiment_args) -> Path:
    output_dir = experiment_args['output_base_directory']
    output_dir /= experiment_args['experiment_name']
    output_dir /= experiment_args['dataset_name']
    output_dir /= f"fold-{experiment_args['fold_nr']}"
    return output_dir


def get_minotaur_stdout_redirection_filename(experiment_args) -> Path:
    filename = get_experiment_output_directory(experiment_args)
    filename /= 'stdout_redirection.txt'
    return filename


def format_minotaur_args(experiment_args) -> List[str]:
    dataset_paths = get_dataset_paths(experiment_args)
    formatted_args = []
    formatted_args.append(f"--train-data={dataset_paths['train_data']}")
    formatted_args.append(f"--train-labels={dataset_paths['train_labels']}")
    formatted_args.append(f"--test-data={dataset_paths['test_data']}")
    formatted_args.append(f"--test-labels={dataset_paths['test_labels']}")

    formatted_args.append(f"--output-directory={get_experiment_output_directory(experiment_args)}")

    formatted_args.append(f"--classification-type={experiment_args['classification_type']}")

    for m in experiment_args['fitness_metrics']:
        formatted_args.append(f"--fitness-metrics={m}")

    formatted_args.append(f"--fittest-selection={experiment_args['fittest_selection']}")

    formatted_args.append(f"--max-generations={experiment_args['max_generations']}")
    formatted_args.append(f"--population-size={experiment_args['population_size']}")
    formatted_args.append(f"--mutants-per-generation={experiment_args['mutants_per_generation']}")
    formatted_args.append(f"--cfsbe-target-instance-coverage={experiment_args['cfsbe_target_instance_coverage']}")

    formatted_args.append(f"--expensive-sanity-checks=false")

    return formatted_args


def run_minotaur(formatted_args: List[str], minotaur_stdout_redirection):
    subprocess_args = [MINOTAUR_PATH] + formatted_args
    print("Running MINOTAUR... ", end='')
    subprocess.run(args=subprocess_args, stdout=minotaur_stdout_redirection)
    print("Done.")
