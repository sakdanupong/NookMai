var carouselDict = {};

function Carousel(id, carousel_count, itemPerPage, allMovie, currentPage, callback) {
	var $ = document;
		var head  = $.getElementsByTagName('head')[0];
	    var link  = $.createElement('link');
	    link.rel  = 'stylesheet';
	    link.type = 'text/css';
	    link.href = '/stylesheets/carousel.css';
	    link.media = 'all';
	    head.appendChild(link);

		var carousel = "<div class='carousel_div'>\
			<div class='btn_carousel_div'><a class='btn_carousel' id='all_page_link'></a></div>\
            <div class='btn_carousel_div'><a class='btn_carousel' id='first_page_link'><< First</a></div>\
            <div class='btn_carousel_div'><a class='btn_carousel' id='prev_page_link'>< Prev</a></div>\
            <div id='page_btn_div'></div>\
            <div class='btn_carousel_div'><a class='btn_carousel' id='next_page_link'>Next ></a></div>\
            <div class='btn_carousel_div'><a class='btn_carousel' id='last_page_link'>Last >></a></div>\
          </div>"

	this.div = $.createElement('div');
    this.div.innerHTML = carousel;
    this.carouselCount = carousel_count;

    this.itemPerPage = itemPerPage;
   	this.all_movie_count = allMovie;
   	this.allPage = this.all_movie_count / itemPerPage;
    this.allPage = Math.ceil(this.allPage);
    this.currentPage = currentPage;

    this.btn_carousel_count = carousel_count;
	if (this.allPage < carousel_count)
    	this.btn_carousel_count = this.allPage;

    this.addCarouselToDiv = function(div) {
        this.initPaginationButton();
    	div.appendChild(this.div);
    }

    this.initPaginationButton = function() {
    	var allPageLink = this.GetElementInsideContainer('all_page_link');
    	var btnParentDiv = this.GetElementInsideContainer('page_btn_div');
    	allPageLink.innerHTML = 'Page '+ this.currentPage + ' of ' +  this.allPage;
    	for (var i = 0; i < this.btn_carousel_count; i++) {
            var btnWrapperDiv = document.createElement('div');
            btnWrapperDiv.className = 'btn_carousel_div';
            var btnDiv = document.createElement('a');
            var pageIndex = (this.currentPage + i);
            btnDiv.innerHTML = ''+ pageIndex;            
            btnDiv.href = "";
            btnDiv.onclick = function() {
            	var index = parseInt(this.innerHTML);
            	gotoPage(index);
            }
            btnWrapperDiv.appendChild(btnDiv);
            btnParentDiv.appendChild(btnWrapperDiv);
         }
         this.updatePositionCarousel();
    }

    this.GetElementInsideContainer = function(childID) {
	    var elm = {};
	    var elms = this.div.getElementsByTagName("*");
	    for (var i = 0; i < elms.length; i++) {
	        if (elms[i].id === childID) {
	            elm = elms[i];
	            break;
	        }
	    }
	    return elm;
	}

	this.renewCarousel = function(first_index) {
      var searchEles = this.GetElementInsideContainer("page_btn_div").children;
      for(var i = 0; i < searchEles.length; i++) {
        var carousel = this.getCarousel(i);
        var index = (first_index+i);
        carousel.innerHTML = ""+ index;
        carousel.href = "";
        carousel.onclick = function() {
        	var index = parseInt(this.innerHTML);
        	gotoPage(index);
        }
      }

    }

    this.enableCarousel = function(carousel_id, indexToGo) {
    	var carousel = this.GetElementInsideContainer(carousel_id);
    	carousel.href = "";
        carousel.className = 'btn_carousel';
        carousel.onclick = function() {
        	gotoPage(indexToGo);
        }
    }


	this.disableCarousel = function(carousel_id) {
      var carousel = this.GetElementInsideContainer(carousel_id);
      carousel.className = 'btn_carousel_disable';
      carousel.removeAttribute("href")
    }

    this.removeAllCarouselHiligth = function() {
    	var searchEles = this.GetElementInsideContainer("page_btn_div").children;
		for(var i = 0; i < searchEles.length; i++) {
			var carousel = this.getCarousel(i);
			carousel.className = "";
			carousel.className = "btn_carousel";
		}
    }

    this.enableAllCarousel = function() {
    	//$("#comingsoon_prev_page_link").attr("href", "javascript:getComingSoon("+ (comingsoon_current_page - 1) +");");
        //$("#comingsoon_next_page_link").attr("href", "javascript:getComingSoon("+ (comingsoon_current_page + 1) +");");
        //$("#comingsoon_last_page_link").attr("href", "javascript:getComingSoon("+ all_comingsoon_page +");");
        //$("#comingsoon_first_page_link").attr("href", "javascript:getComingSoon(1);");
        this.enableCarousel('prev_page_link', this.currentPage - 1);
        this.enableCarousel('next_page_link', this.currentPage + 1);
        this.enableCarousel('last_page_link', this.allPage);
        this.enableCarousel('first_page_link', 1);
    }

    this.updatePositionCarousel = function() {
    	this.enableAllCarousel();
		if (this.currentPage <= 1) {
			this.disableCarousel('prev_page_link');
			this.disableCarousel('first_page_link');
		}

		if (this.currentPage  == this.allPage) {
			this.disableCarousel('next_page_link');
			this.disableCarousel('last_page_link');
		} 

		//alert(''+this.currentPage);
		var allPageLink = this.GetElementInsideContainer('all_page_link');
		allPageLink.innerHTML = 'Page '+ this.currentPage + ' of ' +  this.allPage;
		this.removeAllCarouselHiligth();
		if (this.btn_carousel_count >= this.carouselCount) {
			var current_margin = this.allPage - this.currentPage;
			if (current_margin < (this.btn_carousel_count - 1)) {
			  var startPage = this.allPage - (this.btn_carousel_count - 1);
			  this.renewCarousel(startPage);
			} else {
			  this.renewCarousel(this.currentPage);
			}
		} 

		var searchEles = this.GetElementInsideContainer("page_btn_div").children;
		for(var i = 0; i < searchEles.length; i++) {
			var carousel = this.getCarousel(i);
			var a = parseInt(carousel.innerHTML);
			if (a == this.currentPage) {
			  carousel.className = "";
			  carousel.className = "btn_carousel_select";
			}
		}
    }

    this.getCarousel = function(index) {
          var searchEles = this.GetElementInsideContainer("page_btn_div").children;
          var btnDiv = searchEles[index];
          var carousel = btnDiv.children[0];
          return carousel;
    }

	var gotoPage = function(page) {
		callback(page);
		gotoPage.calousel.currentPage = page;
		gotoPage.calousel.updatePositionCarousel();
		event.preventDefault();		
	}
	gotoPage.calousel = this;
}

