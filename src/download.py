from pytube import YouTube
import yt_dlp

def download(url:str) -> str:
    yt = YouTube(url)
    videoid = yt.video_id

    ydl_opts = {'outtmpl': videoid}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return videoid


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=5qap5aO4i9A"
    download(url)