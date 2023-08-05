import re
import requests
import json
from .consts import BASE_POST_URL, BASE_USER_INFO_URL, POST_TYPE_TEXT, POST_TYPE_IMAGE, POST_TYPE_URL, MY_FEED, GROUP_POST, BOTH
from .dicts import linkedin_network_visibility, linkedin_media_category
from pytube import YouTube

class LinkedinAutomate:
    def __init__(self, access_token, description, feed_type, post_media_category, yt_url = None, title = None):
        self.access_token = access_token
        self.yt_url = yt_url
        self.title = title if title or not yt_url else YouTube(yt_url).title
        self.description = description
        # self.python_group_list = [6986570, 13740423, 10309698, 101591, 7018876, 10314051, 25827, 1846027, 10400473, 4388870, 50788, 9247360, 2066905, 12057217, 6626464, 7018767, 6732842, 10318053, 7043467, 3674163, 2688378, 13873590, 3604777, 7041934, 10312814, 4112641, 2101958]
        self.python_group_list = [9247360]
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        self.feed_type = feed_type
        self.post_media_category = post_media_category

    def media_configuration(self):
        if self.post_media_category == POST_TYPE_URL:
            return [
                        {
                            "status": "READY",
                            "description": {
                                "text": self.description
                            },
                            "originalUrl": self.yt_url,
                            "title": {
                                "text": self.title
                            },
                            "thumbnails": [
                                    {
                                    "url": self.extract_thumbnail_url_from_YT_video_url()
                                    }
                                ]
                        }
                    ]


    def common_api_call_part(self, linkedin_feed_type, group_id = None):
        payload_dict = {
            "author": f"urn:li:person:{self.user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": self.description
                    },
                    "shareMediaCategory": linkedin_media_category[self.post_media_category]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": linkedin_feed_type
            }
        }
        if linkedin_feed_type == linkedin_network_visibility[GROUP_POST] and group_id:
            payload_dict["containerEntity"] = f"urn:li:group:{group_id}"

        if self.post_media_category != POST_TYPE_TEXT:
            payload_dict["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = self.media_configuration()
            
        return json.dumps(payload_dict)

    def extract_thumbnail_url_from_YT_video_url(self):
        exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
        s = re.findall(exp,self.yt_url)[0][-1]
        return  f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"

    def get_user_id(self):
        url = BASE_USER_INFO_URL
        response = requests.request("GET", url, headers=self.headers)
        print(response.text)
        jsonData = json.loads(response.text)
        return jsonData["id"]
    
    def feed_post(self):
        url = BASE_POST_URL
        payload = self.common_api_call_part(linkedin_feed_type=linkedin_network_visibility[MY_FEED])
        return requests.request("POST", url, headers=self.headers, data=payload)
    
    def group_post(self, group_id):
        url = BASE_POST_URL
        payload = self.common_api_call_part(linkedin_feed_type=linkedin_network_visibility[GROUP_POST], group_id=group_id)
        return requests.request("POST", url, headers=self.headers, data=payload)


    def main_func(self):
        self.user_id = self.get_user_id()
        # print(self.user_id)

        if self.feed_type in [MY_FEED, BOTH]:
            return self.feed_post()
        
        if self.feed_type in [GROUP_POST, BOTH]:
            for group_id in self.python_group_list:
                print(group_id)
                group_post = self.group_post(group_id)
                print(group_post)
            return group_post
# https://www.linkedin.com/feed/update/urn:li:activity:7090393356886827009/


# https://www.linkedin.com/feed/update/urn:li:activity:7090396536899026945
# https://www.linkedin.com/feed/update/urn:li:activity:7090396534940311552
# group_post.headers.get("x-linkedin-id")