// Carousel.prototype.initPaginationButton = function() {
        



	
// 	// for (var i = 0; i < btn_comingsoon_count; i++) {
// 	// 	var btnWrapperDiv = document.createElement('div');
// 	// 	btnWrapperDiv.className = 'btn_carousel_div';
// 	// 	var btnDiv = document.createElement('a');
// 	// 	var pageIndex = (comingsoon_current_page + i);
// 	// 	btnDiv.innerHTML = ''+ pageIndex;
// 	// 	btnDiv.href = "javascript:getComingSoon("+ pageIndex +");";
// 	// 	btnWrapperDiv.appendChild(btnDiv);
// 	// 	btnParentDiv.appendChild(btnWrapperDiv);
// 	// }
// };



// Carousel.prototype.getCarouselDiv = function() {
// 	//this.initPaginationButton();
// 	//alert(this.all_movie_count+"");
// 	setTimeout(function() {
//         var btnParentDiv = this.div.getElementById('page_btn_div');
// 		var allPageLink = this.div.getElementById('all_page_link');
// 		allPageLink.innerHTML = 'Page '+ this.currentPage + ' of ' +  this.allPage;
//     }, 0); 
    
		

// 		//alert("fuck");


//   	return this.div;
// };


// function initCaroucel(keyName, carousel_count, itemPerPage, allPage, currentPage) {

// }

// function createCarouselDict(carousel_count, itemPerPage, allPage, currentPage) {
//     var vote_result = (rate_count * vote_comment_count) + vote_count;
//     var dict = {
//         'vote_state' : state,
//         'vote_count' : vote_result,
//     };
//     return dict;
// }
