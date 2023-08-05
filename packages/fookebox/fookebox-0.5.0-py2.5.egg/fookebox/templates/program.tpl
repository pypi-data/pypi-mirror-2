<%inherit file="base.tpl"/>
<div id="now">
	<span class="label">${_('now playing')}</span><br />
	<span id="currentTitle"><img src="img/progress.gif" alt="" /></span>
</div>
<div class="state">
	<span id="currentState" style="display: none">
		<img src="img/progress.gif" alt="" />
	</span>
</div>
<div id="next" style="display: none">
	<span class="label">${_('coming up')}</span><br />
	<span id="nextTitle"></span>
	<br /><span class="time">@<span id="nextTime"></span></span>
</div>
<div id="clock"></div>
<script type="text/javascript">
<!--
	setTimeout('refreshProgram()', 1000);
-->
</script>
