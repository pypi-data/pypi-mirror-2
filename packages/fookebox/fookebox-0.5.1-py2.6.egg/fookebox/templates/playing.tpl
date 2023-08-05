<div id="nowPlaying">
	<h2><img src="img/sound.png" /> ${_('Now playing')}</h2>
	<ol>
		<li id="artist"></li>
		<li id="track"></li>
		<li id="time"><span id="timePassed"></span> / <span id="timeTotal"></span></li>
% if config.get('enable_controls'):
		<li id="control">
			<a href="#" onclick="javascript:control('prev'); return false"><img src="img/control_prev.png" alt="back" title="${_('back')}" /></a>
			<a href="#" onclick="javascript:control('pause'); return false"><img src="img/control_pause.png" alt="pause" title="${_('pause')}" /></a>
			<a href="#" onclick="javascript:control('play'); return	false"><img src="img/control_play.png" alt="play" title="${_('play')}" /></a>
			<a href="#" onclick="javascript:control('next'); return false"><img src="img/control_next.png" alt="next" title="${_('next')}" /></a>
			<a href="#" onclick="javascript:control('voldown'); return false"><img src="img/control_voldown.png" alt="volume down" title="${_('volume down')}" /></a>
			<a href="#" onclick="javascript:control('volup'); return false"><img src="img/control_volup.png" alt="volume up" title="${_('volume up')}" /></a>
			<a href="#" onclick="javascript:control('rebuild'); return false"><img src="img/control_rebuild.png" alt="rebuild database" title="${_('rebuild database')}" /></a>
		</li>
% endif
	</ol>
</div>
<div>
	<img id="nowPlayingCover" src="" width="200" alt="" style="display: none" />
</div>
