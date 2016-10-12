require.config({
    paths: {
        // Dependencies:
        "underscore": "lib/underscore-min",
        "backbone": "lib/backbone",
        "leaflet": "//cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/leaflet",
        "jquery": "//code.jquery.com/jquery-1.11.3.min",
        "chartjs": "//cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.min",

        // Utilities:
        "utils": "src/utils",
        "locale": "src/localization",

        // APIs:
        "arcgis": "src/api/arcgis",
        "places": "src/api/places",

        // Application: //
        "config": "src/config",
        "local-config": "src/localConfig",
        "app-state": "src/appState",
        "ref-location": "src/refLocation",

        // Leaflet stuff:
        "ref-marker": "src/leaflet/refMarker",
        "proposal-marker": "src/leaflet/proposalMarker",
        "info-layer-helper": "src/leaflet/infoLayer",

        // Backbone Models:
        "proposal": "src/model/proposal",
        "layer": "src/model/layer",
        "project": "src/model/project",

        // Backbone Collections:
        "selectable": "src/collection/selectableCollection",
        "proposals": "src/collection/proposals",
        "layers": "src/collection/layers",
        "regions": "src/collection/regions",
        "projects": "src/collection/projects",
        "collection-manager": "src/collection/collectionManager",

        "alerts": "src/view/alerts",

        // Backbone Views:
        // Generic:
        "modal-view": "src/view/modalView",

        // Application-specific:
        "proposal-view": "src/view/proposal",
        "map-view": "src/view/map",
        "proposal-info-view": "src/view/proposalInfo",
        "projects-summary-view": "src/view/projectsSummary",
        "layers-view": "src/view/layers",
        "filters-view": "src/view/filters",
        "subscribe-view": "src/view/subscribe",
        "info-view": "src/view/infoView",
        "list-view": "src/view/list",
        "image-view": "src/view/image",

        // View managers:
        "view-manager": "src/viewManager",

        // Additional features:
        "budget": "src/view/budget",
        "glossary": "src/glossary",
        "legal-notice": "src/legalNotice",

        "setup": "src/setup"
    },

    shim: {
        "leaflet": {
            exports: "L"
        }
    }
});

require(["setup"], function(setup) {
    window.app = setup.start();
});
