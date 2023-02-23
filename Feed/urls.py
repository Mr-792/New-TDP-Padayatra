
from django.contrib import admin
from django.urls import path
from Feed.views import PostsApi, LikesApi, CommentsApi, BookmarksApi, FeedAPI,StoriesAPI,BannersAPI,PollsAPI

urlpatterns = [
    path('upload', PostsApi.as_view({'post':'upload'})),
    path('create-post', PostsApi.as_view({'post':'create'})),
    path('get-post/<int:pk>', PostsApi.as_view({'get':'retrieve'})),
    path('update-post',PostsApi.as_view({'put':'update'})),
    path('publish-post',PostsApi.as_view({'put':'publish'})),
    path('block-post',PostsApi.as_view({'put':'block'})),

    path('delete-post/<int:pk>',PostsApi.as_view({'delete':'destroy'})),
    path('all-posts',PostsApi.as_view({'get':'all_posts'})),
    path('all-posts-with-comments',PostsApi.as_view({'get':'all_posts_with_comments'})),
    path('share-post',PostsApi.as_view({'put':'share'})),
    path('create-like', LikesApi.as_view({'post':'create'})),
    path('delete-like',LikesApi.as_view({'delete':'destroy'})),

    path('create-comment', CommentsApi.as_view({'post':'create'})),
    path('delete-comment',CommentsApi.as_view({'delete':'destroy'})),
    path('block-comment',CommentsApi.as_view({'put':'block'})),

    path('get-comments/<int:pk>',CommentsApi.as_view({'get':'retrieve'})),
    
    path('create-bookmark', BookmarksApi.as_view({'post':'create'})),
    path('delete-bookmark',BookmarksApi.as_view({'delete':'delete'})),
    path('get-bookmarked-posts',BookmarksApi.as_view({'get':'retrieve'})),

    path('userfeed',FeedAPI.as_view({'get':'feed'})),

    path('upload-stories',StoriesAPI.as_view({'post':'upload_stories'})),
    path('upload-stories-thumbnail',StoriesAPI.as_view({'post':'upload_stories_thumbnail'})),
    path('create-stories',StoriesAPI.as_view({'post':'create'})),
    path('get-stories',StoriesAPI.as_view({'get':'retrieve'})),
    path('all-stories',StoriesAPI.as_view({'get':'all_stories'})),
    path('update-stories',StoriesAPI.as_view({'put':'update'})),
    path('delete-stories/<int:pk>',StoriesAPI.as_view({'delete':'destroy'})),
    path('story-by-id/<int:pk>',StoriesAPI.as_view({'get':'story_by_id'})),
    path('publish-stories',StoriesAPI.as_view({'put':'publish'})),

    path('upload-banners',BannersAPI.as_view({'post':'upload_banners'})),
    path('create-banners',BannersAPI.as_view({'post':'create'})),
    path('get-banners',BannersAPI.as_view({'get':'retrieve'})),
    path('all-banners',BannersAPI.as_view({'get':'all_banners'})),
    path('update-banners',BannersAPI.as_view({'put':'update'})),
    path('publish-banners',BannersAPI.as_view({'put':'publish'})),
    path('delete-banners/<int:pk>',BannersAPI.as_view({'delete':'destroy'})),
    path('banner-by-id/<int:pk>',BannersAPI.as_view({'get':'banner_by_id'})),


    path('create-poll',PollsAPI.as_view({'post':'create'})),
    path('get-polls',PollsAPI.as_view({'get':'retrieve'})),
    path('all-polls',PollsAPI.as_view({'get':'all_polls'})),
    path('user-poll',PollsAPI.as_view({'put':'user_poll'})),
    path('publish-poll',PollsAPI.as_view({'put':'publish'})),
    path('update-poll',PollsAPI.as_view({'put':'update'})),
    path('publish-poll',PollsAPI.as_view({'put':'publish'})),
    path('delete-poll/<int:pk>',PollsAPI.as_view({'delete':'destroy'})),

    path('delete-poll/<int:pk>',PollsAPI.as_view({'delete':'destroy'})),
    path('poll-by-id/<int:pk>',PollsAPI.as_view({'get':'poll_by_id'})),
    path('poll-thoughts',PollsAPI.as_view({'post':'poll_thoughts'})),
    path('download-poll-users/<int:pk>', PollsAPI.as_view({'get':'download_poll_users'})),
    path('download-all-thoughts/<int:pk>', PollsAPI.as_view({'get':'download_all_thoughts'})),
    path('recent-thoughts/<int:pk>', PollsAPI.as_view({'get':'recent_thoughts'})),



    ]
