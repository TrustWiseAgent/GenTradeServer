"""
Public result API interfaces
"""
import logging

import time
import json
import datetime
from dateutil.tz import tzlocal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..datahub import DataHub
from ..model import HealthCheck, settings

LOG = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def get_health() -> HealthCheck:
    """
    Check health
    """
    return HealthCheck(status="OK")


@router.get("/server_time")
async def get_server_time():
    """
    Get server time
    """
    curr_ts = time.time()
    now_utc   = datetime.datetime.fromtimestamp(curr_ts, datetime.UTC)
    tl = tzlocal()

    return {
        'timezone_name': tl.tzname(now_utc),
        'timezone_offset': tl.utcoffset(now_utc).total_seconds(),
        'timestamp_server': int(curr_ts)
    }

@router.get("/markets/")
async def get_markets():
    """
    Get markets
    """
    retval = {}
    for _, market in DataHub.inst().markets.items():
        retval[market.market_id] = {
            "name": market.name,
            "type": market.market_type,
        }
    return retval

@router.get("/markets/")
async def get_markets2():
    """
    Get markets
    """
    retval = {}
    for _, market in DataHub.inst().markets.items():
        retval[market.market_id] = {
            "name": market.name,
            "type": market.market_type,
        }
    return retval

@router.get("/assets/")
async def get_assets(market_id:str=""):
    """
    Get assets
    """
    ret = {}
    markets = []
    if len(market_id) != 0 and market_id not in DataHub.inst().markets:
        LOG.error("could not find the market %s", market_id)
        return ret
    if len(market_id) == 0:
        for id_ in DataHub.inst().markets:
            markets.append(id_)
    else:
        markets.append(market_id)

    for id_ in markets:
        market_inst = DataHub.inst().markets[id_]
        for asset in market_inst.assets.values():
            if market_inst.market_id == "b13a4902-ad9d-11ef-a239-00155d3ba217" and \
                asset.asset_type == "spot":
                ret[asset.name] = asset.to_dict()
            elif market_inst.market_id == "5784f1f5-d8f6-401d-8d24-f685a3812f2d" and \
                asset.asset_type == "stock":
                ret[asset.name] = asset.to_dict()
    return ret

@router.get("/asset/fetch_ohlcv/")
async def fetch_ohlcv(assetname:str='btc_usdt', interval="1d",
                      since:int=-1, to:int=-1,limit:int=300):
    """fetch ohlcv

    Args:
        assetname (str, optional): _description_. Defaults to 'btc_usdt'.
        interval (str, optional): _description_. Defaults to "1d".
        since (int, optional): _description_. Defaults to -1.
        to (int, optional): _description_. Defaults to -1.
        limit (int, optional): _description_. Defaults to 300.

    Returns:
        _type_: _description_
    """
    retval = {}
    LOG.info("fetch_ohlcv: %s", assetname)
    asset = DataHub.inst().get_asset(assetname)
    if asset is not None:
        ret = asset.fetch_ohlcv(interval, since, to, limit)
        ret.to_json(orient="records")
        retval=json.loads(ret.reset_index().to_json(orient="records"))
    return retval
