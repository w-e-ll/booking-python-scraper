import os
import json
import socket
import time
import random
from chrome_useragents import chrome
from pprint import pprint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# timeout in seconds
timeout = 60
socket.setdefaulttimeout(timeout)
headers = {}
headers['User-Agent'] = random.choice(chrome)


class BookingScraper:
    """Booking.com spyder that scrapes \
       data for hotel room facilities and hotel nearby usefull locations. \
       Loads hotel names and ids from tb_hotels.json. \
       After all content preparations completed, script dumps data to json file.
    """
    def __init__(self, *args, **kwargs):
        self.chrome_path = os.path.abspath(os.path.curdir) + '/chromedriver'
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(
            executable_path=f"{self.chrome_path}",
            options=self.options)
        self.options.add_argument("--disable-javascript")
        self.options.add_argument("--disable-bundled-ppapi-flash")
        self.options.add_argument("--disable-plugins-discovery")
        self.options.add_argument('--disable-web-security')
        self.options.add_argument('--disable-webrtc-multiple-routes')
        self.options.add_argument('--disable-webrtc-hw-encoding')
        self.options.add_argument('--disable-webrtc-hw-decoding')
        self.options.add_argument('--disable-webrtc-encryption')
        self.driver.implicitly_wait(1)
        super(BookingScraper, self).__init__(*args, **kwargs)

    def load_hotels(self):
        """Loads hotel names and ids from tb_hotels.json"""
        hotels = json.load(open('tb_hotels.json', 'r'))
        return hotels

    def get_query(self, hotel):
        """Prepare google queries using hotel name as row data"""
        query = hotel['name'].replace("ú", "%FA").replace("\xc8", "%C8").replace("\xe0", "%E0").replace("\xdc", "%DC").replace(
            "\xf3", "%F3").replace("\xfa", "%5Cxfa").replace("\xdf", "%DF").replace("\xd6", "%D6").replace("\xe8", "%E8").replace(
            "\u2122", "%u2122").replace("\u2013", "%5Cu2013").replace("\xf4", "%F4").replace("\xc4", "%C4").replace("\xe2", "%E2").replace(
            "\xe4", "%E4").replace("\xfc", "%FC").replace("\xe9", "%E9").replace("\xf6", "%F6").replace(" ", "%20").replace(
            "&", "%26").replace("'", "%27").replace("*", "%2A").replace("|", "%7C").replace("\'n", "%5C%27n").replace(
            "\'", "%5C%27").replace("/", "%2F").replace(" ", "%2B")
        return query

    def get_hotel_name(self, hotel):
        """Prepare hotel name, replace all bad simbols"""
        name = hotel['name'].replace("%C8", "\xc8").replace("%E0", "\xe0").replace("%DC", "\xdc").replace(
            "%F3", "\xf3").replace("%5Cxfa", "\xfa").replace("%DF", "\xdf").replace("%D6", "\xd6").replace("%E8", "\xe8").replace(
            "%u2122", "\u2122").replace("%5Cu2013", "\u2013").replace("%F4", "\xf4").replace("%C4", "\xc4").replace("%E2", "\xe2").replace(
            "%E4", "\xe4").replace("%FC", "\xfc").replace("%E9", "\xe9").replace("%F6", "\xf6").replace("%20", " ").replace(
            "%26", "&").replace("%27", "'").replace("%2A", "*").replace("%7C", "|").replace("%5C%27n", "\'n").replace(
            "%5C%27", "\'").replace("%2F", "/").replace("%2B", " ")
        return name

    def get_to_booking(self):
        """Get to Booking.com start page too start scraping"""
        url = 'https://www.booking.com/index.en-gb.html'
        self.driver.get(url)

    def search_for_hotel(self, hotel_name):
        """Let's start to search for needed hotel"""
        input_button = self.driver.find_element_by_name('ss')
        input_button.click()
        input_button.send_keys(f"{hotel_name}")
        search_button = self.driver.find_element_by_class_name('sb-searchbox__button  ')
        search_button.click()

    def get_from_center_element(self):
        """Try to get obj from center element_by_class_name"""
        try:
            center_obj = self.driver.find_element_by_class_name('distfromdest').text
            return center_obj
        except NoSuchElementException as err:
            print("{}".format(err))
            return None

    def get_to_hotel(self):
        """Get link to required hotel"""
        to_hotel = self.driver.find_element_by_class_name('hotel_name_link').get_attribute('href')
        self.driver.get(to_hotel)

    def get_room_type_buttons(self):
        """Get room type buttons"""
        room_type_buttons = self.driver.find_elements_by_class_name('jqrt')
        return room_type_buttons

    def click_close(self):
        """Click on calendar close button"""
        self.driver.find_element_by_class_name('c2-calendar-close-button').click()

    def click_close2(self):
        """Click on calendar close button"""
        self.driver.find_element_by_class_name('c2-calendar-close-button-icon').click()

    def click_close1(self):
        """Click on close button"""
        self.driver.find_element_by_class_name('et-survey__closeBtn').click()

    def get_facility_obj(self, src):
        """Get facility obj"""
        facility_obj = self.driver.find_element_by_xpath(f'//*[@id="blocktoggle{src}"]').text
        return facility_obj

    def room_type_close_button(self):
        """Click on a lightbox close button"""
        self.driver.find_element_by_class_name('lightbox_close_button').click()

    def get_breakfast_info(self):
        """Getting breakfast info"""
        try:
            breakfast_info = self.driver.find_element_by_xpath('//*[@class="ph-item-copy-breakfast-option"]').text
            return breakfast_info
        except NoSuchElementException as err:
            print("{}".format(err))

    def nearby(self):
        """Getting nearby_objs, working on them"""
        try:
            nearby_objs = self.driver.find_elements_by_class_name('location_block__content_block')
            nearbyes = [obj.text for obj in nearby_objs]
            print(nearbyes)
        except NoSuchElementException as err:
            print("{}".format(err))
            nearby_objs = self.driver.find_element_by_class_name('hp-poi-content-container--column').text
            nearbyes = nearby_objs
        try:
            if 'What Travelers Love' in nearbyes[-1]:
                del nearbyes[-1]
            if 'What travellers love' in nearbyes[-1]:
                del nearbyes[-1]
        except IndexError as err:
            print(f"ERR: {err}")
            pass

        nearb = []
        two_column_objs = ['Closest Landmarks', 'Closest landmarks', 'Most popular landmarks',
                           'Most Popular Landmarks', 'Closest airports', 'Closest Airports',
                           'Restaurants and markets', 'Restaurants & Markets']
        three_column_objs = ['Natural Beauty', 'Natural beauty']

        for nearby in nearbyes:
            new = nearby.split("\n")
            print(new)
            nearby_name = new[0]
            if nearby_name:
                del new[0]
                if nearby_name in two_column_objs:
                    print(new)
                    names = new[::2]
                    longs = new[1::2]
                    h_nearby = list(zip(names, longs))
                    hotel_nearby = {nearby_name: h_nearby}
                    nearb.append(hotel_nearby)
                if nearby_name in three_column_objs:
                    names = new[::3]
                    types = new[1::3]
                    longs = new[2::3]
                    h_nearby = list(zip(names, types, longs))
                    hotel_nearby = {nearby_name: h_nearby}
                    nearb.append(hotel_nearby)
        return nearb

    def old_nearby(self):
        """Getting old nearby objs (old Booking ver.), working on them if it exists"""
        try:
            nearby_objs = self.driver.find_elements_by_xpath(
                '//*[contains(@class, "hp-poi-content-container hp-poi-content-container--column clearfix")]/div')
            nearbyes = [i.text for i in nearby_objs]
            print(nearbyes)
        except NoSuchElementException as err:
            print("{}".format(err))
            pass
        try:
            if 'What Travelers Love' in nearbyes[-1]:
                del nearbyes[-1]
            if 'What travellers love' in nearbyes[-1]:
                del nearbyes[-1]
        except IndexError as err:
            print(f"ERR: {err}")
            pass
        nearb = []
        two_column_objs = ['Closest Landmarks', 'Closest landmarks', 'Most popular landmarks',
                           'Most Popular Landmarks', 'Closest airports', 'Closest Airports',
                           'Restaurants and markets', 'Restaurants & Markets']
        three_column_objs = ['Natural Beauty', 'Natural beauty']

        for nearby in nearbyes:
            new = nearby.split("\n")
            nearby_name = new[0]
            if nearby_name:
                del new[0]
                if nearby_name in two_column_objs:
                    names = new[::2]
                    longs = new[1::2]
                    h_nearby = list(zip(names, longs))
                    hotel_nearby = {nearby_name: h_nearby}
                    nearb.append(hotel_nearby)
                if nearby_name in three_column_objs:
                    names = new[::3]
                    types = new[1::3]
                    longs = new[2::3]
                    h_nearby = list(zip(names, types, longs))
                    hotel_nearby = {nearby_name: h_nearby}
                    nearb.append(hotel_nearby)
        return nearb

    def facility_preparation(self, f):
        """Preparing hotel room facilities"""
        newf = f.split("\n")
        facility_obj_name = newf[0]
        if facility_obj_name:
            del newf[0]
            h_facility_obj = {facility_obj_name: tuple(newf)}
        return h_facility_obj

    def get_facilities(self):
        """getting hotel room facilities"""
        facility_objs = self.driver.find_elements_by_class_name('facilitiesChecklistSection')
        facilities_lists = [obj.text for obj in facility_objs]
        return facilities_lists

    def b_facilities(self, facilities_lists):
        """Working on room facilities"""
        b_facilities = []
        for f in facilities_lists:
            if 'General' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Health & Wellness Facilities' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Wellness facilities' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Pool and Spa' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Pool and wellness' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Front Desk Services' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Services' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Reception services' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            elif 'Food & Drink' in f:
                h_facility_obj = self.facility_preparation(f)
                b_facilities.append(h_facility_obj)
            else:
                pass
        return b_facilities

    def find_restaurants(self):
        """Getting restaurant objects"""
        rest_objs = self.driver.find_elements_by_class_name('restaurant-block')
        rest_lists = [obj.text for obj in rest_objs]
        return rest_lists

    def restaurant_preparation(self, r):
        """Preparing restaurant objects"""
        newr = r.split("\n")
        restaurant_obj_name = newr[0]
        if restaurant_obj_name:
            del newr[0]
            h_restaurant_obj = {restaurant_obj_name: tuple(newr)}
        return h_restaurant_obj


