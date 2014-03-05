function MoviePoster(movie_data) {
	var $ = document;
	var head  = $.getElementsByTagName('head')[0];
    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/poster.css';
    link.media = 'all';
    head.appendChild(link);

    var data = movie_data;
    var movie_id = data['movie_id'];
    var image_src =  '/image?movie_id='+movie_id;
    var name_en = data['name_en'];

	var poster = "<div class='poster_div'>\
                    <img class='poster_image' src="+ image_src +">\
                    <div class='poster_title poster_title_white'>"+ name_en +"</div> \
                  </div>";

	var div = $.createElement('div');
    div.innerHTML = poster;

    return div;
}