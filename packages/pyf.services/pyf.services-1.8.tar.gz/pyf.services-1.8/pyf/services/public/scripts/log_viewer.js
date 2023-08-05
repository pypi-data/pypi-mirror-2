max_prog_width = null;

var base_title = document.title;

function compute_max_prog_width() {
	progressionEl = $('progression');
	old_width = progressionEl.getSize().x - 2;
	progressionEl.setStyle('width', '');
	max_prog_width = progressionEl.getSize().x - 2;
	progressionEl.setStyle('width', old_width+"px");
}

function update_progression(percent) {
	if (percent == null)
		percent = 0;
	prog_width = ((max_prog_width / 100) * percent.toInt()).toInt();
	
	document.id('progression').morph({
		'width': prog_width + '%'
	});
	
	$$('#progression p').set('text', percent.toInt() + "%");
	if (percent > 54) {
		$$('#progression p').morph({
			'color': '#fff'
		});
	}

    document.title = base_title + " - " + percent.toInt() + "%";
}

function set_output_files(output_files) {
	$('output_files').empty();
	output_files.each(function(output_file) {
		new Element('A', {
			'href': '/events/download_output/' + output_file.id,
			'text': output_file.filename
		}).inject('output_files');
		new Element('BR').inject('output_files');
	});
	$('output_files').morph({
		'opacity': 1
	});
}

function show_message(message) {
	var bubble = new Element('div', {
		'class': 'bubble',
		'style': {
			'overflow': 'hidden'
		}
	}).inject($('messages'), "top");
	
    var bq = new Element(
		'blockquote'
	).inject(new Element('div', {'class': 'rounded ' + message.message_type}).inject(bubble));

	new Element('span', {
        'class': 'message_type',
		'text': message.message_type
	}).inject(bq);

	new Element('P', {
		'text': message.message
	}).inject(bq);

	new Element('cite', {
		'class': 'rounded ' + message.message_type,
		'html': '<strong>' + message.source + '</strong> on ' + message.timestamp
	}).inject(bubble);
	
	bubble.get('morph').start({
		'height': [0, bubble.getSize().y],
		'opacity': [0, 1]
	}).chain(function(bubble) {
		bubble.setStyle('overflow', 'visible');
	}.pass(bubble));
	
}
window.addEvent('domready', function() {
	periodical_func = (function() {
		new Request.JSON({
			url: json_url,
			method: 'get',
			onSuccess: function(response) {
				
				if (max_prog_width == null)
					compute_max_prog_width();
				
				value = response.value;
				update_progression(value.progression);
				if ((value.status == 'success') | (value.status == 'failure'))
					$clear(periodical_func);
				
				$('status').set('text', value.status);
				
				messages = value.history;
				messages.sort(function(a, b) {return (a.id - b.id);});
				messages.each(function(message) {
					if (message.id > max_comment_id)
					{
						show_message(message);
						max_comment_id = message.id;
					}
				});
				set_output_files(value.output_files);
			}
		}).send();
	}).periodical(500);
});
