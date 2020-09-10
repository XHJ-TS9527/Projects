# coding=utf-8
import requests
import chardet
import json
import pandas as pd


class Crawl_Spyder():

    def __init__(self):
        self.domestic_history_src_url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList'
        self.domestic_today_src_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34102442326153314225_1599438698036&_=1599438698037'
        self.global_statistic_src_url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis'
        self.foreign_history_src_url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryMerge'
        self.foreign_today_src_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=jQuery34102278363527813223_1599443016035&_=1599443016036'
        self.countries_today_src_url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'}
        self.server_html_path = '/var/www/html/xhj/projects/small_projects/covid_19_spider_visualization/'

    def crawl_service(self, category='domestic'):
        # Switch URL
        statistic_url = self.domestic_today_src_url if category == 'domestic' else self.global_statistic_src_url
        history_url = self.domestic_history_src_url if category == 'domestic' else self.foreign_history_src_url
        today_url = self.domestic_today_src_url if category == 'domestic' else self.foreign_today_src_url
        # Get the data from Tencent
        statistic_response = requests.get(statistic_url, headers=self.header)
        history_response = requests.get(history_url, headers=self.header)
        today_response = requests.get(today_url, headers=self.header)
        # Get the most possible charset and set the charset to the response
        statistic_charset = chardet.detect(statistic_response.content)['encoding']
        history_charset = chardet.detect(history_response.content)['encoding']
        today_charset = chardet.detect(today_response.content)['encoding']
        statistic_response.encoding = statistic_charset
        history_response.encoding = history_charset
        today_response.encoding = today_charset
        # Get the text and change json string to dict
            # statistical data need preprocessing
        statistic_data_left_idx = statistic_response.text.find('(')
        statistic_data_right_idx = statistic_response.text.rfind(')')
        statistic_data = json.loads(statistic_response.text)['data'] if statistic_data_left_idx < 0 else json.loads(
            statistic_response.text[statistic_data_left_idx + 1:statistic_data_right_idx])['data']
        history_data = json.loads(history_response.text)['data']
            # today's data need preprocessing
        today_data_left_idx = today_response.text.find('(')
        today_data_right_idx = today_response.text.rfind(')')
        today_data = json.loads(today_response.text[today_data_left_idx + 1:today_data_right_idx])
        today_data = json.loads(today_data['data'])
        return statistic_data, history_data, today_data

    def crawl_foreign_service(self):
        # Get the data from Tencent
        response = requests.get(self.countries_today_src_url, headers=self.header)
        # Get the most possible charset and set the charset to the response
        possible_charset = chardet.detect(response.content)['encoding']
        response.encoding = possible_charset
        # Get the text and change json string to dict
        return json.loads(response.text)['data']

    def update_date_store(self, region, update_time):
        try:
            open('疫情数据更新时间.csv', 'rt')
        except:
            init_dict = {'区域': ['中国', '全球'], '更新时间': [' ', ' ']}
            init_df = pd.DataFrame(init_dict)
            init_df.to_csv('疫情数据更新时间.csv', index=False)
        finally:
            update_time_data = pd.read_csv('疫情数据更新时间.csv')
            row_idx = 0 if region == 'domestic' else 1
            update_time_data.loc[row_idx, '更新时间'] = update_time
            update_time_data.to_csv('疫情数据更新时间.csv', index=False)

    def crawl_domestic_epidemic(self, server=True):
        # Get the data
        _, history_data, today_data = self.crawl_service('domestic')
        history_data = history_data['chinaDayList']
        # Reshape the received today data into dataframe
            # today's data
        province = []
        city = []
        confirmed = []
        accumulate_confirmed = []
        healed = []
        dead = []
                # whole country
        today_update_time = today_data['lastUpdateTime']
        today_whole_country_data = today_data['chinaTotal']
        province.append('中国')
        city.append('中国')
        confirmed.append(today_whole_country_data['nowConfirm'])
        accumulate_confirmed.append(today_whole_country_data['confirm'])
        healed.append(today_whole_country_data['heal'])
        dead.append(today_whole_country_data['dead'])
                # each province and their children cities
        province_tree = today_data['areaTree'][0]['children']
        for each_province in province_tree:
            province_name = each_province['name']
            province_total_data = each_province['total']
                    # add the province data to the list
            province.append(province_name)
            city.append(province_name)
            confirmed.append(province_total_data['nowConfirm'])
            accumulate_confirmed.append(province_total_data['confirm'])
            healed.append(province_total_data['heal'])
            dead.append(province_total_data['dead'])
                    # unwrap each city
            city_tree = each_province['children']
            for each_city in city_tree:
                city_name = each_city['name']
                if province_name in {'香港', '澳门', '台湾'}:
                    city_name = '%s地区' % province_name
                city_total_data = each_city['total']
                # add the city data to the list
                province.append(province_name)
                city.append(city_name)
                confirmed.append(city_total_data['nowConfirm'])
                accumulate_confirmed.append(city_total_data['confirm'])
                healed.append(city_total_data['heal'])
                dead.append(city_total_data['dead'])
            # reshape to dataframe
        today_data_dict = {'省份': province, '城市/地区': city, '现存确诊': confirmed, '累计确诊': accumulate_confirmed,
                           '治愈': healed, '死亡': dead}
        today_df = pd.DataFrame(today_data_dict)
            # historical data
        history_date = [record['date'] for record in history_data]
        history_confirmed = [record['nowConfirm'] for record in history_data]
        history_accumulate_confirmed = [record['confirm'] for record in history_data]
        history_healed = [record['heal'] for record in history_data]
        history_dead = [record['dead'] for record in history_data]
        history_data_dict = {'日期': history_date, '现存确诊': history_confirmed, '累计确诊': history_accumulate_confirmed,
                             '治愈': history_healed, '死亡': history_dead}
        history_df = pd.DataFrame(history_data_dict)
            # statistical data
        country_confirmed = confirmed[:1]
        country_accumulate_confirmed = accumulate_confirmed[:1]
        country_healed = healed[:1]
        country_dead = dead[:1]
        statistic_data_dict = {'现存确诊': country_confirmed, '累计确诊': country_accumulate_confirmed,
                               '治愈': country_healed, '死亡': country_dead}
        statistic_df = pd.DataFrame(statistic_data_dict)
        # Save data
        today_df.to_csv('中国疫情数据-当日数据.csv', index=False)
        history_df.to_csv('中国疫情数据-历史数据.csv', index=False)
        statistic_df.to_csv('中国疫情数据-国家统计.csv', index=False)
        if server:
            today_df.to_html('%sChina-Detail.html' % self.server_html_path, index=False)
            history_df.to_html('%sChina-History.html' % self.server_html_path, index=False)
            statistic_df.to_html('%sChina-Statistic.html' % self.server_html_path, index=False)
        # Update time store
        self.update_date_store('domestic', today_update_time)
        # Print the data -- for test
        # print(history_data)
        # Return the dataframes
        return statistic_df, history_df, today_df

    def crawl_foreign_epidemic(self, server=True):
        # Get the data
        statistic_data, history_data, today_data = self.crawl_service('foreign')
        countries_data = self.crawl_foreign_service()
        statistic_data = statistic_data['FAutoGlobalStatis']
        history_data = history_data['FAutoCountryMerge']
        # Reshape the received today data into dataframe
        today_update_time = statistic_data['lastUpdateTime']
            # today's data
        today_detail_data = today_data['foreignList']
        continent = []
        nation = []
        city = []
        city_on_map = []
        update_date = []
        confirmed = []
        accumulate_confirmed = []
        healed = []
        dead = []
        for country in today_detail_data:
            country_continent = country['continent']
            country_name = country['name']
            if '日本' in country_name:
                country_name = '日本'
            # Add the country statistical information to the list
            continent.append(country_continent)
            nation.append(country_name)
            city.append(country_name)
            city_on_map.append('')
            update_date.append(country['date'])
            confirmed.append(country['nowConfirm'])
            accumulate_confirmed.append(country['confirm'])
            healed.append(country['heal'])
            dead.append(country['dead'])
            # Unwrap the cities' data
            for each_city in country.get('children', []):
                continent.append(country_continent)
                nation.append(country_name)
                city.append(each_city['name'])
                city_on_map.append(each_city['nameMap'])
                update_date.append(each_city['date'])
                confirmed.append(each_city.get('nowConfirm', '暂缺'))
                accumulate_confirmed.append(each_city['confirm'])
                healed.append(each_city['heal'])
                dead.append(each_city['dead'])
        today_data_dict = {'所属洲': continent, '国家': nation, '城市/地区': city, '地图城市名': city_on_map,
                           '更新日期': update_date, '现存确诊': confirmed, '累计确诊': accumulate_confirmed,
                           '治愈': healed, '死亡': dead}
        today_df = pd.DataFrame(today_data_dict)
            # global history data
        global_daily_history_data = today_data['globalDailyHistory']
        global_date = [record['date'] for record in global_daily_history_data]
        global_history_accumulate_confirmed = [record['all']['confirm'] for record in global_daily_history_data]
        global_history_healed = [record['all']['heal'] for record in global_daily_history_data]
        global_history_dead = [record['all']['dead'] for record in global_daily_history_data]
        global_history_dict = {'日期': global_date, '累计确诊': global_history_accumulate_confirmed,
                               '治愈': global_history_healed, '死亡': global_history_dead}
        global_history_df = pd.DataFrame(global_history_dict)
            # history data of some special countries
        keep_history_countries = ['全球']
        for country, country_data in history_data.items():
            country_date = [record['date'] for record in country_data['list']]
            country_confirmed = [record['confirm'] for record in country_data['list']]
            country_dict = {'日期': country_date, '现存确诊': country_confirmed}
            country_df = pd.DataFrame(country_dict)
            country_df.to_csv('全球疫情数据-【%s】历史数据.csv' % country, index=False)
            if server:
                country_df.to_html('%sGlobal-History-%s.html' % (self.server_html_path, country), index=False)
            keep_history_countries.append(country)
            # global data
        global_confirmed = [statistic_data['nowConfirm'],]
        global_accumulate_confirmed = [statistic_data['confirm'],]
        global_healed = [statistic_data['heal']]
        global_dead = [statistic_data['dead']]
        statistic_data_dict = {'现存确诊': global_confirmed, '累计确诊': global_accumulate_confirmed,
                               '治愈': global_healed, '死亡': global_dead}
        statistic_df = pd.DataFrame(statistic_data_dict)
            # each country's data
        countries_continent = [record['continent'] for record in countries_data]
        countries_name = [record['name'] for record in countries_data]
        countries_name[countries_name.index('日本本土')] = '日本'
        countries_date = [record['date'] for record in countries_data]
        countries_confirmed = [record['nowConfirm'] for record in countries_data]
        countries_accumulate_confirmed = [record['confirm'] for record in countries_data]
        countries_healed = [record['heal'] for record in countries_data]
        countries_dead = [record['dead'] for record in countries_data]
        countries_data_dict = {'所属洲': countries_continent, '国家': countries_name, '更新日期': countries_date,
                               '现存确诊': countries_confirmed, '累计确诊': countries_accumulate_confirmed,
                               '治愈': countries_healed, '死亡': countries_dead}
        countries_df = pd.DataFrame(countries_data_dict)
        # Save data
        today_df.to_csv('全球疫情数据-当日数据.csv', index=False)
        global_history_df.to_csv('全球疫情数据-【全球】历史数据.csv', index=False)
        statistic_df.to_csv('全球疫情数据-全球统计.csv', index=False)
        countries_df.to_csv('全球疫情数据-各国数据.csv', index=False)
        if server:
            today_df.to_html('%sGlobal-Detail.html' % self.server_html_path, index=False)
            global_history_df.to_html('%sGlobal-History.html' % self.server_html_path, index=False)
            statistic_df.to_html('%sGlobal-Statistic.html' % self.server_html_path, index=False)
            countries_df.to_html('%sCountries-Detail.html' % self.server_html_path, index=False)
        # Update time store
        self.update_date_store('foreign', today_update_time)
        # Store the countries that keep history data
        history_country_file = open('具备历史数据的国家.txt', 'wt')
        history_country_file.write(','.join(keep_history_countries))
        history_country_file.close()
        # Print the data -- for test
        #print(today_data)
        # Return the dataframes
        return statistic_df, global_history_df, today_df

    def main(self, server=True):
        self.crawl_domestic_epidemic(server)
        self.crawl_foreign_epidemic(server)


if __name__ == '__main__':
    M = Crawl_Spyder()
    M.main(False)
