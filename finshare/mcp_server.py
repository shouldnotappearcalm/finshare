import asyncio
from typing import Optional, List, Dict, Any, Annotated
from pydantic import Field

from mcp.server.fastmcp import FastMCP

import finshare as fs
from finshare import logger as fs_logger

# --- FastMCP Initialization ---
app = FastMCP(
    name="finshare_data_provider",
    instructions="""finshare MCP Server - 提供专业的A股、期货、基金等金融数据服务。
此服务基于 finshare 库，提供客观的历史K线数据、实时快照、资金流向、财务数据等。
提示:
1. 股票代码支持多种格式，如: '000001.SZ', 'sh600000', '600000'。
2. 日期格式应为 'YYYY-MM-DD' 或 'YYYYMMDD'。
3. 请优先使用具体工具获取期望的数据。
"""
)

# --- Tool Registration ---

@app.tool()
def get_snapshot_data(
    code: Annotated[str, Field(description="证券代码 (如 '000001.SZ', 'sh600000')")]
) -> dict:
    """获取单个证券的实时快照数据。"""
    snapshot = fs.get_snapshot_data(code)
    return snapshot.model_dump(mode='json') if snapshot else {"error": f"Failed to get snapshot for {code}"}

@app.tool()
def get_batch_snapshots(
    codes: Annotated[List[str], Field(description="证券代码列表")]
) -> dict:
    """批量获取多个证券的实时快照数据。"""
    snapshots = fs.get_batch_snapshots(codes)
    return {k: v.model_dump(mode='json') if v else None for k, v in snapshots.items()}

@app.tool()
def get_historical_data(
    code: Annotated[str, Field(description="证券代码 (如 '000001.SZ')")],
    start: Annotated[Optional[str], Field(description="开始日期 'YYYY-MM-DD'")] = None,
    end: Annotated[Optional[str], Field(description="结束日期 'YYYY-MM-DD'")] = None,
    period: Annotated[str, Field(description="周期 'daily', 'weekly', 'monthly'")] = "daily",
    adjust: Annotated[Optional[str], Field(description="复权类型 'qfq', 'hfq', 'None'")] = None
) -> Any:
    """获取历史K线数据。"""
    df = fs.get_historical_data(code, start=start, end=end, period=period, adjust=adjust)
    if df is not None and not df.empty:
        # 转换 datetime 为 string 以便 JSON 序列化
        if 'date' in df.columns and df['date'].dtype.kind == 'M':
             df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        # 处理 NaNs
        df = df.fillna(0)
        return df.to_dict(orient='records')
    return []

@app.tool()
def get_money_flow(
    code: Annotated[str, Field(description="股票代码 (如 '000001.SZ')")]
) -> Any:
    """获取单只股票的资金流向数据。"""
    df = fs.get_money_flow(code)
    if df is not None and not df.empty:
        return df.fillna(0).to_dict(orient='records')
    return []

@app.tool()
def get_money_flow_industry() -> list:
    """获取按行业分类的资金流向数据。"""
    df = fs.get_money_flow_industry()
    if df is not None and not df.empty:
        return df.fillna(0).to_dict(orient='records')
    return []

@app.tool()
def get_financial_indicator(
    code: Annotated[str, Field(description="股票代码 (如 '000001.SZ')")],
    ann_date: Annotated[Optional[str], Field(description="公告日期 'YYYYMMDD' (选填)")] = None
) -> Any:
    """获取股票的主要财务指标数据。"""
    df = fs.get_financial_indicator(code, ann_date=ann_date)
    if df is not None and not df.empty:
        return df.fillna(0).to_dict(orient='records')
    return []

@app.tool()
def get_stock_list(
    market: Annotated[str, Field(description="市场类型 ('all': 全部, 'sh': 上海, 'sz': 深圳)")] = "all"
) -> list:
    """获取A股股票列表。"""
    return fs.get_stock_list(market=market)

@app.tool()
def get_future_snapshot(
    code: Annotated[str, Field(description="期货合约代码 (如 'IF2409', 'IF0')")]
) -> dict:
    """获取期货实时快照数据。"""
    snapshot = fs.get_future_snapshot(code)
    return snapshot.model_dump(mode='json') if snapshot else {"error": f"Failed to get future snapshot for {code}"}

@app.tool()
def get_fund_info(
    code: Annotated[str, Field(description="基金代码 (如 '161039')")]
) -> dict:
    """获取基金基本信息。"""
    info = fs.get_fund_info(code)
    return info if info else {"error": f"Failed to get fund info for {code}"}

# --- Main Execution Block ---
def main():
    fs_logger.info("Starting finshare MCP Server via stdio...")
    app.run(transport='stdio')

if __name__ == "__main__":
    main()
