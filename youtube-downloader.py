from pytube import YouTube, Search
import re
from colorama import Style, Fore
from datetime import timedelta
from pytube.cli import on_progress
import os

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
        return Search(self.search).results

            
    # This returns all available resolutions
    def fetch_available_resolutions(self):
        streams = self.YT.streams.filter(progressive=True)
        resolutions = set()
        for stream in streams:
            if stream.resolution != None:
                resolutions.add(int(stream.resolution.strip("p")))
            
        return sorted([i for i in resolutions])


    def download_video(self, resolution):
        streams = self.YT.streams.filter(res=f"{resolution}p", progressive=True)
        stream = streams[0]
        stream.download(output_path=f"{os.getcwd()}/downloaded_videos/", filename=f"{self.YT.title}.mp4")

    def download_mp3(self):
        highest_abr = 0
        available_streams = self.YT.streams.filter(only_audio=True)
        for stream in available_streams:
            abr = int(stream.abr.strip("kbps"))
            if highest_abr < abr:
                highest_abr = abr
        highest_quality = available_streams.filter(abr=f"{highest_abr}kbps").first()
        highest_quality.download(output_path=f"{os.getcwd()}/downloaded_songs/", filename=f"{self.YT.title.replace('.', '-')}.mp3")
        
class GUI:
          
    def inputURL_page(self):
        global search_query, yt
        search_query = input("Insert URL or search query here: ")
        yt = YouTubeDownloader(search=search_query)
        return self.askmode_page()
            
    def askmode_page(self):
        global mode
        print("What would you like to convert the video to?")
        print("1. MP3")
        print("2. MP4")
        mode = input("\nChoice: ")
        if yt.is_link:
            return self.display_information(yt.YT)
        return self.display_suggestions()
        
    def display_suggestions(self):
        suggestions = yt.fetch_videos_from_search()
        for index, suggestion in enumerate(suggestions):
            print(f"{index}: {suggestion.title} BY: {suggestion.author}")
        while True:
            try:
                choose_video = int(input("Input the index of your choice video: "))
                if choose_video < 0 or choose_video > len(suggestions):
                    continue
                else:
                    break
            except:
                continue
        chosen_video = suggestions[choose_video]
        return self.display_information(chosen_video)

    def display_information(self, video):
        global yt, is_mp3
        print("These are the following video details:")
        print(f"Title: {video.title}")
        print(f"Author: {video.author}")
        print(f"Views: {video.views}")
        print(f"Length: {timedelta(seconds=video.length)}")
        print(f"Publish date: {video.publish_date}")
        
        print("What would you like to do?")
        print("1. Continue to download")
        print("2. Go back")
        while True:
            choice = int(input("Choice: "))

            if choice == 1:
                #redeclare yt downloader object with valid url
                yt = YouTubeDownloader(search=f"https://www.youtube.com/watch?v={video.video_id}")
                if mode == 2:
                    is_mp3 = False
                    return self.choose_resolution()
                else:
                    print("Starting download for {}".format(video.title))
                    is_mp3 = True
                    return self.download_page()
            elif choice == 2:
                return self.display_suggestions()
            else:
                continue
            continue
            
    def choose_resolution(self):
        print("Available resolutions for download: ")
        resolutions = yt.fetch_available_resolutions()
        chosen_resolution = int(input("Choose your resolution: "))
        print("Starting download for {}".format(yt.YT.title))
        return self.download_page(chosen_resolution)
        
    def download_page(self, resolution=None):
        if is_mp3:
            input("MP3 file is ready to be downloaded. Press Enter to start.")
            yt.download_mp3()
        elif not is_mp3:
            input("MP4 file is ready to be downloaded. Press Enter to start.")
            yt.download_video(resolution)
        
        



if __name__ == "__main__":
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    RESET = Style.RESET_ALL
    gui = GUI()
    gui.inputURL_page()
    
    
    
    
    
    
"""  while True:
        search = input(CYAN+"\n\nInput URL or search for video: "+RESET)
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
                print(GREEN+f"{index}:{RESET} {video.title}{YELLOW} BY: {video.author}"+RESET)
            
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
                yt.download_mp3()"""