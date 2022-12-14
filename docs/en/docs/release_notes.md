# Release Notes

This release is more about bug fixes and improvements,

Ideally the vendored libraries will be upgraded on-demand only when a new security
or important bug fix is released on the respective vendored repository.


### Variable interpolation

The mechanism to evaluate `Lazy` values has been refactored and now `@format` and
`@jinja` values can be used within dictionaries and lists in any nesting levels.


```py

def my_function(name):
    return f"this is computed during validation time for {name} "

```

Historically Project Docs worked in a multi layered environments for
loading data from files, so you were supposed to have a file like:

```toml
[default]
key = 'value'

[production]
key = 'value'
```

## Coming in 0.1.1
- Support for Pydantic BaseSettings for Validators.
- Support for replacement of `toml` parser on envvars loader.