from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import yt_dlp
import os  # You forgot to import os

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = 'AIzaSyCvt-w7yTuFFsL1HeidXVxW4o1C367AbUI'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

@app.route('/api/stream/<video_id>')
def stream_audio(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
            'skip_download': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            audio_url = next(
                (
                    f['url']
                    for f in formats
                    if f.get('acodec') != 'none'
                    and f.get('vcodec') == 'none'
                    and f.get('ext') in ['m4a', 'webm']
                ),
                None
            )

            if audio_url:
                return jsonify({
                    'audio_url': audio_url,
                    'title': info.get('title'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'duration': info.get('duration')
                })
            else:
                return jsonify({'error': 'Audio URL not found'}), 404

    except Exception as e:
        print(f"❌ yt_dlp error for {video_id}: {e}")
        return jsonify({'error': str(e)}), 500


    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 50,
        'key': YOUTUBE_API_KEY,
    }

    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        data = response.json()

        songs = []
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']
            songs.append({
                'videoId': video_id,
                'title': snippet['title'],
                'channelTitle': snippet['channelTitle'],
                'thumbnail': snippet['thumbnails']['medium']['url'],
            })

        return jsonify({'songs': songs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stream/<video_id>')
def stream_audio(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = next(
                (
                    f['url']
                    for f in info['formats']
                    if f.get('acodec') != 'none'
                    and f.get('vcodec') == 'none'
                    and f.get('ext') in ['m4a', 'webm']
                ),
                None
            )

            if audio_url:
                return jsonify({
                    'audio_url': audio_url,
                    'title': info.get('title'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'duration': info.get('duration')
                })
            else:
                return jsonify({'error': 'Audio URL not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
