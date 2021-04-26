from selenium import webdriver
import os


def capability_select(device_os, download_dir):
    capability = None
    if device_os == 'web':
        capability = webdriver.ChromeOptions()
        capability.add_experimental_option("excludeSwitches", ["enable-logging"])
        capability.add_experimental_option("prefs", {"download.default_directory": download_dir})
    elif device_os == 'mw':
        mobile_emulation = {"deviceName": "Pixel 2"}
        capability = webdriver.ChromeOptions()
        capability.add_experimental_option("mobileEmulation", mobile_emulation)
        capability.add_experimental_option("excludeSwitches", ["enable-logging"])
    elif device_os == 'android':
        capability = {"platformName": "Android",
                      "platformVersion": "8.1",
                      "automationName": "Appium",
                      "appPackage": "ru.mail.search.electroscope",
                      "appActivity": ".ui.activity.AssistantActivity",
                      "app": os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                          '../stuff/Marussia_v1.39.1.apk')
                                             ),
                      "autoGrantPermissions": "true",
                      "orientation": "PORTRAIT"
                      }
    else:
        raise ValueError("Incorrect device os type")
    return capability
