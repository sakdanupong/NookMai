var vote_data_dict = {};
var vote_score = 1;
function MoviewListView(movie_data, user_id) {
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
    up_id = getUpArrowId(movie_id);
    down_id = getDownArrowId(movie_id);
    var count_id = getVoteCountId(movie_id);

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
                            <div id="+ count_id +" class='vote_count'></div>\
                            <div id="+ down_id +" ></div>\
                        </div>\
                    </div>\
                 </div>";

	var div = $.createElement('div');
    div.innerHTML = dialog;

    initVoteData(data);

    setTimeout(function() {
        setVoteState(movie_id);
        setVoteCount(movie_id);
        var arrow_up = getUpArrowDivByData(movie_id);
        var arrow_down = getDownArrowDivByData(movie_id);
        arrow_up.onclick = function() { 
            voteMovie(movie_id, user_id);
        };
        arrow_down.onclick = function() { 
            unVoteMovie(movie_id, user_id);
        };
        
    }, 0); 
    
    return div;
}

function getVoteCountId(movie_id) {
    var count_id = 'movie_count_' + movie_id;
    return count_id;
}

function initVoteData(data) {
    var movie_id = data['movie_id'];
    var key_name = getUserVoteKeyName(movie_id);
    
    var movie_vote = data['movie_vote'];
    var rate_count = movie_vote['rate_count'];
    var vote_count = movie_vote['vote_count'];
    var vote_comment_count = movie_vote['vote_comment_count'];

    var user_vote_data = data['user_vote_data'];
    var user_id = user_vote_data['user_id'];

    if (user_id) {
        var voteState = user_vote_data['vote_state'];
        vote_data_dict[key_name] = createDict(voteState, rate_count, vote_count, vote_comment_count);
    } else {
        vote_data_dict[key_name] = createDict(0, rate_count, vote_count, vote_comment_count);
    }
}

function getVoteCountId(movie_id) {
    var count_id = 'vote_count' + movie_id;
    return count_id;
}

function getDownArrowId(movie_id) {
    var down_id = 'down' + movie_id;
    return down_id;
}

function getUpArrowId(movie_id) {
    var up_id = 'up' + movie_id;
    return up_id;
}

function getUserVoteKeyName(movie_id) {
    var key_name = 'movie_id' + movie_id;
    return key_name;
}

function getUserVoteState(movie_id) {
    var key_name = getUserVoteKeyName(movie_id);
    var vote_dict = vote_data_dict[key_name];
    var vote_state = vote_dict['vote_state'];
    return vote_state;
}

function getUserVoteCount(movie_id) {
    var key_name = getUserVoteKeyName(movie_id);
    var vote_dict = vote_data_dict[key_name];
    var vote_count = vote_dict['vote_count'];
    return vote_count;
}

function getDownArrowDivByData(movie_id) {
    var down_id = getDownArrowId(movie_id);
    var arrow_down = document.getElementById(down_id);
    return arrow_down;
}

function getUpArrowDivByData(movie_id) {
    var up_id = getUpArrowId(movie_id);
    var arrow_up = document.getElementById(up_id);
    return arrow_up;
}

function createDict(state, rate_count, vote_count, vote_comment_count) {
    var vote_result = (rate_count * vote_comment_count) + vote_count;
    var dict = {
        'vote_state' : state,
        'vote_count' : vote_result,
    };
    return dict;
}

function setVoteStateDict(movie_id, state) {
    var key_name = getUserVoteKeyName(movie_id);
    var dict = vote_data_dict[key_name];
    dict['vote_state'] = state;
}

function setVoteCountDict(movie_id, count) {
    var key_name = getUserVoteKeyName(movie_id);
    var dict = vote_data_dict[key_name];
    dict['vote_count'] = count;
}

function unSelectAllArrow(movie_id) {
    var arrow_up = getUpArrowDivByData(movie_id);
    var arrow_down = getDownArrowDivByData(movie_id);
    arrow_up.className = 'arrow-up';
    arrow_down.className = 'arrow-down';
}

function setVoteState(movie_id) {
    var voteState = getUserVoteState(movie_id);
    var arrow_up = getUpArrowDivByData(movie_id);
    var arrow_down = getDownArrowDivByData(movie_id);

    unSelectAllArrow(movie_id);
    if (voteState == 1) {
        arrow_up.className = 'arrow-up-selected';
    } else if (voteState == -1) {
        arrow_down.className = 'arrow-down-selected';
    }

}

function setVoteCount(movie_id) {
    var vote_count = getUserVoteCount(movie_id);
    var count_id = getVoteCountId(movie_id);
    var div = document.getElementById(count_id);
    div.innerHTML = '' + vote_count;
}

function increseVote(movie_id) {
    var key_name = getUserVoteKeyName(movie_id);
    var vote_dict = vote_data_dict[key_name];
    var vote_state = vote_dict['vote_state'];
    vote_state = vote_state + 1;
    setVoteStateDict(movie_id, vote_state);

    var vote_count = vote_dict['vote_count'];
    vote_count = vote_count + vote_score;
    setVoteCountDict(movie_id, vote_count)

    setVoteState(movie_id);
    setVoteCount(movie_id);
}

function decreseVote(movie_id) {
    var key_name = getUserVoteKeyName(movie_id);
    var vote_dict = vote_data_dict[key_name];
    var vote_state = vote_dict['vote_state'];
    vote_state = vote_state - 1;
    setVoteStateDict(movie_id, vote_state);

    var vote_count = vote_dict['vote_count'];
    vote_count = vote_count - vote_score;
    setVoteCountDict(movie_id, vote_count)

    setVoteState(movie_id);
    setVoteCount(movie_id);
}

function voteMovie(movie_id, user_id) {
    if (!user_id) {
        showLoginDialog();
        return;
    }

    var vote_state = getUserVoteState(movie_id);
    if (vote_state == 1)
        return;
    increseVote(movie_id);

    var formData = new FormData();
    formData.append('user_id', user_id);
    formData.append('movie_id', movie_id);
    var vote_state = getUserVoteState(movie_id);
    formData.append('vote_state', vote_state);

    $.ajax({
        url: '/api_vote_movie',  //Server script to process data
        type: 'POST',
        mimeType:"multipart/form-data",
        dataType: 'json',
        success: function(json) {
            
        },
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    });
    
}

function unVoteMovie(movie_id, user_id) {
    if (!user_id) {
        showLoginDialog();
        return;
    }
    // STATE
    var vote_state = getUserVoteState(movie_id);
    if (vote_state == -1)
        return;
    decreseVote(movie_id);


    var formData = new FormData();
    formData.append('user_id', user_id);
    formData.append('movie_id', movie_id);
    var vote_state = getUserVoteState(movie_id);
    formData.append('vote_state', vote_state);

    $.ajax({
        url: '/api_unvote_movie',  //Server script to process data
        type: 'POST',
        mimeType:"multipart/form-data",
        dataType: 'json',
        success: function(json) {
            
        },
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    });

}