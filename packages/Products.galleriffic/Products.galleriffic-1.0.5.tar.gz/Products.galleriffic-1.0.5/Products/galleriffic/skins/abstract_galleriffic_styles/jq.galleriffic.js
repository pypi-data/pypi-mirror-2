/**
 * jQuery Galleriffic plugin
 *
 * Copyright (c) 2008 Trent Foley (http://trentacular.com)
 * Licensed under the MIT License:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Much thanks to primary contributer Ponticlaro (http://www.ponticlaro.com)
 */
;(function($) {
	// Globally keep track of all images by their unique hash.  Each item is an image data object.
	var allImages = {};
	var imageCounter = 0;

	// Galleriffic static class
	$.galleriffic = {
		version: '2.0.1',

		// Strips invalid characters and any leading # characters
		normalizeHash: function(hash) {
			return hash.replace(/^.*#/, '').replace(/\?.*$/, '');
		},

		getImage: function(hash) {
			if (!hash)
				return undefined;

			hash = $.galleriffic.normalizeHash(hash);
			return allImages[hash];
		},

		// Global function that looks up an image by its hash and displays the image.
		// Returns false when an image is not found for the specified hash.
		// @param {String} hash This is the unique hash value assigned to an image.
		gotoImage: function(hash) {
			var imageData = $.galleriffic.getImage(hash);
			if (!imageData)
				return false;

			var gallery = imageData.gallery;
			gallery.gotoImage(imageData);
			
			return true;
		},

		// Removes an image from its respective gallery by its hash.
		// Returns false when an image is not found for the specified hash or the
		// specified owner gallery does match the located images gallery.
		// @param {String} hash This is the unique hash value assigned to an image.
		// @param {Object} ownerGallery (Optional) When supplied, the located images
		// gallery is verified to be the same as the specified owning gallery before
		// performing the remove operation.
		removeImageByHash: function(hash, ownerGallery) {
			var imageData = $.galleriffic.getImage(hash);
			if (!imageData)
				return false;

			var gallery = imageData.gallery;
			if (ownerGallery && ownerGallery != gallery)
				return false;

			return gallery.removeImageByIndex(imageData.index);
		}
	};

	var defaults = {
		delay:                     3000,
		numThumbs:                 20,
		preloadAhead:              40, // Set to -1 to preload all images
		enableTopPager:            false,
		enableBottomPager:         true,
		maxPagesToShow:            7,
		imageContainerSel:         '',
		viewCaption:               false, 
		captionContainerSel:       '',
		controlsContainerSel:      '',
		loadingContainerSel:       '',
		renderSSControls:          true,
		renderNavControls:         true,
		playLinkText:              'Play',
		pauseLinkText:             'Pause',
		prevLinkText:              'Previous',
		nextLinkText:              'Next',
		nextPageLinkText:          'Next &rsaquo;',
		prevPageLinkText:          '&lsaquo; Prev',
		enableHistory:             false,
		enableKeyboardNavigation:  true,
		autoStart:                 false,
		syncTransitions:           false,
		active_lightbox:           false,
		defaultTransitionDuration: 1000,
		onSlideChange:             undefined, // accepts a delegate like such: function(prevIndex, nextIndex) { ... }
		onTransitionOut:           undefined, // accepts a delegate like such: function(slide, caption, isSync, callback) { ... }
		onTransitionIn:            undefined, // accepts a delegate like such: function(slide, caption, isSync) { ... }
		onPageTransitionOut:       undefined, // accepts a delegate like such: function(callback) { ... }
		onPageTransitionIn:        undefined, // accepts a delegate like such: function() { ... }
		onImageAdded:              undefined, // accepts a delegate like such: function(imageData, $li) { ... }
		onImageRemoved:            undefined,  // accepts a delegate like such: function(imageData, $li) { ... }
	
	    // lightbox
        // Configuration related to overlay
		overlayBgColor: 		'#000',		// (string) Background color to overlay; inform a hexadecimal value like: #RRGGBB. Where RR, GG, and BB are the hexadecimal values for the red, green, and blue values of the color.
		overlayOpacity:			0.8,		// (integer) Opacity value to overlay; inform: 0.X. Where X are number from 0 to 9
		// Configuration related to navigation
		fixedNavigation:		false,		// (boolean) Boolean that informs if the navigation (next and prev button) will be fixed or not in the interface.
		// Configuration related to images
		imageLoading:			'lightbox-ico-loading.gif',		// (string) Path and the name of the loading icon
		imageBtnPrev:			'lightbox-btn-prev.gif',			// (string) Path and the name of the prev button image
		imageBtnNext:			'lightbox-btn-next.gif',			// (string) Path and the name of the next button image
		imageBtnClose:			'lightbox-btn-close.gif',		// (string) Path and the name of the close btn
		imageBlank:				'lightbox-blank.gif',			// (string) Path and the name of a blank image (one pixel)
		// Configuration related to container image box
		containerBorderSize:	10,			// (integer) If you adjust the padding in the CSS for the container, #lightbox-container-image-box, you will need to update this value
		containerResizeSpeed:	400,		// (integer) Specify the resize duration of container image. These number are miliseconds. 400 is default.
		// Configuration related to texts in caption. For example: Image 2 of 8. You can alter either "Image" and "of" texts.
		txtImage:				'Image',	// (string) Specify text "Image"
		txtOf:					'of',		// (string) Specify text "of"
		// Configuration related to keyboard navigation
		keyToClose:				'c',		// (string) (c = close) Letter to close the jQuery lightBox interface. Beyond this letter, the letter X and the SCAPE key is used to.
		keyToPrev:				'p',		// (string) (p = previous) Letter to show the previous image
		keyToNext:				'n',		// (string) (n = next) Letter to show the next image.
		// Don´t alter these variables in any way
		imageArray:				[],
		activeImage:			0
	};
    
    //lightbox service function
    /**
	 * Perfomance an effect in the image container resizing it
	 *
	 * @param integer intImageWidth The image´s width that will be showed
	 * @param integer intImageHeight The image´s height that will be showed
	 */
	function _resize_container_image_box (intImageWidth,intImageHeight) {
		// Get current width and height
		var intCurrentWidth = $('#lightbox-container-image-box').width();
		var intCurrentHeight = $('#lightbox-container-image-box').height();
		// Get the width and height of the selected image plus the padding
		var intWidth = (intImageWidth + (defaults.containerBorderSize * 2)); // Plus the image´s width and the left and right padding value
		var intHeight = (intImageHeight + (defaults.containerBorderSize * 2)); // Plus the image´s height and the left and right padding value
		// Diferences
		var intDiffW = intCurrentWidth - intWidth;
		var intDiffH = intCurrentHeight - intHeight;
		// Perfomance the effect
		$('#lightbox-container-image-box').animate({ width: intWidth, height: intHeight },defaults.containerResizeSpeed,function() { _show_image(); });
		if ( ( intDiffW == 0 ) && ( intDiffH == 0 ) ) {
			if ( $.browser.msie ) {
				___pause(250);
			} else {
				___pause(100);	
			}
		} 
		$('#lightbox-container-image-data-box').css({ width: intImageWidth });
		$('#lightbox-nav-btnPrev,#lightbox-nav-btnNext').css({ height: intImageHeight + (defaults.containerBorderSize * 2) });
	}
    
    /**
	 * Prepares image exibition; doing a image´s preloader to calculate it´s size
	 *
	 */
	function _set_image_to_view () {
		// Show the loading
		$('#lightbox-loading').show();
		if ( defaults.fixedNavigation ) {
			$('#lightbox-image,#lightbox-container-image-data-box,#lightbox-image-details-currentNumber').hide();
		} else {
			// Hide some elements
			$('#lightbox-image,#lightbox-nav,#lightbox-nav-btnPrev,#lightbox-nav-btnNext,#lightbox-container-image-data-box,#lightbox-image-details-currentNumber').hide();
		}
		// Image preload process
		var objImagePreloader = new Image();
		objImagePreloader.onload = function() {
			$('#lightbox-image').attr('src',defaults.imageArray[defaults.activeImage][0]);
			// Perfomance an effect in the image container resizing it
			_resize_container_image_box(objImagePreloader.width,objImagePreloader.height);
			//	clear onLoad, IE behaves irratically with animated gifs otherwise
			objImagePreloader.onload=function(){};
		};
		objImagePreloader.src = defaults.imageArray[defaults.activeImage][0];
	}
	
	/**
	 * Show the prepared image
	 *
	 */
	function _show_image () {
		$('#lightbox-loading').hide();
		$('#lightbox-image').fadeIn(function() {
			_show_image_data();
			_set_navigation();
		});
		_preload_neighbor_images();
	}

	/**
	 * Show the image information
	 *
	 */
	function _show_image_data () {
		$('#lightbox-container-image-data-box').slideDown('fast');
		$('#lightbox-image-details-caption').hide();
		if ( defaults.imageArray[defaults.activeImage][1] ) {
			$('#lightbox-image-details-caption').html(defaults.imageArray[defaults.activeImage][1]).show();
		}
		// If we have a image set, display 'Image X of X'
		if ( defaults.imageArray.length > 1 ) {
			$('#lightbox-image-details-currentNumber').html(defaults.txtImage + ' ' + ( defaults.activeImage + 1 ) + ' ' + defaults.txtOf + ' ' + defaults.imageArray.length).show();
		}		
	}

	// handles the reloaction of the URL hash variable when the previous/next buttons are clicked within the lightbox UI.
	function changeThumbnail (activeImg) {
		location.hash = '#'+(activeImg+1);
		//$.galleriffic.gallery.syncThumbs();
		// IE we need to explicity call goto
		/*if ($.browser.msie) {
			this.goto(activeImg);
		}*/
	}

	/**
	 * Display the button navigations
	 *
	 */
    function _set_navigation () {
		$('#lightbox-nav').show();

		// Instead to define this configuration in CSS file, we define here. And it´s need to IE. Just.
		$('#lightbox-nav-btnPrev,#lightbox-nav-btnNext').css({ 'background' : 'transparent url(' + defaults.imageBlank + ') no-repeat' });

		// Show the prev button, if not the first image in set
		if ( defaults.activeImage != 0 ) {
			if ( defaults.fixedNavigation ) {
				$('#lightbox-nav-btnPrev').css({ 'background' : 'url(' + defaults.imageBtnPrev + ') left 15% no-repeat' })
					.unbind()
					.bind('click',function(e) {
						defaults.activeImage = defaults.activeImage - 1;
                        changeThumbnail(defaults.activeImage);
						_set_image_to_view();
						return false;
					});
			} else {
				// Show the images button for Next buttons
				$('#lightbox-nav-btnPrev').unbind().hover(function() {
					$(this).css({ 'background' : 'url(' + defaults.imageBtnPrev + ') left 15% no-repeat' });
				},function() {
					$(this).css({ 'background' : 'transparent url(' + defaults.imageBlank + ') no-repeat' });
				}).show().bind('click',function(e) {
					defaults.activeImage = defaults.activeImage - 1;
                    changeThumbnail(defaults.activeImage);
					_set_image_to_view();
					return false;
				});
			}
		}

		// Show the next button, if not the last image in set
		if ( defaults.activeImage != ( defaults.imageArray.length -1 ) ) {
			if ( defaults.fixedNavigation ) {
				$('#lightbox-nav-btnNext').css({ 'background' : 'url(' + defaults.imageBtnNext + ') right 15% no-repeat' })
					.unbind()
					.bind('click',function(e) {
						defaults.activeImage = defaults.activeImage + 1;
                        changeThumbnail(defaults.activeImage);
						_set_image_to_view();
						return false;
					});
			} else {
				// Show the images button for Next buttons
				$('#lightbox-nav-btnNext').unbind().hover(function() {
					$(this).css({ 'background' : 'url(' + defaults.imageBtnNext + ') right 15% no-repeat' });
				},function() {
					$(this).css({ 'background' : 'transparent url(' + defaults.imageBlank + ') no-repeat' });
				}).show().bind('click',function(e) {
					defaults.activeImage = defaults.activeImage + 1;
					changeThumbnail(defaults.activeImage);
					_set_image_to_view();
					return false;
				});
			}
		}
		// Enable keyboard navigation
		_enable_keyboard_navigation();
	}

	/**
	 * Enable a support to keyboard navigation
	 *
	 */
	function _enable_keyboard_navigation () {
		$(document).keydown(function(objEvent) {
			_keyboard_action(objEvent);
		});
	}
	/**
	 * Disable the support to keyboard navigation
	 *
	 */
	function _disable_keyboard_navigation () {
		$(document).unbind();
	}

	/**
	 * Perform the keyboard actions
	 *
	 */
	function _keyboard_action (objEvent) {
		// To ie
		if ( objEvent == null ) {
			keycode = event.keyCode;
			escapeKey = 27;
		// To Mozilla
		} else {
			keycode = objEvent.keyCode;
			escapeKey = objEvent.DOM_VK_ESCAPE;
		}
		// Get the key in lower case form
		key = String.fromCharCode(keycode).toLowerCase();
		// Verify the keys to close the ligthBox
		if ( ( key == defaults.keyToClose ) || ( key == 'x' ) || ( keycode == escapeKey ) ) {
			_finish();
		}
		// Verify the key to show the previous image
		if ( ( key == defaults.keyToPrev ) || ( keycode == 37 ) ) {
			// If we´re not showing the first image, call the previous
			if ( defaults.activeImage != 0 ) {
				defaults.activeImage = defaults.activeImage - 1;
				changeThumbnail(defaults.activeImage);
				_set_image_to_view();
				_disable_keyboard_navigation();
			}
		}
		// Verify the key to show the next image
		if ( ( key == defaults.keyToNext ) || ( keycode == 39 ) ) {
			// If we´re not showing the last image, call the next
			if ( defaults.activeImage != ( defaults.imageArray.length - 1 ) ) {
				defaults.activeImage = defaults.activeImage + 1;
				changeThumbnail(defaults.activeImage);
				_set_image_to_view();
				_disable_keyboard_navigation();
			}
		}
	}
	
	/**
	 * Preload prev and next images being showed
	 *
	 */
	function _preload_neighbor_images () {
		if ( (defaults.imageArray.length -1) > defaults.activeImage ) {
			objNext = new Image();
			objNext.src = defaults.imageArray[defaults.activeImage + 1][0];
		}
		if ( defaults.activeImage > 0 ) {
			objPrev = new Image();
			objPrev.src = defaults.imageArray[defaults.activeImage -1][0];
		}
	}
	/**
	 * Remove jQuery lightBox plugin HTML markup
	 *
	 */
	function _finish () {
		$('#jquery-lightbox').remove();
		$('#jquery-overlay').fadeOut(function() { $('#jquery-overlay').remove(); });
		// Show some elements to avoid conflict with overlay in IE. These elements appear above the overlay.
		$('embed, object, select').css({ 'visibility' : 'visible' });
	}
	
	/**
	 / THIRD FUNCTION
	 * getPageSize() by quirksmode.com
	 *
	 * @return Array Return an array with page width, height and window width, height
	 */
	function ___getPageSize () {
		var xScroll, yScroll;
		if (window.innerHeight && window.scrollMaxY) {	
			xScroll = window.innerWidth + window.scrollMaxX;
			yScroll = window.innerHeight + window.scrollMaxY;
		} else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
			xScroll = document.body.scrollWidth;
			yScroll = document.body.scrollHeight;
		} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
			xScroll = document.body.offsetWidth;
			yScroll = document.body.offsetHeight;
		}
		var windowWidth, windowHeight;
		if (self.innerHeight) {	// all except Explorer
			if(document.documentElement.clientWidth){
				windowWidth = document.documentElement.clientWidth; 
			} else {
				windowWidth = self.innerWidth;
			}
			windowHeight = self.innerHeight;
		} else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
			windowWidth = document.documentElement.clientWidth;
			windowHeight = document.documentElement.clientHeight;
		} else if (document.body) { // other Explorers
			windowWidth = document.body.clientWidth;
			windowHeight = document.body.clientHeight;
		}	
		// for small pages with total height less then height of the viewport
		if(yScroll < windowHeight){
			pageHeight = windowHeight;
		} else { 
			pageHeight = yScroll;
		}
		// for small pages with total width less then width of the viewport
		if(xScroll < windowWidth){	
			pageWidth = xScroll;		
		} else {
			pageWidth = windowWidth;
		}
		arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight);
		return arrayPageSize;
	}
	
	/**
	 / THIRD FUNCTION
	 * getPageScroll() by quirksmode.com
	 *
	 * @return Array Return an array with x,y page scroll values.
	 */
	function ___getPageScroll () {
		var xScroll, yScroll;
		if (self.pageYOffset) {
			yScroll = self.pageYOffset;
			xScroll = self.pageXOffset;
		} else if (document.documentElement && document.documentElement.scrollTop) {	 // Explorer 6 Strict
			yScroll = document.documentElement.scrollTop;
			xScroll = document.documentElement.scrollLeft;
		} else if (document.body) {// all other Explorers
			yScroll = document.body.scrollTop;
			xScroll = document.body.scrollLeft;	
		}
		arrayPageScroll = new Array(xScroll,yScroll);
		return arrayPageScroll;
	}
    /**
    * Stop the code execution from a escified time in milisecond
    *
    */
    function ___pause (ms) {
        var date = new Date(); 
        curDate = null;
        do { var curDate = new Date(); }
        while ( curDate - date < ms);
    }
    // end ligthbox functions
    
	// Primary Galleriffic initialization function that should be called on the thumbnail container.
	$.fn.galleriffic = function(settings) {
		//  Extend Gallery Object
		$.extend(this, {
			// Returns the version of the script
			version: $.galleriffic.version,

			// Current state of the slideshow
			isSlideshowRunning: false,
			slideshowTimeout: undefined,

			// This function is attached to the click event of generated hyperlinks within the gallery
			clickHandler: function(e, link) {
				this.pause();

				if (!this.enableHistory ) {
					// The href attribute holds the unique hash for an image
					var hash = $.galleriffic.normalizeHash($(link).attr('href'));
					$.galleriffic.gotoImage(hash);
					e.preventDefault();
				}
			},
            
            // lightbox specific functions
            
            _set_interface: function () {
        		// Apply the HTML markup into body tag
        		$('body').append('<div id="jquery-overlay"></div><div id="jquery-lightbox"><div id="lightbox-container-image-box"><div id="lightbox-container-image"><img id="lightbox-image"><div style="" id="lightbox-nav"><a href="#" id="lightbox-nav-btnPrev"></a><a href="#" id="lightbox-nav-btnNext"></a></div><div id="lightbox-loading"><a href="#" id="lightbox-loading-link"><img src="' + defaults.imageLoading + '"></a></div></div></div><div id="lightbox-container-image-data-box"><div id="lightbox-container-image-data"><div id="lightbox-image-details"><span id="lightbox-image-details-caption"></span><span id="lightbox-image-details-currentNumber"></span></div><div id="lightbox-secNav"><a href="#" id="lightbox-secNav-btnClose"><img src="' + defaults.imageBtnClose + '"></a></div></div></div></div>');	
        		// Get page sizes
        		var arrPageSizes = ___getPageSize();
        		// Style overlay and show it
        		$('#jquery-overlay').css({
        			backgroundColor:	defaults.overlayBgColor,
        			opacity:			defaults.overlayOpacity,
        			width:				arrPageSizes[0],
        			height:				arrPageSizes[1]
        		}).fadeIn();
        		// Get page scroll
        		var arrPageScroll = ___getPageScroll();
        		// Calculate top and left offset for the jquery-lightbox div object and show it
        		$('#jquery-lightbox').css({
        			top:	arrPageScroll[1] + (arrPageSizes[3] / 10),
        			left:	arrPageScroll[0]
        		}).show();
        		// Assigning click events in elements to close overlay
        		$('#jquery-overlay,#jquery-lightbox').click(function() {
        			_finish();									
        		});
        		// Assign the _finish function to lightbox-loading-link and lightbox-secNav-btnClose objects
        		$('#lightbox-loading-link,#lightbox-secNav-btnClose').click(function() {
        			_finish();
        			return false;
        		});
        		// If window was resized, calculate the new overlay dimensions
        		$(window).resize(function() {
        			// Get page sizes
        			var arrPageSizes = ___getPageSize();
        			// Style overlay and show it
        			$('#jquery-overlay').css({
        				width:		arrPageSizes[0],
        				height:		arrPageSizes[1]
        			});
        			// Get page scroll
        			var arrPageScroll = ___getPageScroll();
        			// Calculate top and left offset for the jquery-lightbox div object and show it
        			$('#jquery-lightbox').css({
        				top:	arrPageScroll[1] + (arrPageSizes[3] / 10),
        				left:	arrPageScroll[0]
        			});
        		});
        	},
            
        	buildLightBox: function (image,current) {

        		this.pause();

                var current_image_src = this.data[current].slideUrl.replace('/image_preview', '/image_large');
        		// Hide some elements to avoid conflict with overlay in IE. These elements appear above the overlay.
        		$('embed, object, select').css({ 'visibility' : 'hidden' });
        		// Call the function to create the markup structure; style some elements; assign events in some elements.
        		this._set_interface();
        		// Unset total images in imageArray
        		defaults.imageArray.length = 0;
        		// Unset image active information
        		defaults.activeImage = 0;

        		if ( this.data.length == 1 ) {
        			defaults.imageArray.push(new Array(current_image_src,this.data[current].title));
        		} else {
        			// Add an Array (as many as we have), with href and title attributes, inside the Array that storage the images references		
        			for ( var i = 0; i < this.data.length; i++ ) {
        				defaults.imageArray.push(new Array(this.data[i].slideUrl.replace('/image_preview', '/image_large'),this.data[i].title));
        			}
        		}
        		while ( defaults.imageArray[defaults.activeImage][0] != current_image_src ) {
        			defaults.activeImage++;
        		}
        		// Call the function that prepares image exibition
        		_set_image_to_view();
        	},
        	
			// Appends an image to the end of the set of images.  Argument listItem can be either a jQuery DOM element or arbitrary html.
			// @param listItem Either a jQuery object or a string of html of the list item that is to be added to the gallery.
			appendImage: function(listItem) {
				this.addImage(listItem, false, false);
				return this;
			},

			// Inserts an image into the set of images.  Argument listItem can be either a jQuery DOM element or arbitrary html.
			// @param listItem Either a jQuery object or a string of html of the list item that is to be added to the gallery.
			// @param {Integer} position The index within the gallery where the item shouold be added.
			insertImage: function(listItem, position) {
				this.addImage(listItem, false, true, position);
				return this;
			},

			// Adds an image to the gallery and optionally inserts/appends it to the DOM (thumbExists)
			// @param listItem Either a jQuery object or a string of html of the list item that is to be added to the gallery.
			// @param {Boolean} thumbExists Specifies whether the thumbnail already exists in the DOM or if it needs to be added.
			// @param {Boolean} insert Specifies whether the the image is appended to the end or inserted into the gallery.
			// @param {Integer} position The index within the gallery where the item shouold be added.
			addImage: function(listItem, thumbExists, insert, position) {
				var $li = ( typeof listItem === "string" ) ? $(listItem) : listItem;				
				var $aThumb = $li.find('a.thumb');
				var slideUrl = $aThumb.attr('href');
				var title = $aThumb.attr('title');
				var $caption = $li.find('.caption').remove();
				var hash = $aThumb.attr('name');

				// Increment the image counter
				imageCounter++;

				// Autogenerate a hash value if none is present or if it is a duplicate
				if (!hash || allImages[''+hash]) {
					hash = imageCounter;
				}

				// Set position to end when not specified
				if (!insert)
					position = this.data.length;
				
				var imageData = {
					title:title,
					slideUrl:slideUrl,
					caption:$caption,
					hash:hash,
					gallery:this,
					index:position
				};

				// Add the imageData to this gallery's array of images
				if (insert) {
					this.data.splice(position, 0, imageData);

					// Reset index value on all imageData objects
					this.updateIndices(position);
				}
				else {
					this.data.push(imageData);
				}

				var gallery = this;

				// Add the element to the DOM
				if (!thumbExists) {
					// Update thumbs passing in addition post transition out handler
					this.updateThumbs(function() {
						var $thumbsUl = gallery.find('ul.thumbs');
						if (insert)
							$thumbsUl.children(':eq('+position+')').before($li);
						else
							$thumbsUl.append($li);
						
						if (gallery.onImageAdded)
							gallery.onImageAdded(imageData, $li);
					});
				}

				// Register the image globally
				allImages[''+hash] = imageData;

				// Setup attributes and click handler
				$aThumb.attr('rel', 'history')
					.attr('href', '#'+hash)
					.removeAttr('name')
					.click(function(e) {
						gallery.clickHandler(e, this);
					});

				return this;
			},

			// Removes an image from the gallery based on its index.
			// Returns false when the index is out of range.
			removeImageByIndex: function(index) {
				if (index < 0 || index >= this.data.length)
					return false;
				
				var imageData = this.data[index];
				if (!imageData)
					return false;
				
				this.removeImage(imageData);
				
				return true;
			},

			// Convenience method that simply calls the global removeImageByHash method.
			removeImageByHash: function(hash) {
				return $.galleriffic.removeImageByHash(hash, this);
			},

			// Removes an image from the gallery.
			removeImage: function(imageData) {
				var index = imageData.index;
				
				// Remove the image from the gallery data array
				this.data.splice(index, 1);
				
				// Remove the global registration
				delete allImages[''+imageData.hash];
				
				// Remove the image's list item from the DOM
				this.updateThumbs(function() {
					var $li = gallery.find('ul.thumbs')
						.children(':eq('+index+')')
						.remove();

					if (gallery.onImageRemoved)
						gallery.onImageRemoved(imageData, $li);
				});

				// Update each image objects index value
				this.updateIndices(index);

				return this;
			},

			// Updates the index values of the each of the images in the gallery after the specified index
			updateIndices: function(startIndex) {
				for (i = startIndex; i < this.data.length; i++) {
					this.data[i].index = i;
				}
				
				return this;
			},

			// Scraped the thumbnail container for thumbs and adds each to the gallery
			initializeThumbs: function() {
				this.data = [];
				var gallery = this;

				this.find('ul.thumbs > li').each(function(i) {
					gallery.addImage($(this), true, false);
				});

				return this;
			},

			isPreloadComplete: false,

			// Initalizes the image preloader
			preloadInit: function() {
				if (this.preloadAhead == 0) return this;
				
				this.preloadStartIndex = this.currentImage.index;
				var nextIndex = this.getNextIndex(this.preloadStartIndex);
				return this.preloadRecursive(this.preloadStartIndex, nextIndex);
			},

			// Changes the location in the gallery the preloader should work
			// @param {Integer} index The index of the image where the preloader should restart at.
			preloadRelocate: function(index) {
				// By changing this startIndex, the current preload script will restart
				this.preloadStartIndex = index;
				return this;
			},

			// Recursive function that performs the image preloading
			// @param {Integer} startIndex The index of the first image the current preloader started on.
			// @param {Integer} currentIndex The index of the current image to preload.
			preloadRecursive: function(startIndex, currentIndex) {
				// Check if startIndex has been relocated
				if (startIndex != this.preloadStartIndex) {
					var nextIndex = this.getNextIndex(this.preloadStartIndex);
					return this.preloadRecursive(this.preloadStartIndex, nextIndex);
				}

				var gallery = this;

				// Now check for preloadAhead count
				var preloadCount = currentIndex - startIndex;
				if (preloadCount < 0)
					preloadCount = this.data.length-1-startIndex+currentIndex;
				if (this.preloadAhead >= 0 && preloadCount > this.preloadAhead) {
					// Do this in order to keep checking for relocated start index
					setTimeout(function() { gallery.preloadRecursive(startIndex, currentIndex); }, 500);
					return this;
				}

				var imageData = this.data[currentIndex];
				if (!imageData)
					return this;

				// If already loaded, continue
				if (imageData.image)
					return this.preloadNext(startIndex, currentIndex); 
				
				// Preload the image
				var image = new Image();
				
				image.onload = function() {
					imageData.image = this;
					gallery.preloadNext(startIndex, currentIndex);
				};

				image.alt = imageData.title;
				image.src = imageData.slideUrl;

				return this;
			},
			
			// Called by preloadRecursive in order to preload the next image after the previous has loaded.
			// @param {Integer} startIndex The index of the first image the current preloader started on.
			// @param {Integer} currentIndex The index of the current image to preload.
			preloadNext: function(startIndex, currentIndex) {
				var nextIndex = this.getNextIndex(currentIndex);
				if (nextIndex == startIndex) {
					this.isPreloadComplete = true;
				} else {
					// Use setTimeout to free up thread
					var gallery = this;
					setTimeout(function() { gallery.preloadRecursive(startIndex, nextIndex); }, 100);
				}

				return this;
			},

			// Safe way to get the next image index relative to the current image.
			// If the current image is the last, returns 0
			getNextIndex: function(index) {
				var nextIndex = index+1;
				if (nextIndex >= this.data.length)
					nextIndex = 0;
				return nextIndex;
			},

			// Safe way to get the previous image index relative to the current image.
			// If the current image is the first, return the index of the last image in the gallery.
			getPrevIndex: function(index) {
				var prevIndex = index-1;
				if (prevIndex < 0)
					prevIndex = this.data.length-1;
				return prevIndex;
			},

			// Pauses the slideshow
			pause: function() {
				this.isSlideshowRunning = false;
				if (this.slideshowTimeout) {
					clearTimeout(this.slideshowTimeout);
					this.slideshowTimeout = undefined;
				}

				if (this.$controlsContainer) {
					this.$controlsContainer
						.find('div.ss-controls a').removeClass().addClass('play')
						.attr('title', this.playLinkText)
						.attr('href', '#play')
						.html(this.playLinkText);
				}
				
				return this;
			},

			// Plays the slideshow
			play: function() {
				this.isSlideshowRunning = true;

				if (this.$controlsContainer) {
					this.$controlsContainer
						.find('div.ss-controls a').removeClass().addClass('pause')
						.attr('title', this.pauseLinkText)
						.attr('href', '#pause')
						.html(this.pauseLinkText);
				}

				if (!this.slideshowTimeout) {
					var gallery = this;
					this.slideshowTimeout = setTimeout(function() { gallery.ssAdvance(); }, this.delay);
				}

				return this;
			},

			// Toggles the state of the slideshow (playing/paused)
			toggleSlideshow: function() {
				if (this.isSlideshowRunning)
					this.pause();
				else
					this.play();

				return this;
			},

			// Advances the slideshow to the next image and delegates navigation to the
			// history plugin when history is enabled
			// enableHistory is true
			ssAdvance: function() {
				if (this.isSlideshowRunning)
					this.next(true);

				return this;
			},

			// Advances the gallery to the next image.
			// @param {Boolean} dontPause Specifies whether to pause the slideshow.
			// @param {Boolean} bypassHistory Specifies whether to delegate navigation to the history plugin when history is enabled.  
			next: function(dontPause, bypassHistory) {
				this.gotoIndex(this.getNextIndex(this.currentImage.index), dontPause, bypassHistory);
				return this;
			},

			// Navigates to the previous image in the gallery.
			// @param {Boolean} dontPause Specifies whether to pause the slideshow.
			// @param {Boolean} bypassHistory Specifies whether to delegate navigation to the history plugin when history is enabled.
			previous: function(dontPause, bypassHistory) {
				this.gotoIndex(this.getPrevIndex(this.currentImage.index), dontPause, bypassHistory);
				return this;
			},

			// Navigates to the next page in the gallery.
			// @param {Boolean} dontPause Specifies whether to pause the slideshow.
			// @param {Boolean} bypassHistory Specifies whether to delegate navigation to the history plugin when history is enabled.
			nextPage: function(dontPause, bypassHistory) {
				var page = this.getCurrentPage();
				var lastPage = this.getNumPages() - 1;
				if (page < lastPage) {
					var startIndex = page * this.numThumbs;
					var nextPage = startIndex + this.numThumbs;
					this.gotoIndex(nextPage, dontPause, bypassHistory);
				}

				return this;
			},

			// Navigates to the previous page in the gallery.
			// @param {Boolean} dontPause Specifies whether to pause the slideshow.
			// @param {Boolean} bypassHistory Specifies whether to delegate navigation to the history plugin when history is enabled.
			previousPage: function(dontPause, bypassHistory) {
				var page = this.getCurrentPage();
				if (page > 0) {
					var startIndex = page * this.numThumbs;
					var prevPage = startIndex - this.numThumbs;				
					this.gotoIndex(prevPage, dontPause, bypassHistory);
				}
				
				return this;
			},

			// Navigates to the image at the specified index in the gallery
			// @param {Integer} index The index of the image in the gallery to display.
			// @param {Boolean} dontPause Specifies whether to pause the slideshow.
			// @param {Boolean} bypassHistory Specifies whether to delegate navigation to the history plugin when history is enabled.
			gotoIndex: function(index, dontPause, bypassHistory) {
				if (!dontPause)
					this.pause();
				
				if (index < 0) index = 0;
				else if (index >= this.data.length) index = this.data.length-1;
				
				var imageData = this.data[index];
				
				if (!bypassHistory && this.enableHistory)
					$.historyLoad(String(imageData.hash));  // At the moment, historyLoad only accepts string arguments
				else
					this.gotoImage(imageData);

				return this;
			},

			// This function is garaunteed to be called anytime a gallery slide changes.
			// @param {Object} imageData An object holding the image metadata of the image to navigate to.
			gotoImage: function(imageData) {
				var index = imageData.index;

				if (this.onSlideChange)
					this.onSlideChange(this.currentImage.index, index);
				
				this.currentImage = imageData;
				this.preloadRelocate(index);
				
				this.refresh();
				
				return this;
			},

			// Returns the default transition duration value.  The value is halved when not
			// performing a synchronized transition.
			// @param {Boolean} isSync Specifies whether the transitions are synchronized.
			getDefaultTransitionDuration: function(isSync) {
				if (isSync)
					return this.defaultTransitionDuration;
				return this.defaultTransitionDuration / 2;
			},

			// Rebuilds the slideshow image and controls and performs transitions
			refresh: function() {
				var imageData = this.currentImage;
				if (!imageData)
					return this;

				var index = imageData.index;

				// Update Controls
				if (this.$controlsContainer) {
					this.$controlsContainer
						.find('div.nav-controls a.prev').attr('href', '#'+this.data[this.getPrevIndex(index)].hash).end()
						.find('div.nav-controls a.next').attr('href', '#'+this.data[this.getNextIndex(index)].hash);
				}

				var previousSlide = this.$imageContainer.find('span.current').remove();
				var previousCaption = 0;

				if (this.$captionContainer) {
					previousCaption = this.$captionContainer.find('span.current').remove();
				}

				// Perform transitions simultaneously if syncTransitions is true and the next image is already preloaded
				var isSync = this.syncTransitions && imageData.image;

				// Flag we are transitioning
				var isTransitioning = true;
				var gallery = this;

				var transitionOutCallback = function() {
					// Flag that the transition has completed
					isTransitioning = false;

					// Remove the old slide
					previousSlide.remove();

					// Remove old caption
					if (previousCaption)
						previousCaption.remove();

					if (!isSync) {
						if (imageData.image && imageData.hash == gallery.data[gallery.currentImage.index].hash) {
							gallery.buildImage(imageData, isSync);
						} else {
							// Show loading container
							if (gallery.$loadingContainer) {
								gallery.$loadingContainer.show();
							}
						}
					}
				};

				if (previousSlide.length == 0) {
					// For the first slide, the previous slide will be empty, so we will call the callback immediately
					transitionOutCallback();
				} else {
					if (this.onTransitionOut) {
						this.onTransitionOut(previousSlide, previousCaption, isSync, transitionOutCallback);
					} else {
						previousSlide.fadeTo(this.getDefaultTransitionDuration(isSync), 0.0, transitionOutCallback);
						if (previousCaption)
							previousCaption.fadeTo(this.getDefaultTransitionDuration(isSync), 0.0);
					}
				}

				// Go ahead and begin transitioning in of next image
				if (isSync)
					this.buildImage(imageData, isSync);

				if (!imageData.image) {
					var image = new Image();
					
					// Wire up mainImage onload event
					image.onload = function() {
						imageData.image = this;

						// Only build image if the out transition has completed and we are still on the same image hash
						if (!isTransitioning && imageData.hash == gallery.data[gallery.currentImage.index].hash) {
							gallery.buildImage(imageData, isSync);
						}
					};

					// set alt and src
					image.alt = imageData.title;
					image.src = imageData.slideUrl;
				}

				// This causes the preloader (if still running) to relocate out from the currentIndex
				this.relocatePreload = true;

				return this.syncThumbs();
			},

			// Called by the refresh method after the previous image has been transitioned out or at the same time
			// as the out transition when performing a synchronous transition.
			// @param {Object} imageData An object holding the image metadata of the image to build.
			// @param {Boolean} isSync Specifies whether the transitions are synchronized.
			buildImage: function(imageData, isSync) {
				var gallery = this;
				var nextIndex = this.getNextIndex(imageData.index);

				// Construct new hidden span for the image
				var newSlide = this.$imageContainer;
				if (gallery.active_lightbox){
				    newSlide.empty().append('<span class="image-wrapper"><a class="advance-link" rel="history" title="'+imageData.image.alt+'"></a></span>');
				}else{
					newSlide.empty().append('<span class="image-wrapper current"><a class="advance-link" rel="history" href="#'+this.data[nextIndex].hash+'" title="'+imageData.title+'">&nbsp;</a></span>');
				}
				newSlide.find('a')
					.append(imageData.image)
					.click(function(e) {
					    if (gallery.active_lightbox){
        				    gallery.buildLightBox(imageData.image, imageData.index);
        				}
        				else{
						    gallery.clickHandler(e, this);
						}
					});

				var newCaption = 0;
				if (this.$captionContainer) {
					// Construct new hidden caption for the image
					newCaption = this.$captionContainer
						.append('<span class="image-caption current"></span>')
						.find('span.current').css('opacity', '0')
						.append(imageData.caption);
				}

				// Hide the loading conatiner
				if (this.$loadingContainer) {
					this.$loadingContainer.hide();
				}

				// Transition in the new image
				if (this.onTransitionIn) {
					this.onTransitionIn(newSlide, newCaption, isSync);
				} else {
					newSlide.fadeTo(this.getDefaultTransitionDuration(isSync), 1.0);
					if (newCaption)
						newCaption.fadeTo(this.getDefaultTransitionDuration(isSync), 1.0);
				}
				
				if (this.isSlideshowRunning) {
					if (this.slideshowTimeout)
						clearTimeout(this.slideshowTimeout);

					this.slideshowTimeout = setTimeout(function() { gallery.ssAdvance(); }, this.delay);
				}

				return this;
			},

			// Returns the current page index that should be shown for the currentImage
			getCurrentPage: function() {
				return Math.floor(this.currentImage.index / this.numThumbs);
			},

			// Applies the selected class to the current image's corresponding thumbnail.
			// Also checks if the current page has changed and updates the displayed page of thumbnails if necessary.
			syncThumbs: function() {
				var page = this.getCurrentPage();
				if (page != this.displayedPage)
					this.updateThumbs();

				// Remove existing selected class and add selected class to new thumb
				var $thumbs = this.find('ul.thumbs').children();
				$thumbs.filter('.selected').removeClass('selected');
				$thumbs.eq(this.currentImage.index).addClass('selected');

				return this;
			},

			// Performs transitions on the thumbnails container and updates the set of
			// thumbnails that are to be displayed and the navigation controls.
			// @param {Delegate} postTransitionOutHandler An optional delegate that is called after
			// the thumbnails container has transitioned out and before the thumbnails are rebuilt.
			updateThumbs: function(postTransitionOutHandler) {
				var gallery = this;
				var transitionOutCallback = function() {
					// Call the Post-transition Out Handler
					if (postTransitionOutHandler)
						postTransitionOutHandler();
					
					gallery.rebuildThumbs();

					// Transition In the thumbsContainer
					if (gallery.onPageTransitionIn)
						gallery.onPageTransitionIn();
					else
						gallery.show();
				};

				// Transition Out the thumbsContainer
				if (this.onPageTransitionOut) {
					this.onPageTransitionOut(transitionOutCallback);
				} else {
					this.hide();
					transitionOutCallback();
				}

				return this;
			},

			// Updates the set of thumbnails that are to be displayed and the navigation controls.
			rebuildThumbs: function() {
				var needsPagination = this.data.length > this.numThumbs;

				// Rebuild top pager
				if (this.enableTopPager) {
					var $topPager = this.find('div.top');
					if ($topPager.length == 0)
						$topPager = this.prepend('<div class="top pagination"></div>').find('div.top');
					else
						$topPager.empty();

					if (needsPagination)
						this.buildPager($topPager);
				}

				// Rebuild bottom pager
				if (this.enableBottomPager) {
					var $bottomPager = this.find('div.bottom');
					if ($bottomPager.length == 0)
						$bottomPager = this.append('<div class="bottom pagination"></div>').find('div.bottom');
					else
						$bottomPager.empty();

					if (needsPagination)
						this.buildPager($bottomPager);
				}

				var page = this.getCurrentPage();
				var startIndex = page*this.numThumbs;
				var stopIndex = startIndex+this.numThumbs-1;
				if (stopIndex >= this.data.length)
					stopIndex = this.data.length-1;

				// Show/Hide thumbs
				var $thumbsUl = this.find('ul.thumbs');
				$thumbsUl.find('li').each(function(i) {
					var $li = $(this);
					if (i >= startIndex && i <= stopIndex) {
						$li.show();
					} else {
						$li.hide();
					}
				});

				this.displayedPage = page;

				// Remove the noscript class from the thumbs container ul
				$thumbsUl.removeClass('noscript');
				
				return this;
			},

			// Returns the total number of pages required to display all the thumbnails.
			getNumPages: function() {
				return Math.ceil(this.data.length/this.numThumbs);
			},

			// Rebuilds the pager control in the specified matched element.
			// @param {jQuery} pager A jQuery element set matching the particular pager to be rebuilt.
			buildPager: function(pager) {
				var gallery = this;
				var numPages = this.getNumPages();
				var page = this.getCurrentPage();
				var startIndex = page * this.numThumbs;
				var pagesRemaining = this.maxPagesToShow - 1;
				
				var pageNum = page - Math.floor((this.maxPagesToShow - 1) / 2) + 1;
				if (pageNum > 0) {
					var remainingPageCount = numPages - pageNum;
					if (remainingPageCount < pagesRemaining) {
						pageNum = pageNum - (pagesRemaining - remainingPageCount);
					}
				}

				if (pageNum < 0) {
					pageNum = 0;
				}

				// Prev Page Link
				if (page > 0) {
					var prevPage = startIndex - this.numThumbs;
					pager.append('<a rel="history" href="#'+this.data[prevPage].hash+'" title="'+this.prevPageLinkText+'">'+this.prevPageLinkText+'</a>');
				}

				// Create First Page link if needed
				if (pageNum > 0) {
					this.buildPageLink(pager, 0, numPages);
					if (pageNum > 1)
						pager.append('<span class="ellipsis">&hellip;</span>');
					
					pagesRemaining--;
				}

				// Page Index Links
				while (pagesRemaining > 0) {
					this.buildPageLink(pager, pageNum, numPages);
					pagesRemaining--;
					pageNum++;
				}

				// Create Last Page link if needed
				if (pageNum < numPages) {
					var lastPageNum = numPages - 1;
					if (pageNum < lastPageNum)
						pager.append('<span class="ellipsis">&hellip;</span>');

					this.buildPageLink(pager, lastPageNum, numPages);
				}

				// Next Page Link
				var nextPage = startIndex + this.numThumbs;
				if (nextPage < this.data.length) {
					pager.append('<a rel="history" href="#'+this.data[nextPage].hash+'" title="'+this.nextPageLinkText+'">'+this.nextPageLinkText+'</a>');
				}

				pager.find('a').click(function(e) {
					gallery.clickHandler(e, this);
				});

				return this;
			},

			// Builds a single page link within a pager.  This function is called by buildPager
			// @param {jQuery} pager A jQuery element set matching the particular pager to be rebuilt.
			// @param {Integer} pageNum The page number of the page link to build.
			// @param {Integer} numPages The total number of pages required to display all thumbnails.
			buildPageLink: function(pager, pageNum, numPages) {
				var pageLabel = pageNum + 1;
				var currentPage = this.getCurrentPage();
				if (pageNum == currentPage)
					pager.append('<span class="current">'+pageLabel+'</span>');
				else if (pageNum < numPages) {
					var imageIndex = pageNum*this.numThumbs;
					pager.append('<a rel="history" href="#'+this.data[imageIndex].hash+'" title="'+pageLabel+'">'+pageLabel+'</a>');
				}
				
				return this;
			}
		});

		// Now initialize the gallery
		$.extend(this, defaults, settings);
		
		// Verify the history plugin is available
		if (this.enableHistory && !$.historyInit)
			this.enableHistory = false;
		
		// Select containers
		if (this.imageContainerSel) this.$imageContainer = $(this.imageContainerSel);
		this.$captionContainer = null;
		if (this.captionContainerSel && this.viewCaption) this.$captionContainer = $(this.captionContainerSel);
		if (this.loadingContainerSel) this.$loadingContainer = $(this.loadingContainerSel);

		// Initialize the thumbails
		this.initializeThumbs();
		
		if (this.maxPagesToShow < 3)
			this.maxPagesToShow = 3;

		this.displayedPage = -1;
		this.currentImage = this.data[0];
		var gallery = this;

		// Hide the loadingContainer
		if (this.$loadingContainer)
			this.$loadingContainer.hide();

		// Setup controls
		if (this.controlsContainerSel) {
			this.$controlsContainer = $(this.controlsContainerSel).empty();
			
			if (this.renderSSControls) {
				if (this.autoStart) {
					this.$controlsContainer
						.append('<div class="ss-controls"><a href="#pause" class="pause" title="'+this.pauseLinkText+'">'+this.pauseLinkText+'</a></div>');
				} else {
					this.$controlsContainer
						.append('<div class="ss-controls"><a href="#play" class="play" title="'+this.playLinkText+'">'+this.playLinkText+'</a></div>');
				}

				this.$controlsContainer.find('div.ss-controls a')
					.click(function(e) {
						gallery.toggleSlideshow();
						e.preventDefault();
						return false;
					});
			}
		
			if (this.renderNavControls) {
				this.$controlsContainer
					.append('<div class="nav-controls"><a class="prev" rel="history" title="'+this.prevLinkText+'">'+this.prevLinkText+'</a><a class="next" rel="history" title="'+this.nextLinkText+'">'+this.nextLinkText+'</a></div>')
					.find('div.nav-controls a')
					.click(function(e) {
						gallery.clickHandler(e, this);
					});
			}
		}

		var initFirstImage = !this.enableHistory || !location.hash;
		if (this.enableHistory && location.hash) {
			var hash = $.galleriffic.normalizeHash(location.hash);
			var imageData = allImages[hash];
			if (!imageData)
				initFirstImage = true;
		}

		// Setup gallery to show the first image
		if (initFirstImage)
			this.gotoIndex(0, false, true);

		// Setup Keyboard Navigation
		if (this.enableKeyboardNavigation) {
			$(document).keydown(function(e) {
				var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
				switch(key) {
					case 32: // space
						gallery.next();
						e.preventDefault();
						break;
					case 33: // Page Up
						gallery.previousPage();
						e.preventDefault();
						break;
					case 34: // Page Down
						gallery.nextPage();
						e.preventDefault();
						break;
					case 35: // End
						gallery.gotoIndex(gallery.data.length-1);
						e.preventDefault();
						break;
					case 36: // Home
						gallery.gotoIndex(0);
						e.preventDefault();
						break;
					case 37: // left arrow
						gallery.previous();
						e.preventDefault();
						break;
					case 39: // right arrow
						gallery.next();
						e.preventDefault();
						break;
				}
			});
		}

		// Auto start the slideshow
		if (this.autoStart)
			this.play();

		// Kickoff Image Preloader after 1 second
		setTimeout(function() { gallery.preloadInit(); }, 1000);

		return this;
	};
})(jQuery);
