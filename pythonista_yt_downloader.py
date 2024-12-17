from __future__ import unicode_literals
import ui

import yt_dlp as youtube_dl
import appex
import console
import clipboard
import os
import sys


def generateTapped(sender):
	'@type sender: ui.Button'
	# Get the button's title for the following logic:
	global shows_result
	# Get the labels:
	label = sender.superview['label1']
	label2 = sender.superview['label6']
	text = sender.superview['textfield1']
	outdir = os.path.expanduser("~/Documents/Downloads")
	try:
	    os.mkdir(outdir)
	except FileExistsError:
	    pass
	
	# Get URL from different possible sources (attachments, URLs, clipboard, text)

	    url = text.text
	
	print("URL: ", url)
	if not url or not url.startswith("http"):
	    url = input("No URL found - enter URL to download: ")
	
	# Setup options for yt-dlp to download best quality video (H.264 only)
	# Callback to update video progress

# Callback to update video progress
	def video_progress_hook(d):
	    label2 = sender.superview['label2']  # Use the UI label for updates
	    if d['status'] == 'downloading':
	        label2.text = f"Downloading Video: {d['_percent_str']} | {d['_speed_str']} | ETA: {d['eta']}s"
	    elif d['status'] == 'finished':
	        label2.text = "Video download complete."

# Callback to update audio progress
	def audio_progress_hook(d):
	    label2 = sender.superview['label2']  # Use the UI label for updates
	    if d['status'] == 'downloading':
	        label2.text = f"Downloading Audio: {d['_percent_str']} | {d['_speed_str']} | ETA: {d['eta']}s"
	    elif d['status'] == 'finished':
	        label2.text = "Audio download complete."

	ydl_opts_video = {
    'format': 'bestvideo[vcodec~="^avc1"]',  # Download best video with H.264 codec
    'outtmpl': os.path.join(outdir, '%(title)s_video.%(ext)s'),
    'noplaylist': True,
    'quiet': True,  # Suppress shell output
    'progress_hooks': [video_progress_hook],  # Add the hook
}
	
	# Download video
	with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
	    info = ydl.extract_info(url, download=True)
	    video_filepath = ydl.prepare_filename(info)
	    print(f"Video downloaded: {video_filepath}")
	
	    # Find the format with the best resolution
	    valid_formats = [f for f in info['formats'] if f.get('height')]
	    if valid_formats:
	      best_video = max(valid_formats, key=lambda f: f['height'])
	      resolution = f"{best_video['height']}p"
	    else:
	      best_video = None
	      resolution = "Unknown"
	      resolution = f"{best_video['height']}p" if 'height' in best_video else "Unknown"
	      print(f"Downloaded video resolution: {resolution}")
	      label2.text = f"Downloaded video resolution: {resolution}"
	
	# Setup options for yt-dlp to download best quality audio (M4A)
	ydl_opts_audio = {
    'format': 'bestaudio[ext!=webm]/bestaudio[ext=m4a]/bestaudio/best',
    'outtmpl': os.path.join(outdir, '%(title)s_audio.%(ext)s'),
    'noplaylist': True,
    'quiet': True,  # Suppress shell output
    'progress_hooks': [audio_progress_hook],  # Add the hook
}
	
	# Download audio
	with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
	    info = ydl.extract_info(url, download=True)
	    audio_filepath = ydl.prepare_filename(info)
	    print(f"Audio downloaded: {audio_filepath}")
	    label2.text = f"Audio downloaded: {audio_filepath}"
	    v.close()
	# Let the user know where the files are saved
	console.open_in(outdir)
	label.text = 'test'

v = ui.load_view('test_1')
v.present('test_1')


	
