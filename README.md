# gyvatukas
collection of python utils i've been rewriting in each project most of the time. i am getting 
older and i am getting tired of rewriting the same stuff over and over again. 
🚨 if definitely full of bugs, do not recommend using if you are not me.

## changelog
v7
- 🚨 Rename modules `_dict` to `dict_` and `_json` to `json_`.
- 🇱🇹 Lithuanian personal code validation logic.
- Use `pathlib` instead of `os.path`.
- New Makefile
- New `generator.get_random_secure_string` function.
- Documentation improvements.
- Lint + format w. `ruff` and `black`.

v6
- Docs using pdoc3
- Makefile improvements

v5
- Rename `read_json_or_return_empty_dict` to `read_json` which now takes default= parameter when 
  value is not found.

v3 
- Email validation logic using https://github.com/JoshData/python-email-validator.

v2 
- Bug fixes, etc. Additional fs/json utils.

v1 
- Initial release with first utils. Not usable.


## publishing a package to pypi
1. make pypi account
2. generate api token
3. run `poetry config pypi-token.pypi <token>`
4. `poetry build` and then `poetry publish`
5. profit 👍