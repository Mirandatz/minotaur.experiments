import subprocess
from dataclasses import dataclass
from typing import List

from paths import get_datasets_paths, get_minotaur_output_path
from paths import get_minotaur_path, get_stdout_redirection_path


@dataclass(frozen=True)
class MinotaurSettings:
    dataset_name: str
    classification_type: str
    fold_nr: int
    output_dir_name: str
    fitness_metrics: List[str]
    fittest_selection: str
    max_generations: int
    population_size: int
    mutants_per_generation: int
    cfsbe_target_instance_coverage: int


def _create_minotaur_args(minotaur_settings: MinotaurSettings) -> List[str]:
    dataset_paths = get_datasets_paths(dataset_name=minotaur_settings.dataset_name,
                                       fold_nr=minotaur_settings.fold_nr)
    experiment_output_dir = get_minotaur_output_path(dataset_name=minotaur_settings.dataset_name,
                                                     fold_nr=minotaur_settings.fold_nr,
                                                     output_dir_name=minotaur_settings.output_dir_name)
    single_args = {'train-data': dataset_paths['train_data'],
                   'train-labels': dataset_paths['train_labels'],
                   'test-data': dataset_paths['test_data'],
                   'test-labels': dataset_paths['test_labels'],
                   'output-directory': experiment_output_dir,
                   'classification-type': minotaur_settings.classification_type,
                   'fittest-selection': minotaur_settings.fittest_selection,
                   'max-generations': minotaur_settings.max_generations,
                   'population-size': minotaur_settings.population_size,
                   'mutants-per-generation': minotaur_settings.mutants_per_generation,
                   'cfsbe-target-instance-coverage': minotaur_settings.cfsbe_target_instance_coverage}

    formatted_args = [f'--fitness-metrics={m}' for m in minotaur_settings.fitness_metrics]
    formatted_args.extend([f'--{arg_name}={arg_value}' for arg_name, arg_value in single_args.items()])
    return formatted_args


def run_minotaur(minotaur_settings: MinotaurSettings):
    formatted_args = _create_minotaur_args(minotaur_settings=minotaur_settings)
    minotaur_path = str(get_minotaur_path())
    subprocess_args = [minotaur_path] + formatted_args

    stdout_redirection = get_stdout_redirection_path(dataset_name=minotaur_settings.dataset_name,
                                                     fold_nr=minotaur_settings.fold_nr,
                                                     output_dir_name=minotaur_settings.output_dir_name)

    stdout_redirection.parent.mkdir(parents=True, exist_ok=True)

    with stdout_redirection.open(mode='wt') as stdout_redirection:
        print("Running MINOTAUR... ", end='', flush=True)
        subprocess.run(args=subprocess_args, stdout=stdout_redirection)
        print("Done.")
