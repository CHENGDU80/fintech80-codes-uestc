import pyecharts.options as opts
from pyecharts.charts import Bar, Line, Pie, WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import random
import pandas as pd
from config import *


def generate_page_1_charts():
    historicalLineChartData = pd.read_csv('data/historicalLineChartData.csv')
    historicalLineChart = (Line(init_opts=opts.InitOpts(
        width=HISTORICAL_DATA_WIDTH, height=HISTORICAL_DATA_HEIGHT)).add_xaxis(
            xaxis_data=historicalLineChartData['Date'].values.tolist()
        ).add_yaxis(
            series_name=historicalLineChartData.columns.tolist()[1],
            y_axis=historicalLineChartData['brent oil'].values.tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        ).add_yaxis(
            series_name=historicalLineChartData.columns.tolist()[2],
            y_axis=historicalLineChartData['gold'].values.tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        ).add_yaxis(
            series_name=historicalLineChartData.columns.tolist()[4],
            y_axis=historicalLineChartData['silver'].values.tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        ).add_yaxis(
            series_name=historicalLineChartData.columns.tolist()[5],
            y_axis=historicalLineChartData['wheat'].values.tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        ).set_global_opts(title_opts=opts.TitleOpts(
            title="", title_textstyle_opts=opts.TextStyleOpts(
                font_size=23))).render(HTML_PATH + "historicalLineChart.html"))
    wordCloudData = pd.read_csv('data/wordCloudData.csv').values.tolist()
    wordCloud = (WordCloud(init_opts=opts.InitOpts(
        width=WORD_CLOUD_WIDTH, height=WORD_CLOUD_HEIGHT)).add(
            "", data_pair=wordCloudData).set_global_opts(
                title_opts=opts.TitleOpts(title=""),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                legend_opts=opts.LegendOpts(is_show=False),
            ).render(HTML_PATH + "wordCloud.html"))


def generate_page_2_charts():
    newsTrendingLineChartData = pd.read_csv(
        'data/newsTrendingLineChartData.csv')
    newsTrendingLineChart = (
        Line(init_opts=opts.InitOpts(width=NEWS_TRENDING_LINE_CHART_WIDTH,
                                     height=NEWS_TRENDING_LINE_CHART_HEIGHT)).
        add_xaxis(xaxis_data=newsTrendingLineChartData['date'].values.tolist(
        )).add_yaxis(
            series_name=newsTrendingLineChartData.columns.tolist()[1],
            y_axis=newsTrendingLineChartData['comment'].values.tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        ).set_global_opts(title_opts=opts.TitleOpts(title=""),
                          # legend_opts=opts.LegendOpts(is_show=False),
                          ).render(HTML_PATH + "newsTrendingLineChart.html"))
    historyPriceScoreLineChartData = pd.read_csv(
        'data/historyPriceScoreLineChartData.csv')
    historyPriceScoreLineChart = (Line(
        init_opts=opts.InitOpts(width=HISTORY_PRICE_SCORE_LINE_CHART_WIDTH,
                                height=HISTORY_PRICE_SCORE_LINE_CHART_HEIGHT)
    ).add_xaxis(
        xaxis_data=historyPriceScoreLineChartData['date'].values.tolist()
    ).add_yaxis(
        series_name='score of Supply&Demand',
        y_axis=historyPriceScoreLineChartData['1_score'].values.tolist(),
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(
        series_name='score of Geopolitical event',
        y_axis=historyPriceScoreLineChartData['2_score'].values.tolist(),
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(
        series_name='score of OPEC',
        y_axis=historyPriceScoreLineChartData['3_score'].values.tolist(),
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(
        series_name='score of Oil Inventories',
        y_axis=historyPriceScoreLineChartData['4_score'].values.tolist(),
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(
        series_name=historyPriceScoreLineChartData.columns.tolist()[5],
        y_axis=historyPriceScoreLineChartData['total_score'].values.tolist(),
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    ).set_global_opts(title_opts=opts.TitleOpts(
        title=""), ).render(HTML_PATH + "historyPriceScoreLineChart.html"))


if __name__ == '__main__':
    generate_page_1_charts()
    generate_page_2_charts()
