from pytube import YouTube, Search
import re
from colorama import Style, Fore
from datetime import timedelta
from pytube.cli import on_progress


class YouTubeDownloader(YouTube):
    
    def __init__(self,search):
        self.youtube_link_pattern = re.compile(r"^https\:\/\/www\.youtube\.com\/watch\?v|^https\://you\.be\/")
        self.search = search
        
        if re.match(self.youtube_link_pattern, search):
            self.is_link = True
            self.YT = YouTube(url=search, on_progress_callback=on_progress)
            
        else:
            self.is_link = False

    # This returns all the videos from the user query
    def fetch_videos_from_search(self):
        return Search(search).results

            
    # This returns all available resolutions
    def fetch_available_resolutions(self):
        streams = self.YT.streams.filter(progressive=True)
        resolutions = set()
        for stream in streams:
            if stream.resolution != None:
                resolutions.add(int(stream.resolution.strip("p")))
            
        return {"resolutions": resolutions}


    def download_video(self, resolution):
        streams = self.YT.streams.filter(res=f"{resolution}p", progressive=True)
        stream = streams[0]
        stream.download(filename=f"{self.YT.title}.mp4")

    def download_mp3(self):
        highest_abr = 0
        available_streams = self.YT.streams.filter(only_audio=True)
        for stream in available_streams:
            abr = int(stream.abr.strip("kbps"))
            if highest_abr < abr:
                highest_abr = abr
        highest_quality = available_streams.filter(abr=f"{highest_abr}kbps").first()
        highest_quality.download(filename=f"{self.YT.title}.mp3")
        
        
def choose_resolution():
    global chosen_resolution
    
    res = []
    available_resolutions = yt.fetch_available_resolutions()['resolutions']
    print("All available resolutions: ")
    for i in available_resolutions:
        res.append(i)
    print(sorted(res))
    while True:
        try:
            chosen_resolution = int(input("Select resolution "))
            if chosen_resolution not in res:
                continue
            break
        except:
            continue

        
if __name__ == "__main__":
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    RESET = Style.RESET_ALL
    
    while True:
        search = input(CYAN+"Input URL or search for video: "+RESET)
        yt = YouTubeDownloader(search=search)
        print("Would you like to convert to MP3 or MP4?")
        print(RED+"1. MP3")
        print("2. MP4"+RESET)
        while True:
            try:
                mode = int(input("Input: "))
                if mode not in [1,2]:
                    continue
                break
            except:
                print(RED+"\nWrong input. Type in 1 or 2\n"+RESET)
                continue
            
            
        if not yt.is_link:
            suggestions = yt.fetch_videos_from_search()
            for index, video in enumerate(suggestions):
                print(GREEN+f"{index}:{RESET} {video.title}{YELLOW} BY: {video.author} {RED}LENGTH: {timedelta(seconds=video.length)}"+RESET)
            
            choose_from_suggestion = suggestions[int(input(GREEN+"\nChoose from suggestions list: "+RESET))]
            yt = YouTubeDownloader(search=f"https://www.youtube.com/watch?v={choose_from_suggestion.video_id}")
            if mode == 2:
                choose_resolution()
                print(GREEN+"DOWNLOADING VIDEO"+RESET)
                yt.download_video(chosen_resolution)
            elif mode == 1:
                print(GREEN+"DOWNLOADING MP3"+RESET)                
                yt.download_mp3()
        
        elif yt.is_link:
            if mode == 2:
                choose_resolution()
                print(GREEN+"DOWNLOADING VIDEO"+RESET)
                yt.download_video(chosen_resolution)
            elif mode == 1:
                print(GREEN+"DOWNLOADING MP3"+RESET)
                yt.download_mp3()