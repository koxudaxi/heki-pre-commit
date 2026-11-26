# heki-pre-commit

A [pre-commit](https://pre-commit.com) hook for [heki](https://github.com/koxudaxi/heki).

It installs heki from its wheels on PyPI, so it needs no Rust toolchain and no build. Each tag
of this repository pins the heki release of the same version.

```yaml
repos:
  - repo: https://github.com/koxudaxi/heki-pre-commit
    rev: v0.6.0
    hooks:
      - id: heki
```

The hook passes the staged Python files to `heki check --touched`. heki follows calls across files, so
it still analyzes the whole project, but it shows and fails on only the reports in those files and the
reports whose call chain reaches one of them, so a project with old findings can use it without a
baseline. Options go before `--touched`, for example `args: [--select, EFF101, --touched]`. To check
the whole project on every commit, set `args: []` and `pass_filenames: false`. heki reads its configuration from
`[tool.heki]` in `pyproject.toml` or from `heki.toml`.

`pre-commit autoupdate` moves `rev` to the newest heki release. This repository is updated
automatically when heki publishes a release to PyPI.

See the [heki documentation](https://heki.koxudaxi.dev/) for the rules and the configuration.
