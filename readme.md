# Clype
Playing around with the new type annotations in Python 3.5 and 3.6,
I noticed they can be used to define command line interfaces from a regular python function.
It's kind of like what [click](http://click.pocoo.org) does, but better.

## Usage
Example:
```python
# test.py
from typing import List, Optional
from pathlib import Path
from clype import SimpleCli, SubcommandCli

@SimpleCli
def mycli(v: Optional[bool], paths: List[Path]):
    print('v:', v)
    print('paths ({}):'.format(type(paths[0])), *paths)

if __name__ == '__main__':
    mycli.run()
```
Result:
```sh
$ python test.py -v dir/file.ext
v: True
paths (<class 'pathlib.PosixPath'>): dir/file.ext
```
