"""
示例 11: 证券列表获取

演示如何获取股票、ETF、LOF、期货等列表数据。
"""

import finshare as fs


def main():
    """运行证券列表获取示例"""

    fs.logger.info("=" * 60)
    fs.logger.info("finshare 证券列表获取示例")
    fs.logger.info("=" * 60)

    # 1. 获取A股股票列表
    fs.logger.info("\n=== 获取A股股票列表 ===")

    try:
        stocks = fs.get_stock_list(market="all")
        fs.logger.info(f"✓ 成功获取 {len(stocks)} 只股票")

        # 显示前10只
        fs.logger.info("\n股票列表 (前10只):")
        fs.logger.info("-" * 60)
        fs.logger.info(f"{'代码':<12} {'名称':<20} {'最新价':<12} {'涨跌幅':<10}")
        fs.logger.info("-" * 60)

        for stock in stocks[:10]:
            change_pct = stock.get("change_pct", 0)
            fs.logger.info(
                f"{stock.get('code'):<12} "
                f"{stock.get('name', '')[:20]:<20} "
                f"{stock.get('price', 0):<12.2f} "
                f"{change_pct:>+9.2f}%"
            )

    except Exception as e:
        fs.logger.error(f"获取股票列表失败: {e}")

    # 2. 获取ETF列表
    fs.logger.info("\n=== 获取ETF基金列表 ===")

    try:
        etfs = fs.get_etf_list()
        fs.logger.info(f"✓ 成功获取 {len(etfs)} 只ETF")

        # 显示前10只
        fs.logger.info("\nETF列表 (前10只):")
        fs.logger.info("-" * 60)
        fs.logger.info(f"{'代码':<12} {'名称':<30} {'最新价':<12} {'涨跌幅':<10}")
        fs.logger.info("-" * 60)

        for etf in etfs[:10]:
            change_pct = etf.get("change_pct", 0)
            fs.logger.info(
                f"{etf.get('code'):<12} "
                f"{etf.get('name', '')[:30]:<30} "
                f"{etf.get('price', 0):<12.2f} "
                f"{change_pct:>+9.2f}%"
            )

    except Exception as e:
        fs.logger.error(f"获取ETF列表失败: {e}")

    # 3. 获取LOF列表
    fs.logger.info("\n=== 获取LOF基金列表 ===")

    try:
        lofs = fs.get_lof_list()
        fs.logger.info(f"✓ 成功获取 {len(lofs)} 只LOF")

        # 显示前10只
        fs.logger.info("\nLOF列表 (前10只):")
        fs.logger.info("-" * 60)

        for lof in lofs[:10]:
            fs.logger.info(f"  {lof.get('code')}: {lof.get('name')}")

    except Exception as e:
        fs.logger.error(f"获取LOF列表失败: {e}")

    # 4. 提示
    fs.logger.info("\n" + "=" * 60)
    fs.logger.info("提示:")
    fs.logger.info("  - get_stock_list(market='all') 获取全部股票")
    fs.logger.info("  - get_stock_list(market='sh') 获取上海股票")
    fs.logger.info("  - get_stock_list(market='sz') 获取深圳股票")
    fs.logger.info("  - 数据来源: EastMoney (东方财富)")
    fs.logger.info("  - 列表数据包含实时行情，可用于筛选")


if __name__ == "__main__":
    main()
