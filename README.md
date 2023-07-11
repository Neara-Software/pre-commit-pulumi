# pre-commit-pulumi

Hooks to use with pre-commit and pulumi

## Current hooks

- pulumi-config: hook that checks the pulumi stack config and refactors it if it has the wrong format

## How to use

Add the following config to your pre-commit

```
  - repo: https://github.com/Neara-Software/pre-commit-pulumi
    rev: "0.1.0"
    hooks:
      - id: pulumi-config
````
