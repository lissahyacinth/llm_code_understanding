import pathlib

import click


@click.command()
@click.argument("example_directory", type=str)
def evaluate(example_directory: str):
    formatted_example_directory = pathlib.Path(example_directory)
    if not formatted_example_directory.exists() or not formatted_example_directory.is_dir():
        raise ValueError(f"Could not find a directory at {example_directory}")


if __name__ == "__main__":
    evaluate()
