# 电商知识库测试

## GMV（总销售额）

GMV 是 Gross Merchandise Volume 的缩写，代表平台在指定时间内的总销售额。
在 Olist 数据集中，GMV 通过 olist_order_items 表的 price 字段求和计算。
只统计状态为 delivered 的订单。

## 客单价（AOV）

客单价即 Average Order Value，指平均每个订单的金额。
计算公式：总 GMV 除以 总订单数。客单价反映了用户的平均消费水平。

## 复购率

复购率是指在一段时间内重复购买的用户占总购买用户的比例。
Olist 数据中可以通过 customer_unique_id 跨订单统计来计算复购率。
高复购率通常意味着用户粘性强、产品满意度高。

## 延迟配送

当订单实际送达日期（order_delivered_customer_date）晚于预计送达日期
（order_estimated_delivery_date）时，视为延迟配送。延迟配送率 =
延迟配送订单数 / 总已完成配送订单数 × 100%。

## 热销品类分析

Olist 数据集中品类信息存储在 product_category_name_translation 表中。
热销品类按 GMV 贡献排名，需要 join olist_order_items 和 olist_products 表。
