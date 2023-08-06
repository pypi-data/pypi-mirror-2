${entry.artist} - ${entry.title}
% if config.get('enable_song_removal'):
<a href="#" onclick="javascript:removeTrack(${entry.queuePosition}); return false"> <img src="img/delete.png" alt="x" title="remove this track from the playlist" /></a>
% endif
