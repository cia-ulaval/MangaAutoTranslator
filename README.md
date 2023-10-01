# MangaAutoTranslator
A tool to translate manga/manhua/manhwa from their original language to a selected target language

## Setting environment up

In order to set up environment, I recommend you to use [WSL 2.0 on Windows and install Ubuntu on it](https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-11-with-gui-support#1-overview). Furthermore, I recommend git installation procedure for linux based environment :

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

### pyenv (optional but recommended)

#### Installation

Follow instructions from [official repository](https://github.com/pyenv/pyenv#installation).

**!! WARNING !!**

- If you use WSL 2.0 or Linux, don't forget to install prerequisites :

```bash
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

- Add pyenv to path :

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

#### Project usage

- Look for all available python versions :

```bash
pyenv install --list | grep " 3\."
```

- Install specific version :

```bash
pyenv install <python version>

# For example :
pyenv install 3.10.12
```

- Choose a specific python version :

```bash
# Global python version setting (i.e. by default)
pyenv global <python version>

# Local (for a project)
pyenv local <python version>
```

### poetry

#### Installation

Follow instructions from [official documentation](https://python-poetry.org/docs/#installation).

**!! WARNING !!**

- Add poetry to path :

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

#### Project usage

- Configurations before installing python environment :

```bash
# Use active python version (linux command : which python)
poetry config virtualenvs.prefer-active-python true --local

# Create .venv folder instead of installing it into poetry root environments path
poetry config virtualenvs.in-project true --local
```

- Install project python environment :

```bash
poetry install
```

- Use poetry environment in terminal :

```bash
poetry shell
```

- Run poetry script :

```bash
# Further informations will be given later
poetry run <script name>
```

### poe the poet

Last environment installation step ! Simply run :

```bash
poe torch-cuda
```

This is because *PyTorch* cuda version is not well handled by *poetry*.

## Data

Please download data and store them in `data` folder. Don't worry, `.gitignore` file is ignoring every files in this folder but `.gitkeep` file allows us to keep the folder visible in the repository.

## Notebooks

Please use `notebooks` folder to put all visualization or demo notebooks.

## Usage

- To main project script :

```bash
poetry run translate
```
