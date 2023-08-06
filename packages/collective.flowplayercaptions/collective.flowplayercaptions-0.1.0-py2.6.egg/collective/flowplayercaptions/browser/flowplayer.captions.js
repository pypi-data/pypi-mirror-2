/**
 * Javascript code for Flowplayer caption inside Plone
 */

jq(document).ready(function () {

	var captionsData = jq(".captionsData");

    $f("*").each(function (index) {
		var captionPlugin = null;
		var contentsPlugin = null;

		/**
		 * Activate captions on a video; playlist supported
		 * @param {Object} clip the clip on which activate captioning
		 */
		var activateCaptions = function(clip) {
			captionsData.find('dt').each(function(index) {
				if (clip.url.indexOf(jq(this).text())===0) {
					clip.update({ captionUrl: captionsData.find('dd:eq('+index+')').text() });				
				}				
			});
		}	
		
        this.onBeforeLoad(function (event) {			
			var clip = this.getCommonClip();
			activateCaptions(clip);
		});
		
		this.onLoad(function (event) {
			captionPlugin = this.getPlugin('captions');
			contentsPlugin = this.getPlugin('captionsContent');
			
			// Hide caption area if no caption there
			if (captionsData.length==0) {
				contentsPlugin.hide();
			}
		});
		
		/**
		 * collective.flowplayer don't use Flowplayer playlist
		 * @param {Array} playlist the array of new clips (length is seems always one)
		 */
		this.onPlaylistReplace(function(playlist) {
			var clip = playlist[0];
			//activateCaptions(clip);
			//contentsPlugin.loadCaptions(0, 'http://localhost:8080/Plone/cultura/at_download/captions', 'srt')
		});
		
	});
});

