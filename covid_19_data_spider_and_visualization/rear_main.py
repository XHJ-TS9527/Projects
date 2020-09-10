# coding=utf-8
from support_tools import crawl_data, spacial_visualization_rear, temporal_visualization_rear
import warnings
import pandas as pd
import time


class MainActivity():

    def __init__(self):
        self.server_html_path = '/var/www/html/xhj/projects/small_projects/covid_19_spider_visualization/'

    def update_info(self):
        # Crawl the data
        spider = crawl_data.Crawl_Spyder()
        spider.main()
        # Update spacial visualization
        spacial_visualizer = spacial_visualization_rear.Rear_Spacial_Visualization()
        spacial_visualizer.main()
        # Update temporal visualization
        temporal_visualizer = temporal_visualization_rear.Rear_Temporal_Visualization()
        temporal_visualizer.main()

    def update_surface(self):
        # Data update time
        data_update_time_df = pd.read_csv('疫情数据更新时间.csv', dtype={'更新时间': object})
        China_update_time = data_update_time_df.loc[0, '更新时间']
        Global_update_time = data_update_time_df.loc[1, '更新时间']
        # Surface update time
        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # Get the countries that have history data
        countries_file = open('具备历史数据的国家.txt', 'rt')
        countries = countries_file.read().replace('\n', '').split(',')
        countries_file.close()
        # Structure data link of each country
        links = ['<a href="http://49.234.68.36/xhj/projects/small_projects/covid_19_spider_visualization/Global-History-%s.html" \
         target="_blank">%s数据</a>' % (country, country) for country in countries]
        del links[0]
        link_html = '<br />'.join(links)
        # Format the html file
        origin_html = open('main_page.txt', 'rt', encoding='utf-8')
        origin_html_text = origin_html.read()
        origin_html.close()
        html = origin_html_text % (local_time, China_update_time, link_html, Global_update_time)
        with open('%smain-page.html' % self.server_html_path, 'wt') as target_html_page:
            target_html_page.write(html)
            target_html_page.close()

    def main(self):
        warnings.filterwarnings('ignore')
        self.update_info()
        self.update_surface()


if __name__ == '__main__':
    M = MainActivity()
    M.main()
