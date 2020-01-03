import sys
from itertools import product
from typing import Iterable

import minotaur


def _generate_dataset_settings(dataset_name: str, classification_type: str,
                               cfsbe_values: Iterable[int]
                               ) -> Iterable[minotaur.MinotaurSettings]:
    fold_count = 10
    fold_values = list(range(fold_count))
    for fold_nr, cfsbe_value in product(fold_values, cfsbe_values):
        minotaur_settings = minotaur.MinotaurSettings(dataset_name=dataset_name,
                                                      classification_type=classification_type,
                                                      fold_nr=fold_nr,
                                                      output_dir_name=f"{dataset_name}-cfsbe-{cfsbe_value}",
                                                      fitness_metrics=['fscore'],
                                                      fittest_selection='nsga2',
                                                      max_generations=200,
                                                      population_size=80,
                                                      mutants_per_generation=40,
                                                      cfsbe_target_instance_coverage=cfsbe_value)
        yield minotaur_settings


def run_iris():
    for minotaur_settings in _generate_dataset_settings(dataset_name='iris', classification_type='singlelabel',
                                                        cfsbe_values=[2, 8, 16, 32, 64, 128]):
        minotaur.run_minotaur(minotaur_settings)


def run_breast_cancer_wisconsin():
    for minotaur_settings in _generate_dataset_settings(dataset_name='breast-cancer-wisconsin',
                                                        classification_type='singlelabel',
                                                        cfsbe_values=[2, 8, 16, 32, 64, 128, 256]):
        minotaur.run_minotaur(minotaur_settings)


def run_wine():
    for minotaur_settings in _generate_dataset_settings(dataset_name='wine',
                                                        classification_type='singlelabel',
                                                        cfsbe_values=[2, 8, 16, 32, 64]):
        minotaur.run_minotaur(minotaur_settings)


def run_madelon():
    for minotaur_settings in _generate_dataset_settings(dataset_name='madelon',
                                                        classification_type='singlelabel',
                                                        cfsbe_values=[2, 16, 64, 128, 256, 512, 1024, 2048]):
        minotaur.run_minotaur(minotaur_settings)


def run_yeast():
    for minotaur_settings in _generate_dataset_settings(dataset_name='yeast', classification_type='multilabel',
                                                        cfsbe_values=[2, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]):
        minotaur.run_minotaur(minotaur_settings)


def run_emotions():
    for minotaur_settings in _generate_dataset_settings(dataset_name='emotions', classification_type='multilabel',
                                                        cfsbe_values=[2, 8, 16, 32, 64, 128, 256, 512]):
        minotaur.run_minotaur(minotaur_settings)


def run_scene():
    for minotaur_settings in _generate_dataset_settings(dataset_name='scene', classification_type='multilabel',
                                                        cfsbe_values=[2, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]):
        minotaur.run_minotaur(minotaur_settings)


def run_CAL500():
    for minotaur_settings in _generate_dataset_settings(dataset_name='CAL500', classification_type='multilabel',
                                                        cfsbe_values=[2, 8, 16, 32, 64, 128, 256]):
        minotaur.run_minotaur(minotaur_settings)



def main():
    args = sys.argv
    if len(args) != 2:
        print('Invalid number of command line argumments. Expected 1')
        return

    known_datasets = {'iris': run_iris,
                      'breast-cancer-wisconsin': run_breast_cancer_wisconsin,
                      'wine': run_wine,
                      'madelon': run_madelon,
                      'yeast': run_yeast,
                      'emotions': run_emotions,
                      'scene': run_scene,
                      'CAL500': run_CAL500}

    dataset_name = args[1]

    if dataset_name in known_datasets:
        known_datasets[dataset_name]()
    else:
        print("Unknown dataset")


if __name__ == '__main__':
    main()
