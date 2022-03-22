# projectX-cli

[![Pylint](https://github.com/Basesolve/projectX-cli/actions/workflows/pylint.yml/badge.svg)](https://github.com/Basesolve/projectX-cli/actions/workflows/pylint.yml)
[![Labeler](https://github.com/Basesolve/projectX-cli/actions/workflows/label.yml/badge.svg)](https://github.com/Basesolve/projectX-cli/actions/workflows/label.yml)

## build

```bash
# Install pre-requisites
sudo apt install patchelf ccache -y
pip install -r build-requirements.txt
pip install -r requirements.txt
python -m nuitka -j `nproc` --onefile projectx.py --output-dir build -o projectX
```
