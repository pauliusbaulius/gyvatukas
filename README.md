# gyvatukas
collection of python utils and prototypes.
it is public, but i would not advise to use it for any serious business. is more of a util 
bundle and playground for new ideas.

anyways, see [docs](https://pauliusbaulius.github.io/gyvatukas/gyvatukas/) page for more info.

pypi: [gyvatukas](https://pypi.org/project/gyvatukas/)

🚨 No changelog

🚩 Frequently changing API

🚨 Lack of tests

🤠 Only fun

## usage
`pip install gyvatukas` or `poetry add gyvatukas`
```python
import gyvatukas as g

tel = '+37060000000'
is_valid, clean_tel = g.validate_lt_tel_nr(tel)
print(is_valid, clean_tel)
```

## dev guide
0. New code time (add new features to `__init__/__all__` if/when they are "prod" worthy to use 
   the pattern of `gyvatukas.<util>` in dependent projects (except for WWW))
1. Format + lint (its 2024, people nitpick a lot)
2. Build docs
3. Increment version in pyproject.toml
4. Build package (commit package + pyproject.toml + docs (clean single build commit, since docs 
   are published from master and are source of truth for the latest pypi release))
5. `poetry publish`
6. Profit 🤑
