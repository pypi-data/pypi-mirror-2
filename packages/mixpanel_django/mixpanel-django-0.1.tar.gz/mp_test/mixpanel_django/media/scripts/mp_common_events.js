// common event functions start here
var trackMixpanelEvent = function() {
    var null_fn = function() {
    };

    switch (arguments.length) {
        case 2:
            var event_name = arguments[0];
            var event_data = arguments[1];
            var event_callback = null_fn;
            break;
        case 3:
            var event_name = arguments[0];
            var event_data = arguments[1];
            var event_callback = arguments[2];
            break;
        default:
            throw 'mixpanel args error';
    }

    switch (MP_LOAD_TYPE) {
        case 'async':
            mpq.push(['track', event_name, event_data]);
            break;
        case 'standard':
            mpmetrics.track(event_name, event_data, event_callback);
            break;
        case 'fbml':
            mpmetrics.track(event_name, event_data);
            break;
        default:
            throw 'mixpanel type error';
    }
};

var trackfunnelMixpanelEvent = function() {
    var null_fn = function() {
    };
    switch (arguments.length) {
        case 4:
            var funnel_name = arguments[0];
            var funnel_step = arguments[1];
            var funnel_goal = arguments[2];
            var funnel_data = arguments[3];
            var funnel_callback = null_fn;
            break;
        case 5:
            var funnel_name = arguments[0];
            var funnel_step = arguments[1];
            var funnel_goal = arguments[2];
            var funnel_data = arguments[3];
            var funnel_callback = arguments[4];
            break;
        default:
            throw 'mixpanel args error';
    }

    switch (MP_LOAD_TYPE) {
        case 'async':
            mpq.push(['track_funnel', funnel_name, funnel_step,
                funnel_goal, funnel_data]);
            break;
        case 'standard':
            mpmetrics.track_funnel(funnel_name, funnel_step,
                funnel_goal, funnel_data, funnel_callback);
            break;
        case 'fbml':
            mpmetrics.track_funnel(funnel_name, funnel_step,
                funnel_goal, funnel_data);
            break;
        default:
            throw 'mixpanel type error';
    }
};


