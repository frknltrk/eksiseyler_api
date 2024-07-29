# eksiseyler api

## Usage

### Random Article

```bash
$ curl -X GET https://eksiseyler-api.fly.dev/articles/random
```

### All Articles

```bash
$ curl -X GET https://eksiseyler-api.fly.dev/articles
```

## Build & Run

```bash
$ git clone https://github.com/frknltrk/eksiseyler_api.git && cd eksiseyler_api/
```

### Using Docker

```bash
$ docker build
$ docker run
```

### Locally

```bash
$ pipx install poetry
$ poetry install
$ poetry run fastpi run eksiseyler_api/main.py
```

## Deploy

### Documentation

- https://fly.io/docs/python/frameworks/fastapi/
- https://fly.io/docs/laravel/advanced-guides/github-actions/#github-ci-action-auto-deploy-to-fly-io

### Platforms

- fly.io (used & recommended)
- render.com
- railway.app
- Heroku

## Development

### Useful Resources

- https://docs.docker.com/samples/
- https://docs.pydantic.dev/latest/api/config/#pydantic.config
- https://stackoverflow.com/questions/2279706/select-random-row-from-a-sqlite-table

### Troubleshooting

- [s4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?](https://stackoverflow.com/questions/24398302/bs4-featurenotfound-couldnt-find-a-tree-builder-with-the-features-you-requeste)
- [TypeError: unsupported operand type(s) for |: 'type' and 'NoneType' [duplicate]](https://stackoverflow.com/questions/76712720/typeerror-unsupported-operand-types-for-type-and-nonetype)
- [Permission denied to github-actions[bot]](https://stackoverflow.com/a/75308228/14997609)