if __name__ == "__main__":
    bs = BookingScraper()
    hotels = bs.load_hotels()
    print(hotels)
    with open('additional_data.json', 'w', encoding='utf-8') as file:
        outer_list = []
        for hotel in hotels:
            data = {}
            data['UNID'] = str(hotel['unid'])
            print(f"UNID: {data['UNID']}")
            print()
            data['NAME'] = bs.get_hotel_name(hotel)
            print(f"NAME: {data['NAME']}")
            print()
            bs.get_to_booking()
            hotel_name = hotel['name']
            bs.search_for_hotel(hotel_name)
            try:
                bs.click_close()
                bs.click_close1()
                bs.click_close2()
            except NoSuchElementException:
                pass
            len_from_center = bs.get_from_center_element()
            data['LEN_FROM_CENTER'] = len_from_center
            print(f"LEN_FROM_CENTER: {data['LEN_FROM_CENTER']}")
            print()
            bs.get_to_hotel()
            data['BREAKFAST_INFO'] = bs.get_breakfast_info()
            pprint(f"BREAKFAST_INFO: {data['BREAKFAST_INFO']}")
            print()
            room_type_buttons = bs.get_room_type_buttons()
            room_type_names = [obj.get_attribute('data-room-name-en') for obj in room_type_buttons]
            room_type_hrefs = [obj.get_attribute('href') for obj in room_type_buttons]
            print(f"For this hotel here we have {len(room_type_buttons)} room type buttons")
            data["ROOM_TYPE_QUANTITY"] = len(room_type_buttons)
            room_types = []
            for button, name, href in tuple(zip(room_type_buttons, room_type_names, room_type_hrefs)):
                button.click()
                ref = href.split("1&#")
                src = ref[-1]
                print(src)
                facility_obj = bs.get_facility_obj(src)
                x = facility_obj.split("\nRoom facilities:\n")
                y = x[-1]
                z = y.split("\nMissing some information?\n")
                facilities_objs = z[0]
                facilities_row = facilities_objs.split("\n")
                facilities = [obj.replace("• ", "") for obj in facilities_row]
                room_type = name
                room_data = (room_type, facilities)
                room_types.append(room_data)
                bs.room_type_close_button()
            data['ROOM_TYPES'] = room_types
            pprint(f"ROOM_TYPES: {data['ROOM_TYPES']}")
            print()
            nearby_objs = bs.nearby()
            if not nearby_objs:
                nearby_objs = bs.old_nearby()
            data['NEARBY'] = nearby_objs
            pprint(f"NEARBY: {data['NEARBY']}")
            print()
            facilities_lists = bs.get_facilities()
            b_facilities = bs.b_facilities(facilities_lists)
            data['FACILITIES'] = b_facilities
            pprint(f"FACILITIES: {data['FACILITIES']}")
            print()
            rest_lists = bs.find_restaurants()
            b_restaurants = []
            for r in rest_lists:
                h_restaurant_obj = bs.restaurant_preparation(r)
                b_restaurants.append(h_restaurant_obj)
            data['RESTAURANTS'] = b_restaurants
            pprint(f"RESTAURANTS: {data['RESTAURANTS']}")
            if data not in outer_list:
                outer_list.append(data)

        json.dump(outer_list, file, sort_keys=True, indent=4, ensure_ascii=False)
