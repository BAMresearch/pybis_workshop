# BAM `pyBIS` workshop

This is the material for the pyBIS workshop presented at BAM by the BAM Data Store team.

In order to develop the tutorial, clone this repository locally:

```sh
git clone https://github.com/BAMresearch/bam-masterdata.git
cd bam-masterdata
```

Then, create and activate an environment:

```sh
conda create -n pybis_tuto python=3.12
conda activate pybis_tuto
```

With the environment activated, make sure to upgrade pip and install `uv`

```sh
pip install --upgrade pip
pip install uv
```

You can install the dependencies from the uv.lock file:

```sh
uv sync --frozen
```

Launch the MkDocs page by running:

```sh
mkdocs serve
```
