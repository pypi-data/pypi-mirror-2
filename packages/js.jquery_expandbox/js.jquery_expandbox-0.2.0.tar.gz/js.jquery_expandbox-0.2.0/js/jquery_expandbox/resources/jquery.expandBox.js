/* jquery.expandBox v0.2.0
 * http://projects.stephane-klein.info/jquery.expandBox/
 *
 * Copyright 2010-2011, Stéphane Klein
 * Licensed under the LGPL version 3 (http://www.gnu.org/licenses/lgpl-3.0.txt).
 */
(function( $ ){
    $.fn.expandBoxHorizontally = function(parent, remove_px) {
        this.each(function() {
            $(this).css("width", null);
        });

        if (parent == undefined) {
            var parent = $(this.get(0)).parent().get(0);
        }
        var empty_space = $(parent).width() - 1;
        $($(this.get(0)).parent().get(0)).children().each(function() {
            if (window.getComputedStyle(this).getPropertyValue('position') != 'absolute')
                empty_space -= $(this).outerWidth();
        });
        var space_to_append = Math.floor(empty_space / this.length);
        if (remove_px != undefined)
            space_to_append -= remove_px;

        this.each(function() {
            $(this).css("width", ($(this).width() + space_to_append) + "px");
        });
    },
    $.fn.expandBoxVertically = function(parent, remove_px) {
        this.each(function() {
            $(this).css("height", null);
        });

        if (parent == undefined) {
            var parent = $(this.get(0)).parent().get(0);
        }
        var empty_space = $(parent).height() - 1;
        $($(this.get(0)).parent().get(0)).children().each(function() {
            if (window.getComputedStyle(this).getPropertyValue('position') != 'absolute')
                empty_space -= $(this).outerHeight();
        });
        var space_to_append = Math.floor(empty_space / this.length);
        if (remove_px != undefined)
            space_to_append -= remove_px;

        this.each(function() {
            $(this).css("height", ($(this).height() + space_to_append) + "px");
        });
    }
})( jQuery );

