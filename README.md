# Page Loader

CLI utility that downloads pages and their files(only domain) from the Internet and saves them to your computer.

[![asciicast](https://asciinema.org/a/JO30RT0HQSgiUJTMy4t48C0uk.svg)](https://asciinema.org/a/JO30RT0HQSgiUJTMy4t48C0uk)

## Tests and linter status(CI)

[![.github/workflows/page-loader-check.yml](https://github.com/RamiGaggi/python-project-lvl3/actions/workflows/page-loader-check.yml/badge.svg)](https://github.com/RamiGaggi/python-project-lvl3/actions/workflows/page-loader-check.yml)

## Codeclimate

[![Maintainability](https://api.codeclimate.com/v1/badges/955e18a5aec9fbcdfa2c/maintainability)](https://codeclimate.com/github/RamiGaggi/edu-page-loader/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/955e18a5aec9fbcdfa2c/test_coverage)](https://codeclimate.com/github/RamiGaggi/edu-page-loader/test_coverage)

## Install

1) Clone repository ```git clone https://github.com/RamiGaggi/edu-page-loader.git```
2) Go to working directory ```cd edu-page-loader```
3) Install dependencies ```make install```
4) Install as package```make package-install``` or use ```poetry run```

## Usage

```
page-loader https://www.google.ru
```

```
poetry run page-loader https://www.google.ru
```
