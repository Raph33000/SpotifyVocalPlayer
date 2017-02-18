#!/usr/bin/env python

import spotipy
import sys
import spotipy.util as util
import requests.packages.urllib3
import vlc
import time
import random

class currentUser:
	username = ''
	token = ''
	tracklist = []
	titles = []

	def getUsername(self):
		return self.username

	def setToken(self, token):
		self.token = token

	def getToken(self):
		return self.token

	def setUsername(self, username):
		self.username = username

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name'])

def get_playlist_tracks(username,playlist_id, sp):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def getTracksFromAllPlaylists(sp, name, me):
	results = sp.search(q='playlist:' + name, type='playlist')
	items = results['playlists']['items']
	nb = 0
	for i in range(0, len(items)):
 		playlist = get_playlist_tracks(items[i]['owner']['id'], items[i]['id'], sp)
 		for j in range (0, 5000):
 			if (nb > len(playlist)):
 				return me
 			if (j == len(playlist)):
 				break
 			me.tracklist.append(playlist[j]['track']['external_urls']['spotify'])
			me.titles.append(playlist[j]['track']['name'])
 		nb += j
 	return me

def main(): 

	print('Welcome on the Spotify Vocal Player ~by RaphX~')
	requests.packages.urllib3.disable_warnings()

	me = currentUser()
	me.setUsername('2123jaklehs6dd4twoz7btv2i')
	scope = 'user-library-read'
	me.setToken(util.prompt_for_user_token(me.getUsername(), scope))
	if (me.token == None) :
		exit()
	sp = spotipy.Spotify(auth=me.token)
	if len(sys.argv) > 1:
		name = ' '.join(sys.argv[1:])
	else:
		name = 'Chill house'
	me = getTracksFromAllPlaylists(sp, name, me)
	me.tracklist = list(set(me.tracklist))
	instance=vlc.Instance()
	while (len(me.tracklist) > 0):
		songNumber = random.randrange(0, len(me.tracklist))
		player=instance.media_player_new()
		media=instance.media_new(me.tracklist[songNumber])
		print me.titles[songNumber]
		media.get_mrl()
		player.set_media(media)
		player.play()
		playing = set([1,2,3,4])
		time.sleep(1) #Give time to get going
		duration = player.get_length() / 1000
		mm, ss = divmod(duration, 60)
		print "Playing", me.titles[songNumber], "Length:", "%02d:%02d" % (mm,ss)
		while True:
			state = player.get_state()
			if state not in playing:
				print 'okok'
				break
			continue
		del me.tracklist[songNumber]	       

if __name__ == "__main__":
    main()