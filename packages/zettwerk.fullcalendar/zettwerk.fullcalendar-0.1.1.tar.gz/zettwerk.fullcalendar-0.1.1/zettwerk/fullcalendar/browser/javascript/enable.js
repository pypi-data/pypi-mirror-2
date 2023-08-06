$(document).ready(function() {
    try {
	$('#calendar').fullCalendar(defaultCalendarOptions);
    } catch(e) {
	null; // ignore views, that dont use the calendar
    }
});
