from .consts import POST_TYPE_TEXT, POST_TYPE_URL, POST_TYPE_IMAGE, MY_FEED, GROUP_POST

linkedin_media_category = {
    POST_TYPE_TEXT: "NONE",
    POST_TYPE_URL: "ARTICLE",
    POST_TYPE_IMAGE: "IMAGE" #Currently Not supported
}


linkedin_network_visibility = {
    MY_FEED: "PUBLIC",
    GROUP_POST: "CONTAINER"
}