var data;

function MoviewListView(movie_data) {
	var $ = document;
	var head  = $.getElementsByTagName('head')[0];
    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/movie_listview.css';
    link.media = 'all';
    head.appendChild(link);

    data = movie_data;
    var movie_id = data['movie_id'];
    var image_src =  '/image?movie_id='+movie_id;
    var movie_name = data['name_en'];
    var detail_link = '/detail/'+movie_id;
	var dialog = "<div id='movie_listview_content'>\
                    <div id='movie_listview_detail_div'>\
                        <div id='movie_listview_right_img_div'>\
                            <div id='movie_listview_detia_rigth'>\
                            </div>\
                            <div id='movie_listview_detia_left'>\
                                <a href='"+ detail_link +"' style='text-decoration: none;'><div id='movie_listview_movie_name'>" + movie_name + "</div></a>\
                            </div>\
                        </div>\
                        <div id='movie_listview_img_div'>\
                            <a href='"+ detail_link +"' style='text-decoration: none;'><img class='poster_image' src="+ image_src +"></img></a>\
                        </div>\
                    </div>\
                    <div id='movie_listview_vote_div'>\
                        <div id='vote_div'>\
                            <div class='arrow-up'></div>\
                            <div class='vote_count'>"+ 0 +"</div>\
                            <div class='arrow-down'></div>\
                        </div>\
                    </div>\
                 </div>";

	var div = $.createElement('div');
    div.innerHTML = dialog;

    return div;
}
