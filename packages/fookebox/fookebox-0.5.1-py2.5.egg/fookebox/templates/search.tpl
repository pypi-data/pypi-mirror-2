<h2>${what}</h2>
% if len(albums) < 1:
	Nothing found
% endif
<ul id="searchResultList">
% for album in albums:
	<li class="searchResultItem">
% if config.get('album_cover_path'):
%	if album.hasCover():
		<img src="cover/${album.getCoverURI()}" width="200" class="coverArt" alt="" />
% 	endif
% endif
		<h3 class="album">
% if where == 'genre':
	${album.artist}
% endif
% if config.get('enable_queue_album'):
			<a href="#" onclick="
% for track in album.tracks:
				queueFile('${track.b64}');
% endfor
				return false
			">
% endif
				${album.name}
% if album.disc != None:
				(Disc ${album.disc})
% endif
% if config.get('enable_queue_album'):
				</a>
% endif
		</h3>
		<ul class="trackList">
% for track in album.tracks:
			<li class="track"><a href="#" onclick="javascript:queueFile('${track.b64}'); return false">${"%02d" % track.track} - ${track.artist} - ${track.title}</a></li>
% endfor
		</ul>
	</li>
% endfor
</ul>
