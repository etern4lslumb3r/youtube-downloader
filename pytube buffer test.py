from pytube import YouTube
from io import BytesIO

# get all available resolutions in this youtube video
def get_resolutions():
    available_resolution = []
    for stream in streams_video:
        if stream.resolution is not None:
            resolution = int(stream.resolution.strip('p'))
            if resolution not in available_resolution:
                available_resolution.append(resolution)
    available_resolution = sorted(available_resolution)
    return available_resolution

# get stream object type of video using resolution
def get_video_stream(resolution):
    return streams_video.filter(res=str(resolution)+"p").first()


# get stream object with the highest quality sound
def highest_abr(): #returns stream of highest audio quality
    available_abr = []
    for stream in streams_audio:
        if stream.abr is not None:
            available_abr.append(int(stream.abr.strip('kbps')))
    top_abr = sorted(available_abr, reverse=True)[0]
    top_stream_audio = streams_audio.filter(abr=str(top_abr)+"kbps")
    return top_stream_audio


# download video file into a buffer
def buffer_video(stream):
    buffer = BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer
    
        
# download audio file into a buffer
def buffer_audio(stream):
    buffer = BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer
    
# combine audio and video buffer into one file
def combine_audio_video_buffer(video_buffer, audio_buffer):  #hopefully outputs videofile
    pass




if __name__ == "__main__":
    yt = YouTube(url="https://youtu.be/gm1QSfY-59g")
    fps_60_streams = []
    streams_video = yt.streams.filter(progressive=False, only_video=True)
    streams_audio = yt.streams.filter(progressive=False, only_audio=True)
    
    for audio_stream in streams_audio:
        print(audio_stream)
    
    for stream in streams_video:
        if stream.fps == 60:
            fps_60_streams.append(stream)


    available_resolutions = get_resolutions()
    print(available_resolutions)
    
    resolution_choice = int(input("Choose resolution: "))
    video_stream = get_video_stream(resolution=resolution_choice)    
    print(video_stream)
    audio_stream = highest_abr()
    print(audio_stream)
    
    video_buffer = buffer_video(video_stream)
    audio_buffer = buffer_audio(video_stream)
    
