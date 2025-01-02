"""
Public result API interfaces
"""
import logging

import time
import json
import datetime
from dateutil.tz import tzlocal

from fastapi import APIRouter, HTTPException

from ..datahub import DataHub
from ..model import HealthCheck, Market, Asset, OHLCV

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

@router.get("/markets")
async def get_markets() -> dict[str, Market]:
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

@router.get("/markets/{market_id}/assets")
async def get_assets(market_id:str="b13a4902-ad9d-11ef-a239-00155d3ba217",
                     start:int=0, limit:int=1000) -> list[Asset]:
    """Get assets array, The maximus lenth is 1000

    Args:
        market_id (str, optional): Market ID string. Defaults to
        "b13a4902-ad9d-11ef-a239-00155d3ba217".
        start (int, optional): Start index. Defaults to 0.

    Returns:
        dict[str, Asset]: _description_
    """
    markets = DataHub.inst().markets

    if market_id not in markets:
        raise HTTPException(status_code=404, detail="Item not found")

    assets = list(markets[market_id].assets.values())

    if start > len(assets) - 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return [item.to_dict() for item in assets[start:min(start + limit, len(assets))]]

@router.get("/asset/fetch_ohlcv")
async def fetch_ohlcv(assetname:str='btc_usdt', interval="1d",
                      since:int=-1, to:int=-1,limit:int=300) -> list[OHLCV]:
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
    LOG.info("fetch_ohlcv: %s, interval: %s", assetname, interval)
    asset = DataHub.inst().get_asset(assetname)
    if asset is not None:
        ret = asset.fetch_ohlcv(interval, since, to, limit)
        ret.to_json(orient="records")
        retval=json.loads(ret.reset_index().to_json(orient="records"))
    return retval
