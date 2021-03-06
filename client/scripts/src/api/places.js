define(["jquery"], function($) {
    var places = $.Deferred();
    if (window.google && google.maps) {
        places.resolve(google.maps.places);
    } else {
        window._onPlacesReady = function() {
            places.resolve(google.maps.places);
        };
    }

    var module = {
        shortAddress: function(place) {
            var pieces = place.address_components;

            return [pieces[0].short_name,
                    pieces[1].short_name].join(" ");
        },

        /**
         * @param {HTMLElement} input
         * @param {google.maps.places.AutocompleteOptions} options
         *
         * @return {$.Deferred} Resolves to the new Autocomplete instance
         *
         * Set up the specified input as a Places autocomplete box when the
         * Places API becomes available.
         */
        setup: function(input, options) {
            var autocomplete = $.Deferred();
            places.done(function(api) {
                autocomplete.resolve(new api.Autocomplete(input, options));
            });

            return autocomplete;
        }
    };

    return module;
});
