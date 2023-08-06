<%inherit file="base.tpl"/>
<div id="message" style="display: none">
	<div class="corner tl"></div>
	<div class="corner tr"></div>
	<div class="corner bl"></div>
	<div class="corner br"></div>
	<div id="messageText"></div>
</div>
<h1 id="h1"><a href="/">${config.get('site_name')}</a></h1>
<div id="meta">
	<a href="http://fookebox.googlecode.com/">fookebox</a> ${config.get('version')}<br />
	&copy; 2007-2010 <a href="http://www.ott.net/">Stefan Ott</a>
</div>
<%include file="browse-menu.tpl"/>
<div id="status">
<%include file="status.tpl"/>
</div>
<img src="img/progress.gif" alt="" id="progress" style="display: none" />
<div id="searchResult"></div>
<script type="text/javascript">
<!--
	parseLocation();
-->
</script>
