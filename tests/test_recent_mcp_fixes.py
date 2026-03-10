import json

from finshare.sources.eastmoney_source import EastMoneyDataSource
from finshare.sources.fund_source import FundDataSource
from finshare.sources.future_source import FutureDataSource
from finshare.stock.feature.client import FeatureClient


def test_parse_fund_info_from_pingzhongdata():
    source = FundDataSource()
    response_data = (
        'var fS_name = "富国中证1000指数增强(LOF)A";'
        'var fS_code = "161039";'
        'var fund_sourceRate="1.20";'
        'var fund_Rate="0.12";'
        'var fund_minsg="10";'
        'var syl_1n="40.13";'
        'var syl_6y="21.22";'
        'var syl_3y="14.77";'
        'var syl_1y="1.81";'
        'var Data_fluctuationScale = {"categories":["2025-09-30","2025-12-31"],"series":[{"y":7.80,"mom":"-2.11%"},{"y":7.48,"mom":"-4.10%"}]};'
        'var Data_assetAllocation = {"series":[{"name":"股票占净比","data":[84.77,84.92]},{"name":"现金占净比","data":[14.31,14.27]}]};'
        'var Data_currentFundManager =[{"name":"徐幼华","star":4,"workTime":"14年又305天","fundSize":"76.05亿(12只基金)"}];'
    )

    info = source._parse_fund_info(response_data, "161039")

    assert info["code"] == "161039"
    assert info["name"] == "富国中证1000指数增强(LOF)A"
    assert info["manager"] == "徐幼华"
    assert info["source_rate"] == "1.20"
    assert info["current_rate"] == "0.12"
    assert info["return_1y"] == "40.13"
    assert info["scale"] == 7.48
    assert info["asset_allocation"]["股票占净比"] == 84.92


def test_parse_sina_future_snapshot_for_index_continuous():
    source = FutureDataSource()
    content = (
        'var hq_str_nf_IF0="4630.400,4674.000,4630.000,4664.000,57102,265841834.000,114486.000,4664.000,0.000,'
        '5063.400,4143.000,0.000,0.000,4599.200,4603.200,132182.000,4663.000,8,0.000,0,0.000,0,0.000,0,0.000,0,'
        '4664.400,1,0.000,0,0.000,0,0.000,0,0.000,0,2026-03-10,15:00:00,100,1,,,,,,,,,4655.561,沪深300股指期货连续";'
    )

    snapshot = source._parse_sina_future_snapshot(content, "IF0")

    assert snapshot is not None
    assert snapshot.code == "IF0"
    assert snapshot.last_price == 4664.0
    assert snapshot.open_interest == 114486.0
    assert snapshot.day_open == 4630.4
    assert snapshot.day_high == 4674.0
    assert snapshot.day_low == 4630.0


def test_parse_sina_future_snapshot_for_commodity_continuous():
    source = FutureDataSource()
    content = (
        'var hq_str_nf_CU0="铜连续,234826,101430.000,101930.000,101000.000,0.000,101840.000,101850.000,101830.000,'
        '0.000,101150.000,1,7,193715.000,24998,沪,铜,2026-03-10,1,,,,,,,,,101538.436,0.000,0,0.000,0,0.000,0";'
    )

    snapshot = source._parse_sina_future_snapshot(content, "CU0")

    assert snapshot is not None
    assert snapshot.code == "CU0"
    assert snapshot.last_price == 101830.0
    assert snapshot.open_interest == 193715.0
    assert snapshot.bid1_price == 101840.0
    assert snapshot.ask1_price == 101850.0


def test_eastmoney_snapshot_does_not_emit_fake_orderbook():
    source = EastMoneyDataSource()
    data = {
        "f43": 1081,
        "f44": 1081,
        "f45": 1073,
        "f46": 1077,
        "f47": 790112,
        "f48": 850573535.93,
        "f60": 1076,
    }

    snapshot = source._parse_eastmoney_snapshot(data, "000001.SZ")

    assert snapshot is not None
    assert snapshot.last_price == 10.81
    assert snapshot.bid1_price is None
    assert snapshot.ask1_price is None
    assert snapshot.bid1_volume is None
    assert snapshot.ask1_volume is None


def test_money_flow_industry_uses_real_ratio_field():
    client = FeatureClient()

    def fake_request(url, params):
        return {
            "data": {
                "diff": [
                    {
                        "f14": "电子",
                        "f62": 10943965184.0,
                        "f184": 2.87,
                        "f3": 3.55,
                    }
                ]
            }
        }

    client._make_request = fake_request

    df = client.get_money_flow_industry()

    assert not df.empty
    assert json.loads(df.to_json(orient="records"))[0]["net_inflow_ratio"] == 2.87
