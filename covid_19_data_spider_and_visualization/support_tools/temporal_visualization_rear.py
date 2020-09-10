# coding=utf-8
import pyecharts
import pyecharts.options as opt
import pandas as pd


class Rear_Temporal_Visualization():

    def __init__(self):
        self.color = {'confirmed': 'orange', 'accumulate': 'red', 'healed': 'green', 'dead': 'grey'}
        self.Chinese_map = {1: 'confirmed', 2: 'accumulate', 3: 'healed', 4: 'dead'}
        self.Global_map = {1: 'accumulate', 2: 'healed', 3: 'dead'}
        self.server_html_path = '/var/www/html/xhj/projects/small_projects/covid_19_spider_visualization/'

    def visualize_domestic_history(self, data_type):
        # Load the data
        history_data = pd.read_csv('中国疫情数据-历史数据.csv', dtype={'日期': object})
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[0, '更新时间']
        # Transfer the data to the data that echarts needs
        date_df = history_data.loc[:, '日期']
        dates = date_df.values.tolist()
        if data_type == 'confirmed':
            chart_data_df = history_data.loc[:, '现存确诊']
            title_str = '现存确诊人数'
        elif data_type == 'accumulate':
            chart_data_df = history_data.loc[:, '累计确诊']
            title_str = '累计确诊人数'
        elif data_type == 'healed':
            chart_data_df = history_data.loc[:, '治愈']
            title_str = '治愈人数'
        else:
            chart_data_df = history_data.loc[:, '死亡']
            title_str = '死亡人数'
        chart_data = chart_data_df.values.tolist()
        # Plot the visualization chart
        smoothline_chart = pyecharts.charts.Line()
        smoothline_chart.add_xaxis(dates)
        smoothline_chart.add_yaxis(title_str, chart_data, is_smooth=True, symbol_size=10,
                                   linestyle_opts=opt.LineStyleOpts(color=self.color[data_type], width=3),
                                   itemstyle_opts=opt.ItemStyleOpts(border_color=self.color[data_type],
                                                                    color=self.color[data_type]))
        smoothline_chart.set_global_opts(title_opts=opt.TitleOpts(title='中国新冠疫情%s历史数据\n更新时间:%s' %
                                                                  (title_str, update_time)))
        smoothline_chart.render('中国新冠疫情%s历史数据.html' % title_str)
        # Change the title of the webpage
        html_page = open('中国新冠疫情%s历史数据.html' % title_str, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '中国新冠疫情%s历史数据' % title_str,
                                      html_title_content[right_idx:])
        html_page = open('中国新冠疫情%s历史数据.html' % title_str, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the map object
        return smoothline_chart

    def visualize_domestic_history_all(self):
        # Load the data
        history_data = pd.read_csv('中国疫情数据-历史数据.csv', dtype={'日期': object})
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[0, '更新时间']
        # Transfer the data to the data that echarts needs
        date_df = history_data.loc[:, '日期']
        dates = date_df.values.tolist()
        # Plot the data
        tabs = pyecharts.charts.Tab()
        for section_idx in range(1, history_data.shape[1]):
            title_str = '%s人数' % history_data.columns[section_idx]
            chart_data_df = history_data.iloc[:, section_idx]
            chart_data = chart_data_df.values.tolist()
            data_type = self.Chinese_map[section_idx]
            # Plot the visualization chart
            smoothline_chart = pyecharts.charts.Line()
            smoothline_chart.add_xaxis(dates)
            smoothline_chart.add_yaxis(title_str, chart_data, is_smooth=True, symbol_size=10,
                                       linestyle_opts=opt.LineStyleOpts(color=self.color[data_type], width=3),
                                       itemstyle_opts=opt.ItemStyleOpts(border_color=self.color[data_type],
                                                                        color=self.color[data_type]))
            smoothline_chart.set_global_opts(title_opts=opt.TitleOpts(title='中国新冠疫情%s历史数据\n更新时间:%s' %
                                                                            (title_str, update_time)))
            tabs.add(smoothline_chart, title_str)
        # Save the chart
        tabs.render('%sChina-History-Visualization.html' % self.server_html_path)
        # Change the title of the webpage
        html_page = open('%sChina-History-Visualization.html' % self.server_html_path, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '中国新冠疫情历史数据',
                                      html_title_content[right_idx:])
        html_page = open('%sChina-History-Visualization.html' % self.server_html_path, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the map object
        return tabs

    def visualize_foreign_history(self):
        # Load the country list
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[1, '更新时间']
        country_list_file = open('具备历史数据的国家.txt', 'rt')
        country_list = country_list_file.read().split(',')
        country_list_file.close()
        del country_list[0]
        # Process each country
        charts = []
        for each_country in country_list:
            # load the history data of that country
            country_history_data = pd.read_csv('全球疫情数据-【%s】历史数据.csv' % each_country, dtype={'日期': object})
            dates_df = country_history_data.loc[:, '日期']
            dates = dates_df.values.tolist()
            confirmed_df = country_history_data.loc[:, '现存确诊']
            confirmed = confirmed_df.values.tolist()
            # plot the chart and save
            smoothline_chart = pyecharts.charts.Line()
            smoothline_chart.add_xaxis(dates)
            smoothline_chart.add_yaxis('现存确诊人数', confirmed, is_smooth=True, symbol_size=10,
                                       linestyle_opts=opt.LineStyleOpts(color='orange', width=3),
                                       itemstyle_opts=opt.ItemStyleOpts(border_color='orange', color='orange'))
            smoothline_chart.set_global_opts(title_opts=opt.TitleOpts(title='%s新冠疫情现存确诊人数历史数据\n更新时间:%s (UTC +8)'
                                                                            % (each_country, update_time)))
            smoothline_chart.render('%s新冠疫情现存确诊人数历史数据.html' % each_country)
            # change the title of the webpage
            html_page = open('%s新冠疫情现存确诊人数历史数据.html' % each_country, 'rt')
            html_content = html_page.readlines()
            html_page.close()
            html_title_content = html_content[4]
            left_idx = html_title_content.find('>')
            right_idx = html_title_content.rfind('</')
            html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '%s新冠疫情现存确诊人数历史数据' % each_country,
                                          html_title_content[right_idx:])
            html_page = open('%s新冠疫情现存确诊人数历史数据.html' % each_country, 'wt', encoding='utf-8')
            html_page.writelines(html_content)
            html_page.close()
            # save the chart to the dictionary
            charts.append(smoothline_chart)
        # Return the charts
        return charts

    def visualize_foreign_history_all(self):
        # Load the country list
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[1, '更新时间']
        country_list_file = open('具备历史数据的国家.txt', 'rt')
        country_list = country_list_file.read().split(',')
        country_list_file.close()
        del country_list[0]
        # Process each country
        tabs = pyecharts.charts.Tab()
        for each_country in country_list:
            # load the history data of that country
            country_history_data = pd.read_csv('全球疫情数据-【%s】历史数据.csv' % each_country, dtype={'日期': object})
            dates_df = country_history_data.loc[:, '日期']
            dates = dates_df.values.tolist()
            confirmed_df = country_history_data.loc[:, '现存确诊']
            confirmed = confirmed_df.values.tolist()
            # plot the chart and save
            smoothline_chart = pyecharts.charts.Line()
            smoothline_chart.add_xaxis(dates)
            smoothline_chart.add_yaxis('现存确诊人数', confirmed, is_smooth=True, symbol_size=10,
                                       linestyle_opts=opt.LineStyleOpts(color='orange', width=3),
                                       itemstyle_opts=opt.ItemStyleOpts(border_color='orange', color='orange'))
            smoothline_chart.set_global_opts(title_opts=opt.TitleOpts(title='%s新冠疫情现存确诊人数历史数据\n更新时间:%s (UTC +8)'
                                                                            % (each_country, update_time)))
            tabs.add(smoothline_chart, each_country)
        tabs.render('%sCountry-History-Visualization.html' % self.server_html_path)
        # change the title of the webpage
        html_page = open('%sCountry-History-Visualization.html' % self.server_html_path, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '各国现存确诊人数历史数据',
                                          html_title_content[right_idx:])
        html_page = open('%sCountry-History-Visualization.html' % self.server_html_path, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # return the tab
        return tabs

    def visualize_global_history(self, data_type):
        # Load the data
        history_data = pd.read_csv('全球疫情数据-【全球】历史数据.csv', dtype={'日期': object})
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[1, '更新时间']
        # Transfer data to the structure that echarts needs
        dates_df = history_data.loc[:, '日期']
        dates = dates_df.values.tolist()
        if data_type == 'accumulate':
            chart_data_df = history_data.loc[:, '累计确诊']
            title_str = '累计确诊人数'
        elif data_type == 'healed':
            chart_data_df = history_data.loc[:, '治愈']
            title_str = '治愈人数'
        else:
            chart_data_df = history_data.loc[:, '死亡']
            title_str = '死亡人数'
        chart_data = chart_data_df.values.tolist()
        # Plot the visualization chart
        smoothline_chart = pyecharts.charts.Line()
        smoothline_chart.add_xaxis(dates)
        smoothline_chart.add_yaxis(title_str, chart_data, is_smooth=True, symbol_size=10,
                                   linestyle_opts=opt.LineStyleOpts(width=3, color=self.color[data_type]),
                                   itemstyle_opts=opt.ItemStyleOpts(border_color=self.color[data_type],
                                                                    color=self.color[data_type]))
        smoothline_chart.set_global_opts(title_opts=opt.TitleOpts(title='全球新冠疫情%s历史数据\n更新时间:%s (UTC +8)'
                                                                  % (title_str, update_time)))
        smoothline_chart.render('全球新冠疫情%s历史数据.html' % title_str)
        # Change the title of the webpage
        html_page = open('全球新冠疫情%s历史数据.html' % title_str, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '全球新冠疫情%s历史数据' % title_str,
                                      html_title_content[right_idx:])
        html_page = open('全球新冠疫情%s历史数据.html' % title_str, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the chart
        return smoothline_chart

    def visualize_global_history_all(self):
        # Load the data
        history_data = pd.read_csv('全球疫情数据-【全球】历史数据.csv', dtype={'日期': object})
        update_time_df = pd.read_csv('疫情数据更新时间.csv')
        update_time = update_time_df.loc[1, '更新时间']
        # Transfer data to the structure that echarts needs and plot
        dates_df = history_data.loc[:, '日期']
        dates = dates_df.values.tolist()
        tabs = pyecharts.charts.Tab()
        # Process each section
        for section_idx in range(1, history_data.shape[1]):
            title_str = '%s人数' % history_data.columns[section_idx]
            chart_data_df = history_data.iloc[:, section_idx]
            chart_data = chart_data_df.values.tolist()
            data_type = self.Global_map[section_idx]
            # Plot the visualization chart
            smoothline_chart = pyecharts.charts.Line()
            smoothline_chart.add_xaxis(dates)
            smoothline_chart.add_yaxis(title_str, chart_data, is_smooth=True, symbol_size=10,
                                       linestyle_opts=opt.LineStyleOpts(width=3, color=self.color[data_type]),
                                       itemstyle_opts=opt.ItemStyleOpts(border_color=self.color[data_type],
                                                                        color=self.color[data_type]))
            smoothline_chart.set_global_opts(title_opts=opt.TitleOpts(title='全球新冠疫情%s历史数据\n更新时间:%s (UTC +8)'
                                                                            % (title_str, update_time)))
            tabs.add(smoothline_chart, title_str)
        tabs.render('%sGlobal-History-Visualization.html' % self.server_html_path)
        # Change the title of the webpage
        html_page = open('%sGlobal-History-Visualization.html' % self.server_html_path, 'rt')
        html_content = html_page.readlines()
        html_page.close()
        html_title_content = html_content[4]
        left_idx = html_title_content.find('>')
        right_idx = html_title_content.rfind('</')
        html_content[4] = '%s%s%s' % (html_title_content[:left_idx + 1], '全球新冠疫情历史数据',
                                      html_title_content[right_idx:])
        html_page = open('%sGlobal-History-Visualization.html' % self.server_html_path, 'wt', encoding='utf-8')
        html_page.writelines(html_content)
        html_page.close()
        # Return the tab
        return tabs

    def main(self, server=True):
        if server:
            self.visualize_domestic_history_all()
            self.visualize_foreign_history_all()
            self.visualize_global_history_all()
        else:
            self.visualize_domestic_history('confirmed')
            self.visualize_domestic_history('accumulate')
            self.visualize_domestic_history('healed')
            self.visualize_domestic_history('dead')
            self.visualize_foreign_history()
            self.visualize_global_history('accumulate')
            self.visualize_global_history('healed')
            self.visualize_global_history('dead')


if __name__ == '__main__':
    M = Rear_Temporal_Visualization()
    M.main(False)
