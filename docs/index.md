

Install:
1. Visual Studio Code
2. Miniforge3 with Python3.12

Open Visual Studio Code and open a terminal.

Make sure the terminal is in `cmd`:

Ctrl+Shift+P → Terminal: Select Default Profile → Command Prompt

Run:
```
C:\Miniforge3\Scripts\conda.exe init cmd.exe
```

Close VSCode fully and reopen.

Verify installation:
```sh
conda --version
```
or
```sh
where conda
```


In order to activate automatically when opening a new cmd terminal:
```sh
Ctrl+Shift+P → Terminal: Select Default Profile → Command Prompt
```

Close VSCode fully and reopen a terminal. You should see `(base)` at the beginning and in the terminal:
```sh
echo %CONDA_DEFAULT_ENV%
```

should return `base`.

If everything went good, you can also launch the iPython:
```sh
python
```

```
Python 3.10.14 | packaged by conda-forge | (main, Mar 20 2024, 12:40:08) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
Ctrl click to launch VS Code Native REPL
>>> 
```

Create a new folder and enter on it:
```sh
mkdir tutorials
cd tutorials
```

In this folder, create a new conda environment (answer `y` during the creation of the environment):
```sh
conda create -n pybis_tuto python=3.12
```

And activate it:
```sh
conda activate pybis_tuto
```

Install a few packages:
```sh
pip install pybis jupyter jupyterlab
```

You can verify that the installation works by running the interactive Python terminal and import a specific pybis object:
```sh
python
```

Run (without the >>> symbols):
```sh
>>> from pybis import Openbis
```