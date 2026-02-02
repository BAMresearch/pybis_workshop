
# One-day BAM Workshop: Automatizing Data Management with PyBIS and the BAM Parser Infrastructure

Welcome to the one-day workshop at BAM to learn Python tools for Research Data Management (RDM) with [openBIS](https://openbis.ch/). This page is organized in the three parts or tutorials presented during the workshop:

* [Part 1 - Basic pyBIS Introduction](part1-basic_introduction.md): you will learn how to do basic calls using pyBIS and about the available [Entities](https://datastore.bam.de/en/concepts/entity_and_entity_types) in an openBIS instance.
* [Part 2 - Advanced pyBIS Features](part2-advanced_features.md): you will learn to create new Entities, their parent-child relationships, and automate searches and filters using pyBIS.
* [Part 3 - BAM Parsers](part3-bam_parsers.md): you will learn how to automate data ingestion by creating new entities and their parent-child relationships using the BAM Parser Infrastructure.

In order to work throughout the tutorials, you will need to install in your laptop:

1. Visual Studio Code (VSCode)
2. Miniforge3 with Python3.12

We also recommend installing a few VSCode extensions which will allow you to open and work with Python and Jupyter Notebooks:

* Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python
* Jupyter: https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter


## Setting up a working VSCode with Python in Windows

Then, open VSCode and open a terminal. In order to run commands with Miniforge3 and Python, you need to make sure the terminal is running with `cmd`. Do:

```
Ctrl+Shift+P → Terminal: Select Default Profile → Command Prompt
```

![VSCode Terminal screenshot](assets/imgs/index_terminal.png)

After that, run in the terminal:

```sh
C:\Miniforge3\Scripts\conda.exe init cmd.exe
```

**Note**: the path `C:\Miniforge3\Scripts` might be different in your case. As of January 2026, this is the path where Miniforge3 is installed in BAM laptops.

After running this command in the terminal, close VSCode completely, and reopen it.

You can verify installation and the proper location of paths if when running:

```sh
conda --version
```

or

```sh
where conda
```

You get back an answer with the version or path where Miniforge3 has the `conda` installer located.

We can close VSCode completely, again, and when launching it again and opening a new terminal, we should see `(base)` at the beginning of your path. You can verify that:

```sh
echo %CONDA_DEFAULT_ENV%
```

returns `base`.

If everything went good, you can also launch the interactive Python terminal:

```sh
python
```

And you will get:

```
Python 3.12.12 | packaged by conda-forge | (main, Jan 26 2026, 23:38:32) [MSC v.1944 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
Ctrl click to launch VS Code Native REPL
>>>
```

## Setup the tutorial workspace

Now, we can create a new folder (done with the command `mkdir`) in the directory we will be working in this tutorial. Then, we also move to it (with `cd`):

```sh
mkdir tutorials
cd tutorials
```

In this folder, you can create a new conda environment (answer `y` during the creation of the environment) with Python 3.12:

```sh
conda create -n pybis_tuto python=3.12
```

And activate it:

```sh
conda activate pybis_tuto
```

Then, we will need to install a few packages:

```sh
pip install pybis jupyter jupyterlab
```

**Note**: in order to speed up the process, you can also pre-install [uv](https://docs.astral.sh/uv/getting-started/installation/) in your laptop and run the command above with `uv` in front, i.e.:

```sh
uv pip install pybis jupyter jupyterlab
```

You can verify that the installation works by running the interactive Python terminal and import a specific pybis object:

```sh
python
```

And in the interactive Python terminal, import:(without the `>>>`):
```sh
>>> from pybis import Openbis
```

If everything went good, after a few seconds, you would be able to instantiate the class `Openbis`.

```python
>>> from pybis import Openbis
>>> Openbis
<class 'pybis.pybis.Openbis'>
```
