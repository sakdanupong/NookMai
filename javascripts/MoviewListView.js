var vote_data_dict = {};

function MoviewListView(movie_data) {
	var $ = document;
	var head  = $.getElementsByTagName('head')[0];
    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/movie_listview.css';
    link.media = 'all';
    head.appendChild(link);

    var data = movie_data;
    var movie_id = data['movie_id'];
    var image_src =  '/image?movie_id='+movie_id;
    var movie_name = data['name_en'];
    var detail_link = '/detail/'+movie_id;
    up_id = 'up' + movie_id;
    down_id = 'down' + movie_id;

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
                            <div id="+ up_id +" ></div>\
                            <div class='vote_count'>"+ 0 +"</div>\
                            <div id="+ down_id +" ></div>\
                        </div>\
                    </div>\
                 </div>";

	var div = $.createElement('div');
    div.innerHTML = dialog;

    initVoteData(data);

    setTimeout(function() {
        var voteState = getUserVoteData(data);
        setVoteState(voteState, data);
        var arrow_up = getUpArrowIdByData(data);
        var arrow_down = getDownArrowIdByData(data);
        arrow_up.onclick = function() { 
            voteMovie(data);
        };
        arrow_down.onclick = function() { 
            unVoteMovie(data);
        };
    }, 0); 
    

    return div;
}

function getDictValue(state) {
    var user_vote_data = {
        "vote_state" : state,
    };
    return user_vote_data;
}

function initVoteData(data) {
    var key_name = 'movie_id' + data['movie_id']
    var user_vote_data = data['user_vote_data'];
    if (user_vote_data) {
        var voteState = user_vote_data['vote_state'];
        vote_data_dict[key_name] = getDictValue(voteState);
    } else {
        vote_data_dict[key_name] = getDictValue(0);
    }
}

function getUserVoteData(data) {
    var key_name = 'movie_id' + data['movie_id']
    var vote_dict = vote_data_dict[key_name];
    var vote_state = vote_dict['vote_state'];
    return vote_state;
}

function increseVote(data) {
    var key_name = 'movie_id' + data['movie_id']
    var vote_dict = vote_data_dict[key_name];
    var vote_state = vote_dict['vote_state'];
    vote_state = vote_state + 1;
    vote_data_dict[key_name] = getDictValue(vote_state);
}

function getDownArrowIdByData(data) {
    var movie_id = data['movie_id'];
    var down_id = 'down' + movie_id;
    var arrow_down = document.getElementById(down_id);
    return arrow_down;
}

function getUpArrowIdByData(data) {
    var movie_id = data['movie_id'];
    var up_id = 'up' + movie_id;
    var arrow_up = document.getElementById(up_id);
    return arrow_up;
}

function unSelectAllArrow(data) {
    var arrow_up = getUpArrowIdByData(data);
    var arrow_down = getDownArrowIdByData(data);
    arrow_up.className = 'arrow-up';
    arrow_down.className = 'arrow-down';
}

function setVoteState(state, data) {

    var arrow_up = getUpArrowIdByData(data);
    var arrow_down = getDownArrowIdByData(data);

    unSelectAllArrow(data);
    if (state == 1) {
        arrow_up.className = 'arrow-up-selected';
    } else if (state == -1) {
        arrow_down.className = 'arrow-down-selected';
    }

}

function voteMovie(data) {
    var vote_state = getUserVoteData(data);
    if (vote_state == 1)
        return;
    alert('voteMovie');
    increseVote(data);
    setVoteState(1, data);
}

function unVoteMovie(data) {
     setVoteState(-1, data);
}