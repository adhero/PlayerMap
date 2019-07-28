# usr/bin/env python3;
#-*-coding: utf-8-*-

from pyecharts.charts import Map, Geo
from pyecharts.globals import GeoType
from pyecharts import options as opts
from flush_data import flush_data
import os

attr, value = flush_data()
print([list(z) for z in zip(attr, value)])
print(sum(value))
# 使用map绘制地图
def map_world() -> Map:
    c = (
        Map()
        .add("球员数量", [list(z) for z in zip(attr, value)], "world", is_map_symbol_show=True)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-世界地图五大联赛球员分布"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    return c

c = map_world()
c.render("geoplayer/render.html")