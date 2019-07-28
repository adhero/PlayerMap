# PlayerMap
Players' region distribution of Europe's top five leagues on world map

本项目旨在通过爬取腾讯体育五大联赛球员信息，使用pyecharts将球员的地区分布可视化，分析五大联赛球员的主要来源和可能原因。

问题：
1. 代码逻辑不够清晰，代码重复率高
2. 腾讯体育球员信息数量少，更新慢，缺省值多，对结果影响较大
3. 世界各国家地区与各国足球协会并非一一对应，且各国的英文译名可能存在差异，所以可视化的过程中会出现地区名称不对应，不够精确的情况。比如：刚果金和民主刚果同属一个国家；pyecharts的地区键值只包含United Kingdom，无法细分到England，Scotland进行可视化
4. 对于使用多线程写文件尚不能确定是否可能有冲突导致信息丢失
