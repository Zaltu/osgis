# Purpose
This repo is meant to be essentially an addition to Python's OS/SYS modules. It will likely grow in features over time.


## fileslice
This is a slightly more feature-rich wrapper around the `glob` module. Primary features are
- Restrict to a list of file types
- Only allow subdirectory globbing, for security reasons.
    - To note, this security can pretty easily be gotten around by changing `aig.topdir` to `/`, but since this is python there's no real way around that.

Use:
```python
>>>>from fileslice import Aiglobber
>>>>aig = Aiglobber(["*.md", "*ignore*"])
>>>>aig.aiglob("./")
[.dockerignore, .gitignore, ReadMe.md]
```

TODO:
- Process exclusions
