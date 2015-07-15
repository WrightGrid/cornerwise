define(["underscore", "jquery"], function(_, $) {

    $.fn.transition = function(klFrom, klActive, klFinal) {
        var self = this;
        this.addClass(klFrom);
        this.one("animationend", function(e) {
            console.log(this);
            self.removeClass(klFrom).removeClass(klActive);
            if (klFinal)
                self.addClass(klFinal);
        });
        this.addClass(klActive);
    };

    $.fn.animateAddClass = function(klBase) {
        this.classTransition(klBase + "-enter",
                             klBase + "-active");
    };

    var defaultHelpers = {
        formatDate: function(d) {
            return (d.toLocaleDateString) ?
                d.toLocaleDateString() :
                d.toString().slice(0, 15);
        }
    };

    return {
        everyPred: function(fs, arg) {
            return _.every(fs, function(f) {
                return f(arg);
            });
        },

        promiseLocation: function() {
            var promise = $.Deferred();

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(pos) {
                        var coords = pos.coords;
                        promise.resolve([coords.latitude,
                                         coords.longitude,
                                         coords.altitude]);
                    },
                    function() {
                        promise.reject({reason: "Permission denied"});
                    });
            } else {
                promise.reject({reason: "Geolocation unavailable in this browser."});
            }

            return promise;
        },

        mToFeet: function(m) {
            return m*3.281;
        },

        feetToM: function(ft) {
            return ft/3.281;
        },

        mToMiles: function(m) {
            return m*3.281/5280;
        },

        /**
         * Like _.template, except that it adds helper functions to the
         * data passed to the resulting template function.
         */
        template: function(templateString, helpers) {
            helpers = helpers || defaultHelpers;

            var temp = _.template(templateString);

            return function(data) {
                return temp(_.extend(data, helpers));
            };
        }
    };
});
