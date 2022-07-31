def get_channels_data(youtube, channelsIDs):
    
    """
    Get general data of a list of channels
    Args:
        youtube: 
        channelsIDs: list of channel IDS
    
    return:
        Dataframe contains channel name, Total subscribes, Total views, Total videos, playlist ID
    
    """
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channelsIDs)
    )
    alldata = []
    response = request.execute()
    for item in response["items"]:
        data = {"channelName": item["snippet"]["title"],
                "subscibes": item["statistics"]["subscriberCount"],
                "views": item["statistics"]["viewCount"],
                "total_Videos": item["statistics"]["videoCount"],
                "playlist_ID": item["contentDetails"]["relatedPlaylists"]["uploads"]
               }
        alldata.append(data)
    
    return pd.DataFrame(alldata)

def get_videosIDs(youtube, playlistid):
    
    """
    Get videos IDs based on plalist id of a specific channel
    Args:
        youtube: 
        playlistid: "string" Id of the plalist
    
    return:
        list of string "videos ID"
    
    """
    
    data = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails,id,status",
        maxResults=50,
        playlistId=playlistid
    )
    response = request.execute()
    
    for item in response["items"]:
        data.append(item["contentDetails"]["videoId"])
    
    next_p = response.get("nextPageToken")

    while next_p is not None:

        request = youtube.playlistItems().list(
            part="snippet,contentDetails,id,status",
            maxResults=50,
            pageToken=next_p,
            playlistId=playlistid
        )
        response = request.execute()
        
        for item in response["items"]:
            data.append(item["contentDetails"]["videoId"])
        
        next_p = response.get("nextPageToken")
    
    return data

def get_videos_data(youtube, plid):
    
    """
    Get videos data based on plalist id of a specific channel
    Args:
        youtube: 
        playlistid: "string" Id of the plalist
    
    return:
        list of dictionnary of videos data
    
    """
    
    data = {}
    all_data = []
    videos = get_videosIDs(youtube, plid)

    for i in range(0,len(videos),50):
        request = youtube.videos().list(part="snippet,contentDetails,statistics",
                                        id=",".join(videos[i:i+50])
                                       )

        response = request.execute()
        for item in response["items"]:
            try:
                all_data.append([item["snippet"]["channelTitle"],
                                 item["snippet"]["publishedAt"],
                                 item["snippet"]["title"],
                                 item["snippet"]["tags"],
                                 item["contentDetails"]["duration"],
                                 item["statistics"]
                                ])
            except:
                all_data.append([item["snippet"]["channelTitle"],
                                 item["snippet"]["publishedAt"],
                                 item["snippet"]["title"],
                                 [],
                                 item["contentDetails"]["duration"],
                                 item["statistics"]
                                ])
       
    return all_data

def transform_to(data):
    
    """
    Transform videos data into dataframe
    Args:
        data: list of dictionnary of videos data
    
    return:
        dataframe
    
    """
    
    l_stat = []
    s = {}
    for d in data:
        s["channelTitle"] = d[0]
        s["publishedAt"] = d[1]
        s["title"] = d[2]
        s["tags"] = d[3]
        s["duration"] = d[4]
        s["viewCount"] = "N.A"
        s["likeCount"] = "N.A"
        s["favoriteCount"] = "N.A"
        s["commentCount"] = "N.A"
        stat = d[5]
        for keyy, val in stat.items():
            s[keyy] = val
        
        l_stat.append(s.copy())
   
    return pd.DataFrame(l_stat)

