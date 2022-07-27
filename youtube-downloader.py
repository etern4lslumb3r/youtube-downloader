from pytube import YouTube, Search
import re
from colorama import Style, Fore
import colorama 
from datetime import timedelta
from pytube.cli import on_progress
import os
import os.path
from pathlib import Path


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
        stream.download(output_path=f"{os.getcwd()}/downloaded_videos/", filename=f"{self.YT.title.replace('.', '-').replace('/','_').replace('|','')}.mp4")

    def download_mp3(self):
        highest_abr = 0
        available_streams = self.YT.streams.filter(only_audio=True)
        for stream in available_streams:
            abr = int(stream.abr.strip("kbps"))
            if highest_abr < abr:
                highest_abr = abr
        highest_quality = available_streams.filter(abr=f"{highest_abr}kbps").first()
        highest_quality.download(output_path=f"{os.getcwd()}/downloaded_songs/", filename=f"{self.YT.title.replace('.', '-').replace('/','_').replace('|','')}.mp3")
   
        
class GUI:
    def __init__(self):
        self.RED = Fore.RED
        self.YELLOW = Fore.YELLOW
        self.CYAN = Fore.CYAN
        self.GREEN = Fore.GREEN
        self.RESET = Style.RESET_ALL
    
    def init_dirs(self):
        curr_dir = os.getcwd()
        
        if not os.path.exists(curr_dir+"/downloaded_songs/"):
            mp3_path = Path(curr_dir+"/downloaded_songs/.readme.txt")
            mp3_path.parent.mkdir(exist_ok=True, parents=True)
            mp3_path.write_text("This is where downloaded songs are stored")
        
        if not os.path.exists(curr_dir+"/downloaded_videos/"):
            mp4_path = Path(curr_dir+"/downloaded_videos/.readme.txt")
            mp4_path.parent.mkdir(exist_ok=True, parents=True)
            mp4_path.write_text("This is where downloaded videos are stored.")
        
        
    def separate_conversions(self, separation_amount:int):
        print("\n"*separation_amount)
    
    def separate_prompts(self):
        print(f"{self.GREEN}-----------------------------------------------------------------------------\n{self.RESET}")
        
        
    def start(self):
        return self.inputURL_page()
    
    
    def inputURL_page(self):
        global search_query, yt
        search_query = input(self.CYAN+"Insert URL or search query here: "+self.RESET)
        if re.match(r' +', search_query) or len(search_query) == 0:
            self.inputURL_page()
        yt = YouTubeDownloader(search=search_query)
        self.separate_prompts()
        return self.askmode_page()
            
    def askmode_page(self):
        global mode, is_mp3
        print(self.CYAN+ "\nWhat would you like to convert the video to?\n")
        print(self.YELLOW+"1. MP3")
        print("2. MP4")
        print(self.RED+"3. Back" +self.RESET)
        while True:
            try:
                mode = int(input(self.YELLOW+"\n\nChoice: "+self.RESET))
                if mode not in [1,2,3]:
                    continue
                elif mode == 1:
                    is_mp3 = True
                elif mode == 2:
                    is_mp3 = False
                elif mode == 3:
                    self.separate_prompts()
                    return self.inputURL_page()
                break
            except:
                continue
        if yt.is_link:
            self.separate_prompts()
            return self.display_information(yt.YT)
        self.separate_prompts()
        return self.display_suggestions()
        
    def display_suggestions(self):
        suggestions = yt.fetch_videos_from_search()
        for index, suggestion in enumerate(suggestions):
            print(f"{self.YELLOW}{index}{self.RESET}: {self.CYAN}{suggestion.title}{self.RESET} {self.RED}BY:{suggestion.author}{self.RESET}")
        print(f"{self.YELLOW}{len(suggestions)}: {self.RED}Go back{self.RESET}")
        while True:
            try:
                choose_video = int(input("\nInput the index of your choice video: "))
                if choose_video < 0 or choose_video > len(suggestions)+1:
                    continue
                if choose_video == len(suggestions):
                    self.separate_prompts()
                    return self.askmode_page()
                else:
                    break
            except:
                continue
        chosen_video = suggestions[choose_video]
        self.separate_prompts()
        return self.display_information(chosen_video)

    def display_information(self, video):
        global yt, is_mp3
        print(f"{self.YELLOW}\nVideo details:\n")
        print(f"{self.YELLOW}Title:{self.RESET} {video.title}")
        print(f"{self.YELLOW}Author:{self.RESET} {video.author}")
        print(f"{self.YELLOW}Views:{self.RESET} {video.views}")
        print(f"{self.YELLOW}Length:{self.RESET} {timedelta(seconds=video.length)}")
        print(f"{self.YELLOW}Publish date:{self.RESET} {video.publish_date}")
        print(f"{self.YELLOW}\nWhat would you like to do?\n")
        if is_mp3:
            print(f"{self.GREEN}1. Continue to download [MP3]")
        else:
            print(f"{self.GREEN}1. Continue to download [MP4]")
            
        print(f"{self.RED}2. Go back{self.RESET}")
        print(f"{self.RED}3. Cancel{self.RESET}")
        while True:
            choice = int(input(f"{self.YELLOW}\nChoice: {self.RESET}"))

            if choice == 1:    # choice 1 = continue to download 
                #redeclare yt downloader object with valid url
                yt = YouTubeDownloader(search=f"https://www.youtube.com/watch?v={video.video_id}")
                if mode == 2: # mode 1 == mp3 || mode 2 == mp4
                    self.separate_prompts()
                    return self.choose_resolution()
                elif mode == 1:
                    print(f"\n{self.GREEN}Starting download for {video.title}{self.RESET}\n")
                    self.separate_prompts()
                    return self.download_page()
            # if user wants to go back and user initially put a valid youtube link, return user to search input.
            elif choice == 2:
                if yt.is_link:
                    self.separate_prompts()
                    return self.inputURL_page()
                self.separate_prompts()
                return self.display_suggestions()
            
            elif choice == 3:
                self.separate_prompts()
                return self.inputURL_page()
            else:
                continue
            continue
            
    def choose_resolution(self):
        print(f"{self.CYAN}Available resolutions for download: (Please Wait)\n")
        resolutions = yt.fetch_available_resolutions()
        print(f"{self.GREEN}{resolutions}{self.RESET}")
        chosen_resolution = int(input("Choose your resolution: "))
        print(f"{self.GREEN}Starting download for {yt.YT.title}{self.RESET}")
        self.separate_prompts()
        return self.download_page(chosen_resolution)
        
    def download_page(self, resolution=None):
        if is_mp3:
            input(f"{self.GREEN}\nMP3 file is ready to be downloaded. Press Enter to start and wait.\n")
            print(f"Downloading...{self.RESET}")
            yt.download_mp3()
        elif not is_mp3:
            input(f"{self.GREEN}\nMP4 file is ready to be downloaded. Press Enter to start and wait.\n")
            print(f"Downloading...{self.RESET}")
            yt.download_video(resolution)
        
        
if __name__ == "__main__":
    colorama.init()
    gui = GUI()
    gui.init_dirs()
    
    while True:
        gui.start()
        gui.separate_conversions(10)
    
