var vote_data_dict = {};
var vote_score = 1;
var divForSort;
function MoviewListView(p_divForSort, movie_data, user_id) {
	var $ = document;
	var head  = $.getElementsByTagName('head')[0];
    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/movie_listview.css';
    link.media = 'all';
    head.appendChild(link);

    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/poster.css';
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

    var comment_count = data['comment_count'];
    var comment_unit = ' Comment';
    if (comment_count > 1)
        comment_unit = ' Comments';

    var topComment = "dfdlgnjdfkghfdkjgfjdgkljfglkjglkdfjgkdfjgkjdflkgjdfgljdfklgjfglkjdflkgjdfkljglfjgldfgldkf;jgldf;gdfkdfgk;dfklkfgkdfkdfkl;fdfgkdflgfd;lkglk;gklgdfkl";
// <div id='top_comment_div'>“" +topComment+ "”</div>\
	var dialog = "<div id='movie_listview_content'>\
                    <div id='movie_listview_detail_div'>\
                        <div id='movie_listview_right_img_div'>\
                            <div id='movie_listview_detia_rigth'>\
                                <div>\
                                    <a id='comment_count_link' href='"+ detail_link +"' >"+ comment_count + comment_unit+"</a>\
                                </div>\
                                <div class='top_comment_cls' id='top_comment_div'></div>\
                            </div>\
                            <div id='movie_listview_detia_left'>\
                                <a href='"+ detail_link +"' style='text-decoration: none;'><div id='movie_listview_movie_name'>" + movie_name + "</div></a>\
                                <div id='rate_div_"+ movie_id +"'></div>\
                                <div id='emotion_div_"+ movie_id +"'></div>\
                            </div>\
                        </div>\
                        <div id='movie_listview_img_div'>\
                            <div class='roll_over'>\
                                <img class='poster_image' src="+ image_src +"></img>\
                                <a class='description' href='"+ detail_link +"' style='text-decoration: none;'></a>\
                            </div>\
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
        var emotion_list = getAvatarDict(movie_data);
        var rate_count = data['movie_rate'];
        var avatarCountSummary = getSummaryAvatarCount(movie_data);
        addRate(rate_count, movie_id);
        addEmotionList(emotion_list, avatarCountSummary, movie_id);
        //checkTextHeight(topComment);
    }, 0); 
    
    divForSort = p_divForSort;

    return div;
}

function short(length) {
  var s = document.getElementsByClassName("top_comment_cls");
  var len = s.length;
    for(var i = 0; i < len; i++) {
        
        var g = s[i].innerHTML;

        if (g.length > length - 5) {
            var x = "“"
            var y = ". . .”";
            var leng = length-5;
            var html = g.substring(0, leng)+"";
            var allHTML = x+html+y;
            s[i].innerHTML = allHTML;
        } else {
            if (s[i].innerHTML.length > 0) {
                var g = s[i].innerHTML;
                var leng = length-2;
                var html = g.substring(0, leng)+"";
                s[i].innerHTML = "“"+html+"”";
            }

        }
    }
}

function checkTextHeight(text) {
    document.getElementById('top_comment_div').innerHTML=text;
    short(125);    
    //var testDiv = document.getElementById('top_comment_div');
}

function getSummaryAvatarCount(data) {
    var allAvatarCount = 0;
    for (var i = 1; i < avatar_count; i++) {
        var key_value = 'avatar_'+i+'_count';
        allAvatarCount+= data[key_value];
    }
    return allAvatarCount;
}

function getAvatarDict(data) {

  var status = [];
  for (var i = 1; i < avatar_count; i++) {
    var key_value = 'avatar_'+i+'_count';
    status.push({name: '/images/details/avatar/image_avatar' + i +'.png', value: data[key_value]});
  }

  status.sort(function(a, b){

  if(a.value > b.value){
    return -1;
  }
  else if(a.value < b.value){
    return 1;
  } 
  return 0;
  });

  return status;
}

function addEmotionList(data_list, avatar_summary, movie_id) {
    var emotion_div_id = 'emotion_div_'+ movie_id;
    var emotion_div = document.getElementById(emotion_div_id);
    for (var j = 0; j<3; j++) {
        var avatar_at_index = data_list[j];
        var image_path = avatar_at_index.name;
        var count = avatar_at_index.value;
        var badge_count = ((count * 100) / avatar_summary) / 20;
        if (badge_count) {
            var div = document.createElement('div');
            var innerHTML = "";
            for (var i = 0; i < 3; i++) {
                innerHTML += "<img class='poster_avatar_image' src="+ image_path +"><img>";    
            }
            div.innerHTML = innerHTML;
            emotion_div.appendChild(div);
        }
    }
    //emotion_div.innerHTML = innerHTML;
}

function addRate(rate_count, movie_id) {
    var innerHTML = "";
    var rate_div_id = 'rate_div_'+ movie_id;
    var rate_div = document.getElementById(rate_div_id);
    var ceilvalue = Math.ceil(rate_count);
    var intvalue = Math.floor(rate_count);
    for (var i =0; i < intvalue; i++) {
        innerHTML += "<span class='glyphicon glyphicon-star pink'></span>";
    }
    if (intvalue<ceilvalue)
        innerHTML += "<span class='glyphicon glyphicon-star-empty pink star_small'></span>";
    rate_div.innerHTML = innerHTML;
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

    // alert(''+vote_state);

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
    
    //sortUsingNestedText(divForSort, "div", 'div.vote_count');

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

    // alert(''+vote_state);

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

    //sortUsingNestedText(divForSort, "div", 'div.vote_count');

}

function sortUsingNestedText(parent, childSelector, keySelector) {
    var items = parent.children(childSelector).sort(function(a, b) {
        var vA = $(keySelector, a).text();
        var vB = $(keySelector, b).text();
        return (vB < vA) ? -1 : (vB > vA) ? 1 : 0;
        // return vB - vA;
        // return (vA < vB) ? -1 : (vA > vB) ? 1 : 0;
    });
    parent.append(items);
}


