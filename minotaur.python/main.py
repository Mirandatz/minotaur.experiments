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
                                                      population_size=160,
                                                      mutants_per_generation=40,
                                                      cfsbe_target_instance_coverage=cfsbe_value)
        yield minotaur_settings


def run_yeast():
    for minotaur_settings in _generate_dataset_settings(dataset_name='yeast', classification_type='multilabel',
                                                        cfsbe_values=[2, 3, 5, 10, 25, 50, 75, 100, 150, 250]):
        minotaur.run_minotaur(minotaur_settings)


def run_emotions():
    for minotaur_settings in _generate_dataset_settings(dataset_name='emotions', classification_type='multilabel',
                                                        cfsbe_values=[2, 3, 5, 10, 25, 50, 75, 100, 150, 250]):
        minotaur.run_minotaur(minotaur_settings)


def run_iris():
    for minotaur_settings in _generate_dataset_settings(dataset_name='iris', classification_type='singlelabel',
                                                        cfsbe_values=[2, 3, 5, 10, 25, 50, 75]):
        minotaur.run_minotaur(minotaur_settings)


def run_breast_cancer_wisconsin():
    for minotaur_settings in _generate_dataset_settings(dataset_name='breast-cancer-wisconsin',
                                                        classification_type='singlelabel',
                                                        cfsbe_values=[2, 3, 5, 10, 25, 50, 75]):
        minotaur.run_minotaur(minotaur_settings)


def main():
    args = sys.argv
    if len(args) != 2:
        print('Invalid number of command line argumments. Expected 1')
        return

    dataset_name = args[1]

    if dataset_name == 'yeast':
        run_yeast()
    elif dataset_name == 'emotions':
        run_emotions()
    elif dataset_name == 'iris':
        run_iris()
    elif dataset_name == 'breast-cancer-wisconsin':
        run_breast_cancer_wisconsin()
    else:
        print("Unknown dataset")


if __name__ == '__main__':
    main()
