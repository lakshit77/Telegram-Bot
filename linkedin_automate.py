import os
from linkedin_automate_folder.linkedin_file import LinkedinAutomate
from linkedin_automate_folder.consts import POST_TYPE_TEXT, POST_TYPE_URL, GROUP_POST, MY_FEED, BOTH
from pytube import YouTube

access_token = os.environ.get("LINKEDIN_ACCESS_KEY")
yt_url = "https://www.youtube.com/watch?v=MO0WRRkdK5c&ab_channel=TechSunami"
title = "PYDANTIC - Most Popular Python DATA VALIDATION Library | Pydantic VALIDATOR"
# description = video._vid_info['videoDetails']['shortDescription']

description = """Pydantic is downloaded over 70M times/month and is used by all FAANG companies and 20 of the 25 largest companies on NASDAQ

Pydantic, a powerful Python library, provides seamless data validation with its Pydantic data validation and Pydantic validator capabilities. 

By ensuring data integrity and type safety, it enhances code reliability. Empower your projects with Pydantic's effortless integration and extensive support for complex data structures, saving you time and boosting productivity. 

Simplify your data validation process and improve your Python applications with Pydantic's user-friendly features and robust functionality.

#techsunami #developer #pydantic 
"""

video = YouTube(yt_url)
print(video)
# feed_type = MY_FEED
# post_media_category = POST_TYPE_URL
# print(LinkedinAutomate(access_token, description, feed_type, post_media_category, yt_url, title).main_func())