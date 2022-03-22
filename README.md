# projectX-cli

## build

```bash
# Install pre-requisites
sudo apt install patchelf ccache -y
pip install -r build-requirements.txt
pip install -r requirements.txt
python -m nuitka -j `nproc` --onefile projectx.py --output-dir build -o projectX
```
