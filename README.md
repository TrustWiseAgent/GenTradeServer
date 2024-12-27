[![Document Scan](https://github.com/TrustWiseAgent/GenTradeServer/actions/workflows/doclint.yml/badge.svg)](https://github.com/TrustWiseAgent/GenTradeServer/actions/workflows/doclint.yml)
[![Pylint Scan](https://github.com/TrustWiseAgent/GenTradeServer/actions/workflows/pylint.yml/badge.svg)](https://github.com/TrustWiseAgent/GenTradeServer/actions/workflows/pylint.yml)

# GenTrade Server

## Quick Start

- Run from source

```shell
export PYTHONPATH=<repo_dir>/src
uvicorn gentrade-server.main:app --reload
or
python -m gentrade-server.main
```

- Run from docker

```shell
docker run -p 8000:8000 registry.cn-hangzhou.aliyuncs.com/kenplusplus/gentrade_server
```