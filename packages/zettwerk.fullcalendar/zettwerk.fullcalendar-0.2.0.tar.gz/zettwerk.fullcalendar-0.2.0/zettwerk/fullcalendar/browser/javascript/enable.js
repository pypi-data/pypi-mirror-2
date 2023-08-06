var defaultCalendarOptions = null;
jq(document).ready(function() {
    if (defaultCalendarOptions !== null) {
	if (defaultCalendarOptions.preview) {
	    defaultCalendarOptions['eventRender'] = function(event, element) {
		addPreviewText(event, element);
	    };
	}
	jq('#jquery-fullcalendar').fullCalendar(defaultCalendarOptions);
    }
});

var addPreviewText = function(event, element) {
    var preview = ' <a class="fc-event-title" href="'+element.attr('href')+'"><span>' + defaultCalendarOptions.preview + '</span></a>';
    jq(preview).appendTo(element.find('div'));
    element.find('a').prepOverlay({
        subtype: 'ajax',
        filter: '#content > *'
    });
};
