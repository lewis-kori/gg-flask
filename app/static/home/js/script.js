;(function($){

	'use strict';

	$(function(){

		document.addEventListener("touchstart", function() {},false);

		if ('ontouchstart' in document.documentElement) {
			$('body').css('cursor', 'pointer');
		}

		/* ---------------------------------------------------- */
		/*	Revolution slider									*/
		/* ---------------------------------------------------- */

	    if ($('#rev-slider').length) {
			jQuery("#rev-slider").revolution({
	            sliderType:"standard",
		    	spinner: "spinner3",
		    	responsiveLevels: [4096,1024,778,480],
		    	delay:6000,
	            navigation: {
	                arrows:{
	                	enable:true,
	                	left: {
							container:"slider",
				            h_align:"left",
				            v_align:"center",
				            h_offset:30,
				            v_offset:0
						},
						right: {
				            container:"slider",
				            h_align:"right",
				            v_align:"center",
				            h_offset:30,
				            v_offset:0
						}
	                },
	                bullets:{
			        	style:"",
			        	enable: true,
			        	container: "slider",
			        	hide_onmobile: false,
			        	hide_onleave: false,
			        	hide_delay: 200,
			        	hide_under: 0,
			        	hide_over: 9999,
			        	tmp:'<span class="circle-bullet"></span>',
			        	direction:"horisontal",
			        	space: 10,
			        	h_align: "center",
			        	v_align: "bottom",
			        	v_offset: 60
			        }
	            },
	            gridwidth:1140,
	            gridheight:700
	        });

	    }

		/* ---------------------------------------------------- */
        /*	Isotope												*/
        /* ---------------------------------------------------- */

		$( window ).on('load', function() {

		  	var $container = $('.isotope');
		    // filter buttons
		    $('#filters button').on('click', function(){
		    	var $this = $(this);
		        // don't proceed if already selected
		        if ( !$this.hasClass('is-checked') ) {
		          $this.parents('#options').find('.is-checked').removeClass('is-checked');
		          $this.addClass('is-checked');
		        }
				var selector = $this.attr('data-filter');
				$container.isotope({  itemSelector: '.item', filter: selector });
				return false;
		    });

		    $.mad_core.isotope();

		});

		/* ---------------------------------------------------- */
        /*	Element size										*/
        /* ---------------------------------------------------- */

		$(window).on("load resize",function(){

			var BoxeeBox = $('.tab-cont'); /* cache the selector */

		    $('.carousel-tabs').css({ 'height': BoxeeBox.outerHeight() });

		});

		/* ---------------------------------------------------- */
        /*	Tooltip									            */
        /* ---------------------------------------------------- */

		$(".qustion-icon").on('click',function(){

			$(this).parents(".qustion-tooltip").find(".tooltip").addClass('opened');

			return false;

	    });

	    $(".close-tooltip").on('click',function(){

		  $(this).parents(".tooltip").removeClass('opened');

		  return false;

	    });

		/* ---------------------------------------------------- */
        /*	Gallery carousel									*/
        /* ---------------------------------------------------- */

        var pageCarousel = $('.owl-carousel');

		if(pageCarousel.length){

			$('.owl-carousel').not('#thumbnails').each(function(){

				/* Max items counting */
				var max_items = $(this).data('max-items');
				var small_items = max_items;
				var tablet_items = max_items;
				var land_items = max_items;
				if(max_items > 1){
					small_items = max_items -1;
					tablet_items = max_items - 1;
					land_items = max_items;
				}
				if(max_items >= 4){
					land_items = max_items - 1;
					tablet_items = max_items -1;
					small_items = max_items - 2;
				}
				var mobile_items = 1;

				var autoplay_carousel = $(this).data('autoplay');

				var center_carousel = $(this).data('center');

				var item_margin = $(this).data('item-margin');

				/* Install Owl Carousel */
				$(this).owlCarousel({
				    smartSpeed : 450,
				    nav : true,
				    loop  : true,
				    autoplay : autoplay_carousel,
				    center: center_carousel,
				    autoplayTimeout: 3000,
				    navText : false,
				    margin: item_margin,
				    lazyLoad: true,
				    rtl: $.mad_core.SUPPORT.ISRTL ? true : false,
				    responsiveClass:true,
				    responsive : {
				        0:{
				            items:mobile_items
				        },
				        481:{
				            items:small_items
				        },
				        769:{
				            items:tablet_items
				        },
				        992:{
				            items:land_items
				        },
				        1400:{
				            items:max_items
				        }
				    }
				});

			});

			$('.custom-owl-prev').on('click',function(){

				$('.owl-carousel').trigger('prev.owl.carousel');

				return false;

			});

			$('.custom-owl-next').on('click',function(){

				$('.owl-carousel').trigger('next.owl.carousel');

				return false;

			});

			if($('#thumbnails').length){
				$('#thumbnails').each(function(){

					/* Max items counting */
					var data = $(this).data();
					var max_items = $(this).data('max-items');
					var tablet_items = max_items;
					if(max_items > 1){
						tablet_items = max_items - 1;
					}
					var mobile_items = 1;

					var autoplay_carousel = $(this).data('autoplay');

					$(this).owlCarousel({
						items : max_items,
						URLhashListener : false,
						navSpeed : 800,
						nav : true,
						loop : true,
						margin : 15,
						rtl: $.mad_core.SUPPORT.ISRTL ? true : false,
						navText:false,
						responsive : {
					        0:{
					            items:tablet_items
					        },
					        481:{
					            items:max_items
					        },
					        1200:{
					            items:max_items
					        }
					    }
				    });
				});

			}

		}

		/* ---------------------------------------------------- */
        /*	SmoothScroll										*/
        /* ---------------------------------------------------- */

		try {
			$.browserSelector();
			var $html = $('html');
			if ( $html.hasClass('chrome') || $html.hasClass('ie11') || $html.hasClass('ie10') ) {
				$.smoothScroll();
			}
		} catch(err) {}

		/* ---------------------------------------------------- */
        /*	Custom Select										*/
        /* ---------------------------------------------------- */

	   	$.MadCustomSelects({
		    target: '.auto-custom-select',
		    cssPrefix: 'auto-'
		});

		/* ---------------------------------------------------- */
        /*	Tabs												*/
        /* ---------------------------------------------------- */

        $(window).on("load",function(){

        	var tabs = $('.tabs-section');
			if(tabs.length){
				tabs.tabs({
					beforeActivate: function(event, ui) {
				        var hash = ui.newTab.children("li a").attr("href");
				   	},
					hide : {
						effect : "fadeOut",
						duration : 450
					},
					show : {
						effect : "fadeIn",
						duration : 450
					},
					updateHash : false
				});
			}

			$('ul.tabs-nav li').on('click',function(){

				var tab_id = $(this).attr('data-tab');

				$('.tab-cont').removeClass('current');
				$("#"+tab_id).addClass('current');

			});

			/* ------------------------------------------------
				Tabs - opacity
			------------------------------------------------ */

			var tabs = $('.mad-tabs');

			if(tabs.length){

				tabs.MadTabs({
					easing: 'easeOutQuint',
					speed: 600,
					cssPrefix: 'mad-'
				});

			}

			/* ------------------------------------------------
					End of Tabs
			------------------------------------------------ */

        });

		/* ---------------------------------------------------- */
        /*	Load more											*/
        /* ---------------------------------------------------- */

		$(".show-more").on( "click", function(){
	        $(this).closest("div").find(".other-items").toggleClass("show-section");
	        $(this).toggleClass("active");
	        $(this).text($(this).text() == 'Show All' ? 'Show Less' : 'Show All');
	        return false;
	    });

	    $("#loadmore").on( "click", function(){
	        $(".other-content").toggleClass("show-section");
	        $(this).toggleClass("active");
	        $(this).text($(this).text() == 'Show Full Review' ? 'Hide Full Review' : 'Show Full Review');
	        return false;
	    });

		/* ---------------------------------------------------- */
        /*	Sticky menu											*/
        /* ---------------------------------------------------- */

		$('body').Temp({
			sticky: true
		});

		/* ---------------------------------------------------- */
        /*	SmoothScroll										*/
        /* ---------------------------------------------------- */

		try {
			$.browserSelector();
			var $html = $('html');
			if ( $html.hasClass('chrome') || $html.hasClass('ie11') || $html.hasClass('ie10') ) {
				$.smoothScroll();
			}
		} catch(err) {}

		/* ------------------------------------------------
		Instagram Feed
		------------------------------------------------ */

	    if($('.instagram-feed').length){

	    	$('#instafeed').each(function(){

	    		var insta_items = $(this).data('instagram');

	    		var feed = new Instafeed({
			      target: 'instafeed',
			      tagName: 'living',
			      limit: insta_items,
			      get: 'user',
			      userId: '',
			      accessToken: '',
			      resolution: 'standard_resolution',
			      clientId: '',
			      template: '<li class="nv-instafeed-item"><a class="fancybox nv-lightbox" data-fancybox="instagram" href="{{image}}" title="{{location}}"><img src="{{image}}" /></a></li>',
			      after: function(){
			       $('#' + this.options.target).find('.fancybox').fancybox();
			      }
			    });

			    feed.run();

	    	});

	    }

	    /* ------------------------------------------------
		Close table product
		------------------------------------------------ */

	    $(".close-product").on('click',function(e){

		    e.preventDefault();
		    var id = $(this).attr('data-id');
		    $("div").each(function(){
		        if($(this).attr('data-id') == id) {
		            $(this).fadeOut("slow");
		        }
		    });

	    });

	    /* ------------------------------------------------
		Popup
		------------------------------------------------ */

		var popup_item = $(".popup-holder");

		if(popup_item.length){

			popup_item.fadeOut();

		    $('.closePopup').on('click', function() {
		      popup_item.fadeOut("slow");
		    });

		    $(document).mouseup(function (e) {

			    var container = $(".popup-holder");
			    if (container.has(e.target).length == 0){
			        container.fadeOut("slow");
			    }

			});

			var popup_btn =

			$('.map-button').on('click', function() {
		      $('.popup-map').fadeIn("slow");
		      return false;
		    });

		    $('.contact-button').on('click', function() {
		      $('.popup-contact').fadeIn("slow");
		      return false;
		    });

		    $('.calc-button').on('click', function() {
		      $('.popup-calc').fadeIn("slow");
		      return false;
		    });

		    $('.trade-button').on('click', function() {
		      $('.popup-trade').fadeIn("slow");
		      return false;
		    });

		}

		/* ------------------------------------------------
		Sticky sidebar
		------------------------------------------------ */

		$(window).on("load resize",function(){

			if ($(window).width() > 992) {

		        $('.content, .sidebar , #sidebar').theiaStickySidebar({
			      // Settings
			      additionalMarginTop: 30
			    });

		    }

		});

	    /* ------------------------------------------------
		Twitter Feed
		------------------------------------------------ */

	    if($("#twitter").length){

			var twitter_items = $(this).attr('data-twitter-items');

    		$('#twitter').tweet({

			    modpath: 'plugins/twitter/',
			    username: "maritim_1",
			    count: twitter_items,
			    loading_text: 'loading twitter feed...'
			    /* etc... */

			});

		}

		/* ---------------------------------------------------- */
        /*	Price Scale										    */
        /* ---------------------------------------------------- */

		/* ---------------------------------------------------- */
        /*	Accordion & Toggle									*/
        /* ---------------------------------------------------- */

		var aItem = $('.accordion:not(.toggle) .accordion-item'),
			link = aItem.find('.a-title'),
			$label = aItem.find('label'),
			aToggleItem = $('.accordion.toggle .accordion-item'),
			tLink = aToggleItem.find('.a-title');

			aItem.add(aToggleItem).children('.a-title').not('.active').next().hide();

		function triggerAccordeon($item) {
			$item
			.addClass('active')
			.next().stop().slideDown()
			.parent().siblings()
			.children('.a-title')
			.removeClass('active')
			.next().stop().slideUp();
		}


		if ($label.length) {
			$label.on('click',function(){
				triggerAccordeon($(this).closest('.a-title'))
			});
		} else {
			link.on('click',function(){
				triggerAccordeon($(this))
			});
		}

		tLink.on('click',function(){
			$(this).toggleClass('active')
			.next().stop().slideToggle();

		});

		/* ---------------------------------------------------- */
        /*	Quantity											*/
        /* ---------------------------------------------------- */

		var q = $('.quantity');

		q.each(function(){
			var $this = $(this),
				button = $this.children('button'),
				input = $this.children('input[type="text"]'),
				val = +input.val();

			button.on('click',function(){
				if($(this).hasClass('qty-minus')){
					if(val === 1) return false;
					input.val(--val);
				}
				else{
					input.val(++val);
				}
			});
		});

	    /* ---------------------------------------------------- */
		/*	Elevate zoom										*/
		/* ---------------------------------------------------- */

		if($('[data-zoom-image]').length){

			var button = $('.qv-preview');

			$("#zoom-image").elevateZoom({
				gallery:'thumbnails',
				galleryActiveClass: 'active',
				zoomType: "inner",
				cursor: "crosshair",
				responsive:true,
			    zoomWindowFadeIn: 500,
				zoomWindowFadeOut: 500,
				easing:true,
				lensFadeIn: 500,
				lensFadeOut: 500
			});

			button.on("click", function(e){
			  var ez = $('#zoom-image').data('elevateZoom');
				$("[data-fancybox]").fancybox(ez.getGalleryList());
			  	e.preventDefault();
			});

		}

		/* ---------------------------------------------------- */
		/*	Google Maps											*/
		/* ---------------------------------------------------- */

		if ($('#googleMap').length) {

			$(document).ready(function() {

				var myCenter = new google.maps.LatLng(17.433053, 78.412172);

				function loadMap() {
				  	var mapProp = {
					    center: myCenter,
					    zoom:12,
					    mapTypeId:google.maps.MapTypeId.ROADMAP

					};

					var map = document.getElementById('googleMap');

					if(map !== null){

				    	var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

					}

		            var marker = new google.maps.Marker({
		               position:myCenter,
		               map: map,
		               icon: '/static/home/images/map_marker.png'
		            });

		            marker.setMap(map);

		            //Zoom to 7 when clicked on marker
		            google.maps.event.addListener(marker,'click',function() {
		               map.setZoom(9);
		               map.setCenter(marker.getPosition());
		            });

				}
				google.maps.event.addDomListener(window, 'load', loadMap);

			});

		}

		if ($('#googleMap2').length) {

			$(document).ready(function() {

				function loadMap() {
				  	var mapProp = {
					    center: {lat: 51.503454, lng: -0.124755},
					    zoom:14,
					    mapTypeId:google.maps.MapTypeId.ROADMAP

					};

					var map = document.getElementById('googleMap2');

					if(map !== null){

				    	var map = new google.maps.Map(document.getElementById("googleMap2"),mapProp);

					}

		            setMarkers(map);

				}
				var marks = [
				  ['first', 51.521454,-0.124755],
				  ['second', 51.511454,-0.124755],
				  ['third', 51.521454,-0.134755],
				  ['forth', 51.495454,-0.125755],
				  ['fifth', 51.481454,-0.136755]
				];

	            function setMarkers(map) {

					for (var i = 0; i < marks.length; i++) {
						var mark = marks[i];
						var marker = new google.maps.Marker({
						  position: {lat: mark[1], lng: mark[2]},
						  map: map,
						  icon: '/static/home/images/map_marker.png',
						  title: mark[0],
						  zIndex: mark[3]
						});
					}

				}
				google.maps.event.addDomListener(window, 'load', loadMap);

			});

		}

		if ($('#googleMap3').length) {

			$(document).ready(function() {

				var myCenter = new google.maps.LatLng(17.433053, 78.412172);

				function loadMap() {
				  	var mapProp = {
					    center: myCenter,
					    zoom:12,
					    mapTypeId:google.maps.MapTypeId.ROADMAP

					};

					var map = document.getElementById('googleMap3');

					if(map !== null){

				    	var map = new google.maps.Map(document.getElementById("googleMap3"),mapProp);

					}

		            var marker = new google.maps.Marker({
		               position:myCenter,
		               map: map,
		               icon: '/static/home/images/map_marker.png'
		            });

		            marker.setMap(map);

		            //Zoom to 7 when clicked on marker
		            google.maps.event.addListener(marker,'click',function() {
		               map.setZoom(9);
		               map.setCenter(marker.getPosition());
		            });

				}
				google.maps.event.addDomListener(window, 'load', loadMap);

			});

		}

		/* ---------------------------------------------------- */
        /*	Newsletter											*/
        /* ---------------------------------------------------- */

	    var subscribe = $('[id^="newsletter"]');
	      subscribe.append('<div class="message-container-subscribe"></div>');
	      var message = $('.message-container-subscribe'),text;

	      subscribe.on('submit',function(e){
	        var self = $(this);

	        if(self.find('input[type="email"]').val() == ''){
	          text = "Please enter your e-mail!";
	          message.html('<div class="alert-box warning"><p>'+text+'</p></div>')
	            .slideDown()
	            .delay(4000)
	            .slideUp(function(){
	              $(this).html("");
	            });

	        }else{
	          self.find('span.error').hide();
	          $.ajax({
	            type: "POST",
	            url: "",
	            data: self.serialize(),
	            success: function(data){
	              if(data == '1'){
	                text = "Your email has been sent successfully!";
	                message.html('<div class="alert-box success"><p>'+text+'</p></div>')
	                  .slideDown()
	                  .delay(4000)
	                  .slideUp(function(){
	                    $(this).html("");
	                  })
	                  .prevAll('input[type="email"]').val("");
	              }else{
	                text = "Invalid email address!";
	                message.html('<div class="alert-box error"></i><p>'+text+'</p></div>')
	                  .slideDown()
	                  .delay(4000)
	                  .slideUp(function(){
	                    $(this).html("");
	                  });
	              }
	            }
	          });
	        }
	        e.preventDefault();
	    });

	    var subscribe = $('[id^="newsletter2"]');
	    subscribe.append('<div class="message-container-subscribe"></div>');
	    var message = $('.message-container-subscribe'),text;

	      subscribe.on('submit',function(e){
	        var self = $(this);

	        if(self.find('input[type="email"]').val() == ''){
	          text = "Please enter your e-mail!";
	          message.html('<div class="alert-box warning"><p>'+text+'</p></div>')
	            .slideDown()
	            .delay(4000)
	            .slideUp(function(){
	              $(this).html("");
	            });

	        }else{
	          self.find('span.error').hide();
	          $.ajax({
	            type: "POST",
	            url: "",
	            data: self.serialize(),
	            success: function(data){
	              if(data == '1'){
	                text = "Your email has been sent successfully!";
	                message.html('<div class="alert-box success"><p>'+text+'</p></div>')
	                  .slideDown()
	                  .delay(4000)
	                  .slideUp(function(){
	                    $(this).html("");
	                  })
	                  .prevAll('input[type="email"]').val("");
	              }else{
	                text = "Invalid email address!";
	                message.html('<div class="alert-box error"></i><p>'+text+'</p></div>')
	                  .slideDown()
	                  .delay(4000)
	                  .slideUp(function(){
	                    $(this).html("");
	                  });
	              }
	            }
	          });
	        }
	        e.preventDefault();
	    });

	    /* ---------------------------------------------------- */
        /*	Contact Form										*/
        /* ---------------------------------------------------- */

		if ($('#contact-form').length){

			var cf = $('#contact-form');
			cf.append('<div class="message-container"></div>');

			cf.on("submit",function(event){

				var self = $(this),text;

				var request = $.ajax({
					url:"",
					type : "post",
					data : self.serialize()
				});

				request.then(function(data){
					if(data == "1"){

						text = "Your message has been sent successfully!";

						cf.find('input:not([type="submit"]),textarea').val('');

						$('.message-container').html('<div class="alert-box success"><i class="icon-smile"></i><p>'+text+'</p></div>')
							.delay(150)
							.slideDown(300)
							.delay(4000)
							.slideUp(300,function(){
								$(this).html("");
							});

					}
					else{
						if(cf.find('textarea').val().length < 20){
							text = "Message must contain at least 20 characters!"
						}
						if(cf.find('input').val() == ""){
							text = "All required fields must be filled!";
						}
						$('.message-container').html('<div class="alert-box error"><i class="icon-warning"></i><p>'+text+'</p></div>')
							.delay(150)
							.slideDown(300)
							.delay(4000)
							.slideUp(300,function(){
								$(this).html("");
							});
					}
				},function(){
					$('.message-container').html('<div class="alert-box error"><i class="icon-warning"></i><p>Connection to server failed!</p></div>')
							.delay(150)
							.slideDown(300)
							.delay(4000)
							.slideUp(300,function(){
								$(this).html("");
							});
				});

				event.preventDefault();

			});

		}

	});

})(jQuery);
