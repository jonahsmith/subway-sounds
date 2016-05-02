// Once the DOM is ready...
$( document ).ready(function() {

  // Create the charts
  var surface_chart = createChart('surface-chart', 'surface level');
  var s_chart = createChart('s-chart', 'concourse level');
  var red_chart = createChart('red-chart', '1/2/3 track');
  var purple_chart = createChart('purple-chart', '7 track');

  // Connect to the view server's websocket
  var socket = new WebSocket('ws://localhost:6999');
  // Set the action for receiving a message to the update()
  socket.onmessage = update;

  // Main function for updating the text. Dispatches functions that update the
  // subsections.
  function update(message) {
    var up = JSON.parse(message['data']);
    update_surface(up['surface']);
    update_s(up['concourse']);
    update_red(up['1-2-3']);
    update_purple(up['7']);
  }

  // Function responsible for updating the 'surface' section
  function update_surface(readings) {
    updateChart(surface_chart, readings['current']['time'], readings['current']['value']);
  }

  // Function responsible for updating the 'concourse/S train' section
  function update_s(readings){
    updateChart(s_chart, readings['current']['time'], readings['current']['value']);
  }

  // Function responsible for updating the '1-2-3' section
  function update_red(readings) {
    updateChart(red_chart, readings['current']['time'], readings['current']['value']);
  }

  // Function responsible for updating the '7' section
  function update_purple(readings) {
    updateChart(purple_chart, readings['current']['time'], readings['current']['value']);
  }

  // Given the span ID and the replacement text, swap it out (if it's different)
  function updateText(id, replacementText) {
    if ($(id).text() != replacementText){
      $(id).fadeOut(function() { $(id).text(replacementText).fadeIn() });
    }
  }

  // Push a new value into a chart object (will automatically update the view)
  function updateChart(chartObject, datetime, value){
    // Remove the beginning once we've accumulated 3 mins of data
    while (chartObject.series[0].data.length > 36) {
      chartObject.series[0].removePoint(0);
    }
    // Convert to local timezone
    chartObject.series[0].addPoint([datetime*1000, value]);
  }
});
