# Clype
Playing around with the new type annotations in Python 3.5 and 3.6,
I noticed they can be used to define command line interfaces from a regular python function.
It's kind of like what [click](http://click.pocoo.org) does, but better.

## Usage
SimpleCli Example:
```python
# test.py
from typing import List, Optional
from pathlib import Path
from clype import SimpleCli

@SimpleCli
def mycli(v: Optional[bool], paths: List[Path]):
    print('v:', v)
    print('paths ({}):'.format(type(paths[0])), *paths)

if __name__ == '__main__':
    mycli.run()
```
Result:
```
$ python test.py -v dir/file.ext
v: True
paths (<class 'pathlib.PosixPath'>): dir/file.ext
```

SubcommandCli Example:
```python
# test.py
from typing import List, Optional
from pathlib import Path
from clype import SubcommandCli

mycli = SubcommandCli('mycli')

@mycli.command
def bar(r: Optional[bool], path: Path):
    """
    The first command
    """
    pass

@mycli.command
def foo(v: Optional[bool], paths: List[Path]):
    """
    The second command
    """
    pass

if __name__ == '__main__':
    mycli.run()
```
Result:
```
$ python test.py -h
usage: mycli [-h] command ...
optional arguments:
  -h, --help  show this help message and exit
commands:
  bar       The first command
  foo       The second command
$ python test.py bar -h
usage: mycli bar [-h] [-r] path
positional arguments:
  path
optional arguments:
  -h, --help  show this help message and exit
  -r
```
