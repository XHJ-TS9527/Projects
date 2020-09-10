# coding=utf-8
import pyecharts
import pyecharts.options as opts
import pandas as pd
import numpy as np
import sklearn.cluster as clustering


class Rear_Spacial_Visualization():

    def __init__(self):
        self.piece_number = 5
        self.random_state = 65535
        self.nameMap = {"阿富汗": "Afghanistan", "安哥拉": "Angola", "阿尔巴尼亚": "Albania", "阿尔及利亚": "Algeria",
                        "阿根廷": "Argentina", "亚美尼亚": "Armenia", "澳大利亚": "Australia", "奥地利": "Austria",
                        "阿塞拜疆": "Azerbaijan", "巴哈马": "Bahamas", "孟加拉": "Bangladesh", "比利时": "Belgium",
                        "贝宁": "Benin", "布基纳法索": "Burkina Faso", "布隆迪": "Burundi", "保加利亚": "Bulgaria",
                        "波黑": "Bosnia and Herz", "白俄罗斯": "Belarus", "伯利兹": "Belize",
                        "百慕大群岛": "Bermuda", "玻利维亚": "Bolivia", "巴西": "Brazil", "文莱": "Brunei",
                        "不丹": "Bhutan", "博茨瓦纳": "Botswana", "柬埔寨": "Cambodia", "喀麦隆": "Cameroon",
                        "加拿大": "Canada", "中非共和国": "Central African Rep.", "乍得": "Chad", "智利": "Chile",
                        "中国": "China", "哥伦比亚": "Colombia", "刚果（金）": "Congo", "哥斯达黎加": "Costa Rica",
                        "科特迪瓦": "Côte d'Ivoire", "克罗地亚": "Croatia", "古巴": "Cuba", "塞浦路斯": "Cyprus",
                        "捷克": "Czech Rep.", "朝鲜": "Dem.Rep.Korea", "刚果（布）": "Dem. Rep. Congo",
                        "丹麦": "Denmark", "吉布提": "Djibouti", "多米尼加": "Dominican Rep.", "厄瓜多尔": "Ecuador",
                        "埃及": "Egypt", "萨尔瓦多": "ElSalvador", "赤道几内亚": "Eq. Guinea", "厄立特里亚": "Eritrea",
                        "爱沙尼亚": "Estonia", "埃塞俄比亚": "Ethiopia", "福克兰群岛": "FalklandIs", "斐济": "Fiji",
                        "芬兰": "Finland", "法国": "France", "法属圭亚那": "FrenchGuiana",
                        "法属南部领地": "Fr.S.AntarcticLands", "加蓬": "Gabon", "冈比亚": "Gambia",
                        "德国": "Germany", "格鲁吉亚": "Georgia", "加纳": "Ghana", "希腊": "Greece",
                        "格陵兰": "Greenland", "危地马拉": "Guatemala", "几内亚": "Guinea", "几内亚比绍": "Guinea-Bissau",
                        "圭亚那": "Guyana", "海地": "Haiti", "赫德岛和麦克唐纳群岛": "HeardI.andMcDonaldIs",
                        "洪都拉斯": "Honduras", "匈牙利": "Hungary", "冰岛": "Iceland", "印度": "India",
                        "印度尼西亚": "Indonesia", "伊朗": "Iran", "伊拉克": "Iraq", "爱尔兰": "Ireland",
                        "以色列": "Israel", "意大利": "Italy", "象牙海岸": "IvoryCoast", "牙买加": "Jamaica",
                        "日本": "Japan", "约旦": "Jordan", "克什米尔": "Kashmir", "哈萨克斯坦": "Kazakhstan",
                        "肯尼亚": "Kenya", "科索沃": "Kosovo", "科威特": "Kuwait", "吉尔吉斯斯坦": "Kyrgyzstan",
                        "老挝": "Lao PDR", "拉脱维亚": "Latvia", "黎巴嫩": "Lebanon", "莱索托": "Lesotho",
                        "利比里亚": "Liberia", "利比亚": "Libya", "立陶宛": "Lithuania", "卢森堡": "Luxembourg",
                        "马达加斯加": "Madagascar", "北马其顿": "Macedonia", "马拉维": "Malawi", "马来西亚": "Malaysia",
                        "马里": "Mali", "毛里塔尼亚": "Mauritania", "墨西哥": "Mexico", "摩尔多瓦": "Moldova",
                        "蒙古": "Mongolia", "黑山": "Montenegro", "摩洛哥": "Morocco", "莫桑比克": "Mozambique",
                        "缅甸": "Myanmar", "纳米比亚": "Namibia", "荷兰": "Netherlands", "新喀里多尼亚": "New Caledonia",
                        "新西兰": "New Zealand", "尼泊尔": "Nepal", "尼加拉瓜": "Nicaragua", "尼日尔": "Niger",
                        "尼日利亚": "Nigeria", "韩国": "Korea", "北塞浦路斯": "NorthernCyprus", "挪威": "Norway",
                        "阿曼": "Oman", "巴基斯坦": "Pakistan", "巴拿马": "Panama", "巴布亚新几内亚": "Papua New Guinea",
                        "巴拉圭": "Paraguay", "秘鲁": "Peru", "刚果": "Republic of the Congo",
                        "菲律宾": "Philippines", "波兰": "Poland", "葡萄牙": "Portugal", "波多黎各": "Puerto Rico",
                        "卡塔尔": "Qatar", "塞尔维亚共和国": "Republic of Serbia", "罗马尼亚": "Romania",
                        "俄罗斯": "Russia", "卢旺达": "Rwanda", "萨摩亚": "Samoa", "沙特阿拉伯": "Saudi Arabia",
                        "塞内加尔": "Senegal", "塞尔维亚": "Serbia", "塞拉利昂": "Sierra Leone",
                        "斯洛伐克": "Slovakia", "斯洛文尼亚": "Slovenia", "所罗门群岛": "SolomonIs",
                        "索马里兰": "Somaliland", "索马里": "Somalia", "南非": "South Africa",
                        "南乔治亚和南桑德威奇群岛": "S.Geo.andS.Sandw.Is", "南苏丹": "S.Sudan",
                        "西班牙": "Spain", "斯里兰卡": "Sri Lanka", "苏丹": "Sudan", "苏里南": "Suriname",
                        "斯威士兰": "Swaziland", "瑞典": "Sweden", "瑞士": "Switzerland", "叙利亚": "Syria",
                        "塔吉克斯坦": "Tajikistan", "坦桑尼亚": "Tanzania", "泰国": "Thailand",
                        "东帝汶": "Timor-Leste", "多哥": "Togo", "特立尼达和多巴哥": "Trinidad and Tobago",
                        "突尼斯": "Tunisia", "土耳其": "Turkey", "土库曼斯坦": "Turkmenistan", "乌干达": "Uganda",
                        "乌克兰": "Ukraine", "阿联酋": "United Arab Emirates", "英国": "United Kingdom",
                        "坦桑尼亚联合共和国": "United Republic of Tanzania", "美国": "United States",
                        "美利坚合众国": "United States", "乌拉圭": "Uruguay", "乌兹别克斯坦": "Uzbekistan",
                        "瓦努阿图": "Vanuatu", "委内瑞拉": "Venezuela", "越南": "Vietnam", "西岸": "WestBank",
                        "西撒哈拉": "W.Sahara", "也门": "Yemen", "赞比亚": "Zambia", "津巴布韦": "Zimbabwe",
                        '新加坡': 'Singapore', '钻石号邮轮': '', '巴林': 'Bahrain', '安道尔': 'Andorra',
                        '圣马力诺': 'San Marino', '马耳他': 'Malta', '毛里求斯': 'Mauritius', '巴勒斯坦': 'Palestine',
                        '列支敦士登公国': 'Liechtenstein', '摩纳哥': 'Monaco', '马尔代夫': 'Maldives',
                        '塞舌尔': 'Seychelles', '安提瓜和巴布达': 'Antigua and Barb.', '佛得角': 'Cape Verde',
                        '梵蒂冈': 'Vatican', '科摩罗': 'Comoros', '巴巴多斯': 'Barbados', '马提尼克岛': 'Martinique',
                        '圣文森特和格林纳丁斯': 'St. Vin. and Gren.', '圣卢西亚': 'Saint Lucia',
                        '格林纳达': 'Grenada', '多米尼克': 'Dominica', '圣基茨和尼维斯': 'Saint Kitts and Nevis'}
        self.server_html_path = '/var/www/html/xhj/projects/small_projects/covid_19_spider_visualization/'

    def cluster_cut_pieces(self, to_piece_data, piece_number):
        # Prepare data
        cluster_data = np.array(to_piece_data)
        cluster_data = np.expand_dims(cluster_data, axis=1)
        cluster_data = np.hstack((cluster_data, np.zeros((cluster_data.shape[0], 1))))
        # Clustering
        model = clustering.KMeans(random_state=self.random_state, n_clusters=piece_number)
        model.fit(cluster_data)
        cluster_labels = model.labels_
        # Get the detail of each cluster
        lower_bound = []
        higher_bound = []
        for cluster_idx in range(piece_number):
            cluster = cluster_data[cluster_labels == cluster_idx][:, 0]
            lower_bound.append(cluster.min())
            higher_bound.append(cluster.max())
        # Sort the bounds
        lower_bound = np.array(lower_bound)
        higher_bound = np.array(higher_bound)
        sort_position = np.argsort(higher_bound)
        sorted_lower_bound = lower_bound[sort_position]
        sorted_higher_bound = higher_bound[sort_position]
        # Structure pieces
        pieces = []
        for cluster_idx in range(piece_number):
            if cluster_idx == piece_number - 1:
                piece = {'min': sorted_lower_bound[cluster_idx], 'max': sorted_higher_bound[cluster_idx] + 10,
                         'label': '>%d' % (sorted_lower_bound[cluster_idx] - 1, )}
            else:
                piece = {'min': sorted_lower_bound[cluster_idx], 'max': sorted_lower_bound[cluster_idx + 1] - 1,
                         'label': '%d ~ %d' % (sorted_lower_bound[cluster_idx], sorted_lower_bound[cluster_idx + 1] - 1)}
            pieces.append(piece)
        return pieces

    def visualize_domestic_today(self, data_type):
        # Load data and the update time
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[0, '更新时间']
        today_data_df = pd.read_csv('中国疫情数据-当日数据.csv')
        # Transfer the data to the form that pyecharts needs
            # extract province data
        province_data_df = today_data_df[today_data_df['省份'] == today_data_df['城市/地区']]
        province = province_data_df.loc[1:, '省份']
        confirmed = province_data_df.loc[1:, '现存确诊']
        accumulate_confirmed = province_data_df.loc[1:, '累计确诊']
        healed = province_data_df.loc[1:, '治愈']
        dead = province_data_df.loc[1:, '死亡']
            # merge the selected data
        if data_type == 'confirmed':
            chart_data_df = pd.concat([province, confirmed], axis=1)
            chart_real_data = confirmed
            title_str = '现存确诊人数'
        elif data_type == 'accumulate':
            chart_data_df = pd.concat([province, accumulate_confirmed], axis=1)
            chart_real_data = accumulate_confirmed
            title_str = '累计确诊人数'
        elif data_type == 'healed':
            chart_data_df = pd.concat([province, healed], axis=1)
            chart_real_data = healed
            title_str = '治愈人数'
        else:
            chart_data_df = pd.concat([province, dead], axis=1)
            chart_real_data = dead
            title_str = '死亡人数'
            # change to list and structure pieces
        chart_data = chart_data_df.values.tolist()
        piece = self.cluster_cut_pieces(chart_real_data, self.piece_number)
        # Plot the visualization chart
        map_chart = pyecharts.charts.Map()
        map_chart.add(series_name=title_str, data_pair=chart_data, maptype='china')
        map_chart.set_global_opts(title_opts=opts.TitleOpts(title='中国新冠疫情%s分布\n更新时间:%s' % (title_str, update_time)),
                                  visualmap_opts=opts.VisualMapOpts(pieces=piece, is_piecewise=True))
        map_chart.render('中国新冠疫情%s分布.html' % title_str)
        # Change the title of the webpage
        html_page = open('中国新冠疫情%s分布.html' % title_str, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '中国新冠疫情%s分布' % title_str,
                                      html_title_content[right_idx:])
        html_page = open('中国新冠疫情%s分布.html' % title_str, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the map object
        return map_chart

    def visualize_domestic_today_all(self):
        # Load data and the update time
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[0, '更新时间']
        today_data_df = pd.read_csv('中国疫情数据-当日数据.csv')
        # Extract the province data
        province_data_df = today_data_df[today_data_df['省份'] == today_data_df['城市/地区']]
        province = province_data_df.loc[1:, '省份']
        # Plot the data
        tabs = pyecharts.charts.Tab()
        for section_idx in range(2, province_data_df.shape[1]):
            title_str = '%s人数' % province_data_df.columns[section_idx]
            chart_real_data_df = province_data_df.iloc[1:, section_idx]
            chart_real_data = chart_real_data_df.values.tolist()
            piece = self.cluster_cut_pieces(chart_real_data, self.piece_number)
            chart_data = pd.concat([province, chart_real_data_df], axis=1)
            chart_data = chart_data.values.tolist()
            map_chart = pyecharts.charts.Map()
            map_chart.add(series_name=title_str, data_pair=chart_data, maptype='china')
            map_chart.set_global_opts(title_opts=opts.TitleOpts(title='中国新冠疫情%s分布\n更新时间:%s' % (title_str, update_time)),
                                      visualmap_opts=opts.VisualMapOpts(pieces=piece, is_piecewise=True))
            tabs.add(map_chart, '%s' % title_str)
        tabs.render('%sChina-Detail-Map.html' % self.server_html_path)
        # Change the title of the webpage
        html_page = open('%sChina-Detail-Map.html' % self.server_html_path, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '中国新冠疫情人数分布',
                                      html_title_content[right_idx:])
        html_page = open('%sChina-Detail-Map.html' % self.server_html_path, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the tab
        return tabs

    def visualize_foreign_today(self, data_type):
        # Load data and the update time
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[1, '更新时间']
        today_data_df = pd.read_csv('全球疫情数据-各国数据.csv')
            # China data
        China_data_df = pd.read_csv('中国疫情数据-国家统计.csv')
        # Transfer the data to the form that pyecharts needs
            # extract province data
        nation_data_df = pd.concat([today_data_df, pd.DataFrame({'所属洲': ['亚洲'], '国家': ['中国'],
                                                                 '更新日期':[0],
                                                                 '现存确诊': [China_data_df.loc[0, '现存确诊']],
                                                                 '累计确诊': [China_data_df.loc[0, '累计确诊']],
                                                                 '治愈': [China_data_df.loc[0, '治愈']],
                                                                 '死亡': [China_data_df.loc[0, '死亡']]})],
                                   axis=0)
        nation = nation_data_df.loc[:, '国家']
        nation = nation.agg(lambda x: self.nameMap[x])
        confirmed = nation_data_df.loc[:, '现存确诊']
        accumulate_confirmed = nation_data_df.loc[:, '累计确诊']
        healed = nation_data_df.loc[:, '治愈']
        dead = nation_data_df.loc[:, '死亡']
            # merge the selected data
        if data_type == 'confirmed':
            chart_data_df = pd.concat([nation, confirmed], axis=1)
            chart_real_data = confirmed
            title_str = '现存确诊人数'
        elif data_type == 'accumulate':
            chart_data_df = pd.concat([nation, accumulate_confirmed], axis=1)
            chart_real_data = accumulate_confirmed
            title_str = '累计确诊人数'
        elif data_type == 'healed':
            chart_data_df = pd.concat([nation, healed], axis=1)
            chart_real_data = healed
            title_str = '治愈人数'
        else:
            chart_data_df = pd.concat([nation, dead], axis=1)
            chart_real_data = dead
            title_str = '死亡人数'
            # change to list and structure pieces
        chart_data = chart_data_df.values.tolist()
        piece = self.cluster_cut_pieces(chart_real_data, self.piece_number)
        # Plot the visualization chart
        map_chart = pyecharts.charts.Map()
        map_chart.add(series_name=title_str, data_pair=chart_data, maptype='world')
        map_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        map_chart.set_global_opts(title_opts=opts.TitleOpts(title='全球新冠疫情%s分布\n更新时间:%s (UTC +8)' %
                                                                  (title_str, update_time)),
                                  visualmap_opts=opts.VisualMapOpts(pieces=piece, is_piecewise=True))
        map_chart.render('全球新冠疫情%s分布.html' % title_str)
        # Change the title of the webpage
        html_page = open('全球新冠疫情%s分布.html' % title_str, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '全球新冠疫情%s分布' % title_str,
                                      html_title_content[right_idx:])
        html_page = open('全球新冠疫情%s分布.html' % title_str, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the map object
        return map_chart

    def visualize_foreign_today_all(self):
        # Load data and the update time
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[1, '更新时间']
        today_data_df = pd.read_csv('全球疫情数据-各国数据.csv')
        # China data
        China_data_df = pd.read_csv('中国疫情数据-国家统计.csv')
        # Transfer the data to the form that pyecharts needs
            # add Chinese data
        nation_data_df = pd.concat([today_data_df, pd.DataFrame({'所属洲': ['亚洲'], '国家': ['中国'],
                                                                 '更新日期': [0],
                                                                 '现存确诊': [China_data_df.loc[0, '现存确诊']],
                                                                 '累计确诊': [China_data_df.loc[0, '累计确诊']],
                                                                 '治愈': [China_data_df.loc[0, '治愈']],
                                                                 '死亡': [China_data_df.loc[0, '死亡']]})],
                                   axis=0)
        nation = nation_data_df.loc[:, '国家']
        nation = nation.agg(lambda x: self.nameMap[x])
        # Plot the chart
        tabs = pyecharts.charts.Tab()
        for section_idx in range(3, today_data_df.shape[1]):
            title_str = '%s人数' % nation_data_df.columns[section_idx]
            chart_real_data_df = nation_data_df.iloc[:, section_idx]
            chart_real_data = chart_real_data_df.values.tolist()
            piece = self.cluster_cut_pieces(chart_real_data, self.piece_number)
            chart_data = pd.concat([nation, chart_real_data_df], axis=1)
            chart_data = chart_data.values.tolist()
            map_chart = pyecharts.charts.Map()
            map_chart.add(series_name=title_str, data_pair=chart_data, maptype='world')
            map_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            map_chart.set_global_opts(title_opts=opts.TitleOpts(title='全球新冠疫情%s分布\n更新时间:%s' % (title_str, update_time)),
                                      visualmap_opts=opts.VisualMapOpts(pieces=piece, is_piecewise=True))
            tabs.add(map_chart, '%s' % title_str)
        tabs.render('%sGlobal-Detail-Map.html' % self.server_html_path)
        # Change the title of the webpage
        html_page = open('%sGlobal-Detail-Map.html' % self.server_html_path, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '全球新冠疫情人数分布',
                                      html_title_content[right_idx:])
        html_page = open('%sGlobal-Detail-Map.html' % self.server_html_path, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the tab
        return tabs

    def main(self, server=True):
        if server:
            self.visualize_domestic_today_all()
            self.visualize_foreign_today_all()
        else:
            self.visualize_domestic_today('confirmed')
            self.visualize_domestic_today('accumulate')
            self.visualize_domestic_today('healed')
            self.visualize_domestic_today('dead')
            self.visualize_foreign_today('confirmed')
            self.visualize_foreign_today('accumulate')
            self.visualize_foreign_today('healed')
            self.visualize_foreign_today('dead')


if __name__ == '__main__':
    M = Rear_Spacial_Visualization()
    M.main(False)
