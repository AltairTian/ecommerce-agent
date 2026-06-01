"""报告路由 —— 经营报告查询接口。"""

import logging

from fastapi import APIRouter, HTTPException

from src.tools.reports import (
    generate_daily_report,
    generate_sales_report,
    generate_delivery_report,
    generate_category_report,
    generate_full_report,
)

logger = logging.getLogger("api")
router = APIRouter()

# 可用报告注册表
_REPORTS = {
    "daily": {
        "name": "日经营报告",
        "description": "当日核心指标概览：GMV、订单数、客单价、评分、配送",
        "func": generate_daily_report,
    },
    "sales": {
        "name": "销售分析报告",
        "description": "销售趋势、地区排行、支付方式分布",
        "func": generate_sales_report,
    },
    "delivery": {
        "name": "配送分析报告",
        "description": "平均配送时长、延迟配送率",
        "func": generate_delivery_report,
    },
    "category": {
        "name": "品类分析报告",
        "description": "品类销售排行、低评分品类、商品排行",
        "func": generate_category_report,
    },
    "full": {
        "name": "完整经营分析报告",
        "description": "包含销售、配送、品类、订单状态和客户分析的综合报告",
        "func": generate_full_report,
    },
}


@router.get("/reports")
async def list_reports():
    """列出所有可用的报告类型。"""
    items = [
        {
            "type": key,
            "name": info["name"],
            "description": info["description"],
        }
        for key, info in _REPORTS.items()
    ]
    return {"count": len(items), "reports": items}


@router.get("/reports/{report_type}")
async def generate_report(report_type: str):
    """生成指定类型的经营报告。

    路径参数 `report_type` 可选值：daily / sales / delivery / category / full
    """
    report_type = report_type.lower().strip()

    if report_type not in _REPORTS:
        raise HTTPException(
            status_code=404,
            detail=f"未知报告类型 '{report_type}'，可用类型：{', '.join(_REPORTS.keys())}",
        )

    try:
        report_func = _REPORTS[report_type]["func"]
        content = report_func()
        return {
            "type": report_type,
            "name": _REPORTS[report_type]["name"],
            "content": content,
        }
    except Exception as e:
        logger.exception("Failed to generate report '%s'", report_type)
        raise HTTPException(
            status_code=500,
            detail=f"报告生成失败：{str(e)}",
        )
