# Installing pyenv for Python version management

## Required Modules

1. Update and upgrade the system:
  ```
  sudo apt update && sudo apt upgrade -y
  ```

2. Install necessary development packages:
  ```
  sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
  ```

3. Install pyenv:

- Download and run the pyenv installer:
  ```
  curl https://pyenv.run | bash
  ```

- Install a specific Python version:
  ```
  pyenv install 3.11
  ```

- Set the desired Python version in your project directory:
  ```
  pyenv local 3.11
  ```

- Make it the global default for your system:
  ```
  pyenv global 3.11
  ```

4. Add pyenv to Terminal Bash Configuration:

- Edit the `~/.bashrc` file:
  ```
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
  echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
  exec "$SHELL"
  ```

- Open `~/.bashrc` in the nano editor:
  ```
  nano ~/.bashrc
  ```

5. Extra Commands:

- List all installed Python versions and mark the currently active one with an asterisk (*):
  ```
  pyenv versions
  ```

- List all available pyenv versions to download, and use `less` to scroll through the output:
  ```
  pyenv install -l | less
  ```

- Get commands to check Python things:

  - Get the path from which the currently active Python version is taken:
    ```
    pyenv prefix
    ```

  - Display the version of the currently active Python interpreter:
    ```
    python3 --version
    ```

  - Get the current working Python version using pyenv:
    ```
    pyenv exec python -V
    ```

  - Get the version of Python in your virtual environment:
    ```
    .venv/bin/python --version
    ```

  - Get the path to the Python interpreter that will be used in your current project directory:
    ```
    which python
    ```

- Create a new virtual environment named `venv` for the currently active Pyenv version:
    ```
    pyenv exec python -m venv venv
    ```

- Reload your `~/.bashrc` configuration to ensure that the pyenv settings are applied:
    ```
    source ~/.bashrc
    ```

- Upgrade pip for the current Pyenv version:
    ```
    pyenv exec python -m pip install --upgrade pip
    ```
