# YouTube Video Statistics

## Main features
Downloading an Excel file that contains data of videos in a given channel.

## Demo Video
Feel free to watch a [short video demo](https://www.youtube.com/watch?v=Pjt7Y3sG118&list=PLNiyoHci9a3Qien3F-WK6qD28biOy9ltE) or a [long video demo](https://www.youtube.com/watch?v=155YRdtva5k&list=PLNiyoHci9a3Qien3F-WK6qD28biOy9ltE).

[![enter image description here](https://github.com/DannyIbo/youtube-video-statistics/raw/presentation/screenshots/2019125-102127.jpg)](https://www.youtube.com/watch?v=Pjt7Y3sG118&list=PLNiyoHci9a3Qien3F-WK6qD28biOy9ltE)

## Description
This is a command line tool gets data from a given channel and returns an Excel file. It takes the channel ID as input that can be extracted from the URL in the browser. Data contains videos, views, likes, comments and much more. The script is written in pyhton 3 and uses pandas to extract and transform the data.

## Returned Data Attributes
After downloading the Excel file you will find it in the output folder: `output/`

Have a look at the [example output .xlsx file](https://github.com/DannyIbo/youtube-video-statistics/raw/master/output/EXAMPLE_youtube-video-statistics_channel_Id_UCV9pZxcKWF6fZ1ZQzDWofgw.xlsx).

The output Excel contains values for the following attributes/columns:

 1. videoId  
 2. publishedAt  
 3. channelId  
 4. title
 5. description
 6. channelTitle
 7. tags  
 8. categoryId  
 9. category  
 10. liveBroadcastContent  
 11. duration
 12. duration_sec  
 13. dimension  
 14. definition  
 15. caption  
 16. licensedContent
 17. projection
 18. privacyStatus  
 19. license  
 20. embeddable  
 21. publicStatsViewable
 22. viewCount  
 23. likeCount  
 24. dislikeCount  
 25. favoriteCount  
 26. commentCount
 27. thumbnails_default

## Requirements
- You need a YouTube Data API to make this work. I do not publish mine here. Get your own for free at [https://console.developers.google.com/](https://console.developers.google.com/)
- Please check further requirements in the `requirements.txt`

## Hidden Features
This script uses a module that I used for some other YouTube Data Analytics Tools. By far not every function in this module is used in this project so you can explore the functions that will also allow to return YouTube Search Results and comments on videos.
Explore the module and have a closer look at `src/youtube_data_module.py`

## To Dos

 1. As some users are may not familiar on how to extract a channel ID from the URL in the browser, it might be a good idea to take as input any URL that somehow connects to a channel. This could be an URL of a specific video in this channel such as [`https://www.youtube.com/watch?v=Pjt7Y3sG118`](https://www.youtube.com/watch?v=Pjt7Y3sG118), a URL of a playlist that belongs to that channel like [`https://www.youtube.com/playlist?list=PLNiyoHci9a3Qien3F-WK6qD28biOy9ltE`](https://www.youtube.com/playlist?list=PLNiyoHci9a3Qien3F-WK6qD28biOy9ltE) or a URL with a personalized URL like [`https://www.youtube.com/user/schafer5`](https://www.youtube.com/user/schafer5)
 2. :boom: :boom::boom:Last but not least: A bowser-based online deployment would be nice :boom::boom::boom:
