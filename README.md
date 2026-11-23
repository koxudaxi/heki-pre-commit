# heki-pre-commit

A [pre-commit](https://pre-commit.com) hook for [heki](https://github.com/koxudaxi/heki).

It installs heki from its wheels on PyPI, so it needs no Rust toolchain and no build. Each tag
of this repository pins the heki release of the same version.

```yaml
repos:
  - repo: https://github.com/koxudaxi/heki-pre-commit
    rev: v0.2.5
    hooks:
      - id: heki
```

The hook runs `heki check` on the whole project, because heki follows calls across files. Pass
options with `args`, for example `args: [--select, EFF101]`. heki reads its configuration from
`[tool.heki]` in `pyproject.toml` or from `heki.toml`.

`pre-commit autoupdate` moves `rev` to the newest heki release. This repository is updated
automatically when heki publishes a release to PyPI.

See the [heki documentation](https://heki.koxudaxi.dev/) for the rules and the configuration.
