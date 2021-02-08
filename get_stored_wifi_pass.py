import subprocess
import re


class WifiFounder:
    def __init__(self):
        self.all_profiles = self.get_all_profiles()
        self.all_profiles_name = self.get_all_profile_names()
        self.list_wifis = []

        self.extract_wifi()

    def get_all_profiles(self):
        return WifiFounder.extract_profiles()

    def get_all_profile_names(self):
        return re.findall("All User Profile     : (.*)\r", self.all_profiles)

    def extract_wifi(self):
        if self.all_profiles_name is not None:
            for profile_found in self.all_profiles_name:
                wifi_details = {}
                wifi_profile = WifiFounder.extract_profiles(profile_found)

                if re.search("Security key           : Absent", wifi_profile):
                    continue
                else:
                    wifi_details['Name of WIFI'] = profile_found
                    wifi_details['Password'] = re.search("Key Content            : (.*)\r", wifi_profile)[1]

                self.list_wifis.append(wifi_details)

    def __repr__(self):
        return f'Your stored Wifi passwords are the followings: \n\n {self.list_wifis}'

    def log_data(self):
        print(self.__repr__())

    @staticmethod
    def extract_profiles(profile_n=None):
        if profile_n is None:
            profiles_list = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True).stdout.decode()
        else:
            profiles_list = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile_n, 'key=clear'], capture_output=True).stdout.decode()
        return profiles_list


init_app = WifiFounder()
init_app.log_data()