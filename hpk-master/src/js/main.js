//
// main.js: Entry-point script for pages on hpk.io

// Simple, global, tme-keeping logging object
window.global_timer = {
  origin: performance.now(),
  log: function (message) {
    console.log("[AT " + (performance.now() - global_timer.origin).toFixed(4) +
                "ms]: " + message);
  },
}
global_timer.log("Initialised global_timer at " + global_timer.origin);

// Import styles and scripts
import '../sass/styles.sass';

import $ from 'jquery';
import { Foundation } from './base.js';

// Initialise JavaScript components
Foundation.addToJquery($);
global_timer.log('Finished importing components in main.js');

$(document).ready(function () {
    $(document).foundation();
    global_timer.log("Foundation initialised on the DOM");
});
global_timer.log("Finished loading main.js");

// end main.js
