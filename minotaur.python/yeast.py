import platform
from pathlib import Path

from minotaur_helper import format_minotaur_args, run_minotaur
from minotaur_helper import get_experiment_output_directory, get_minotaur_stdout_redirection_filename

if 'Windows' in platform.platform():
    DATASETS_BASE_DIR = Path('c:/') / 'source' / 'minotaur.datasets'
    OUTPUT_BASE_DIR = Path('c:/') / 'source' / 'minotaur.output'
elif 'Linux' in platform.platform():
    DATASETS_BASE_DIR = Path.home() / 'minotaur' / 'minotaur.datasets'
    OUTPUT_BASE_DIR = Path.home() / 'minotaur' / 'minotaur.output'
else:
    raise NotImplemented

# Experiment settings
DATASET_NAME = "yeast"
FOLD_COUNT = 10
CLASSIFICATION_TYPE = 'multilabel'
FITNESS_METRICS = ['fscore']
FITTEST_SELECTION = 'nsga2'
MAX_GENERATIONS = 100
POPULATION_SIZE = 100
MUTANTS_PER_GENERATION = 40
CFSBE_TARGET_INSTANCE_COVERAGES = [5, 10, 30, 80, 150]
EXPENSIVE_SANITY_CHECKS = False


def create_single_experiment_args():
    for cfsbe in CFSBE_TARGET_INSTANCE_COVERAGES:
        for fold_nr in range(FOLD_COUNT):
            yield {
                'datasets_dir': DATASETS_BASE_DIR,
                'dataset_name': DATASET_NAME,
                'fold_nr': str(fold_nr),

                'experiment_name': f"experiment-{cfsbe}",

                'output_base_directory': OUTPUT_BASE_DIR,

                'classification_type': CLASSIFICATION_TYPE,
                'fitness_metrics': FITNESS_METRICS,
                'fittest_selection': FITTEST_SELECTION,

                'max_generations': MAX_GENERATIONS,
                'population_size': POPULATION_SIZE,
                'mutants_per_generation': MUTANTS_PER_GENERATION,
                'cfsbe_target_instance_coverage': cfsbe,
            }


def main():
    experiments_arsg_collection = create_single_experiment_args()
    for current_experiment_args in experiments_arsg_collection:
        minotaur_args = format_minotaur_args(current_experiment_args)

        output_dir = get_experiment_output_directory(current_experiment_args)
        output_dir.mkdir(parents=True, exist_ok=True)

        minotaur_stdout_redirection_filename = get_minotaur_stdout_redirection_filename(current_experiment_args)
        with minotaur_stdout_redirection_filename.open(mode='wt') as stdout_redirection:
            run_minotaur(formatted_args=minotaur_args, minotaur_stdout_redirection=stdout_redirection)

    print("Finished running all experiments")


if __name__ == '__main__':
    main()
