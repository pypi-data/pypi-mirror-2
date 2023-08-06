/**
 * Demo code for example.redturtlesubsites_theme
 */

jq(document).ready(function() {
	var demo = jq("<div><h2>Welcome To The demo</h2></div>").hide();
	jq("#portal-globalnav").append(demo);
	demo.show('slow');
});
