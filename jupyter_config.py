import os
import click
import subprocess
import logging
from pathlib import Path

_logger = logging.getLogger()
__version__ = "1.0.0"


def set_logging(verbose):
    if verbose:
        logging.basicConfig(format="%(levelname)s : %(message)s", level=logging.DEBUG)
        _logger = logging.getLogger("simple_example")
        _logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(formatter)

        _logger.addHandler(console_handler)
    return


@click.command()
@click.option(
    "--folder",
    type=click.Path(exists=True),
    required=True,
    help="Input the Jupyter Notebook startup folder",
)
@click.option("--version", is_flag=True, help="Show the version")
@click.option("--verbose", is_flag=True, help="Show log messages")
def cli(folder, version, verbose):
    set_logging(verbose)

    if version:
        click.echo(f"Version = {__version__}")

    folder_path = os.path.normpath(folder)

    subprocess.call("jupyter notebook --generate-config -y")
    home_folder = str(Path.home())
    config_file = os.path.join(home_folder, ".jupyter", "jupyter_notebook_config.py")
    _logger.debug(f"Config file: {config_file}")

    if os.path.isfile(config_file):
        with open(config_file, "r") as reader:

            _logger.debug("Updating the settings for the configuration file")
            text = reader.read()

            text = text.replace(
                """# c.NotebookApp.notebook_dir = ''""",
                f"""c.NotebookApp.notebook_dir = r'{folder_path}'""",
            )

        _logger.debug("writing out the configuration")
        with open(config_file, "w") as writer:

            writer.write(text)
        print("Configuration completed")
        print('Run "jupyter notebook" to start notebook server.')
    else:
        print("Cannot find the jupyter_notebook_config.py file.")


if __name__ == "__main__":
    cli()
