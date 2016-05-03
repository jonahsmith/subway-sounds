// Once the DOM is ready...
$( document ).ready(function() {

  function initializeIntro(){
    var d = new Date();
    var h = d.toLocaleString('en-EN', {hour: '2-digit', hour12: false, timeZone: 'America/New_York'});

    if (h > 21 && h < 0){
      $('#0-1').text("Throngs of people mill around the entrance – or exit – to the subway station, taking in the bright, symbolic lights of Times Square. The characters that previously graced the streets and posed for photographs – be it the superheroes or Disney characters – have retired for the day, but in the city that never sleeps, this is but a small setback in the ‘party station.’");
    } else if (h >= 0 && h < 10) {
      $('#0-1').text('0-1', "The crowds have died down, but Times Square’s bright lights shine on. The station is mostly deserted at this hour, but in a few hours, it will transform into a chaotic hub of activity — it is, after all, the “party station.”");
    } else if (h >= 10 && h <= 21){
      $('#0-1').text("Throngs of people mill around the station entrance, some rummaging in their bags for their MetroCards while others go about their business with practiced ease. Some swipe too slowly. Some will have to swipe again at this turnstile. Just outside, a motley assortment of costumed characters amble down the streets, providing even more spectacle for awestruck tourists as locals shove past, resigned to the “party station” that is Times Square.");
    }
  }

  initializeIntro();

  // Create the charts
  // var surface_chart = createChart('surface-chart', 'surface level');
  // var s_chart = createChart('s-chart', 'concourse level');
  // var red_chart = createChart('red-chart', '1/2/3 track');
  // var purple_chart = createChart('purple-chart', '7 track');

  // Connect to the view server's websocket
  var socket = new WebSocket('ws://localhost:6999');
  // Set the action for receiving a message to the update()
  socket.onmessage = update;

  // Main function for updating the text. Dispatches functions that update the
  // subsections.
  function update(message) {
    var up = JSON.parse(message['data']);
    update_surface(up);
    update_s(up);
    update_red(up);
    update_purple(up);
  }

  function comparison(level){
    if (level > 145) {
      return 'the thumping of a boom car';
    } else if (level > 140) {
      return 'the roar of a jet engine nearby'
    } else if (level > 130) {
      return 'the roar of a jet taking off 100-200 feet away';
    } else if (level > 120) {
      return 'the earth-shaking rumble of a thunderclap';
    } else if (level > 110) {
      return 'the smacking of a jackhammer';
    } else if (level > 105) {
      return 'the revving of a snowmobile';
    } else if (level > 103) {
      return 'the rumble of a jet flying 1000 feet overhead';
    } else if (level > 100) {
      return 'the grinding of a cement mixer';
    } else if (level > 97) {
      return 'the whirring of a newspaper press';
    } else if (level > 88) {
      return 'the revving of a motorcycle';
    } else if (level > 84) {
      return 'the whining of a diesel truck';
    } else if (level > 80) {
      return 'a whirring of a garbage disposal';
    } else if (level > 78) {
      return 'the swishing of a washing machine'
    } else if (level > 70) {
      return 'the whoosing of a vacuum cleaner';
    } else if (level > 60) {
      return 'the chitter-chatter of a normal conversation';
    } else if (level > 50) {
      return 'the awkwardness of a quiet office';
    } else {
      return 'the silence of something very quiet';
    }

  }

  function clockTime(timestamp){
    return new Date(timestamp).toLocaleString('en-EN', {hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'America/New_York'});
  }

  // Function responsible for updating the 'surface' section
  function update_surface(newData) {
    var readings = newData['surface'];
    // updateChart(surface_chart, readings['current']['time'], readings['current']['value']);

    var yesterday = (readings['yest_trough']['value'] != 999) ? true : false;

    if (Math.abs(readings['current']['value'] - readings['today_peak']['value']) < 2) {
        $('#0-2').text("The sound levels are at " + readings['current']['value'] + " dB, which is close to the peak for today.");
        if (yesterday) {
          if (readings['yest_peak']['value'] > readings['current']['value']){
            larger_smaller = 'not as loud as';
          } else if (readings['yest_peak']['value'] < readings['current']['value']){
            larger_smaller = 'louder than';
          } else {
            larger_smaller = 'as loud as';
          }

          today_compare = comparison(readings['current']['value']);
          yest_compare = comparison(readings['yest_peak']['value']);

          if (today_compare != yest_compare) {
              var peak_compare = ', whereas yesterday’s peak was akin to  ' + yest_compare + '.'
          } else {
              var peak_compare = ', which is the same as yesterday.'
          }

          $('#0-2').append("This is " + larger_smaller + " yesterday’s peak of " + readings['yest_peak']['value'] + " dB, which occurred at " + clockTime(readings['yest_peak']['time']*1000) + ". Right now, the station could be compared to " + now_comparison + ' ' + yest_compare);
        }
        // condition for yesterday
    } else if (Math.abs(readings['current']['value'] - readings['today_trough']['value']) < 2) {
        $('#0-2').text("The sound levels are at " + readings['current']['value']+ " dB, which is close to the quietest it has been today.");

        var d = new Date();
        var hour = d.toLocaleString('en-EN', {hour: '2-digit', hour12: false, timeZone: 'America/New_York'});
        var curTime = hour + ":" + d.getMinutes();
        if (hour <= 8) {
          $('#0-2').append(" This isn’t surprising; it's only " + curTime + " in New York City. As rush hour starts, the noise levels will inevitably go up.");
        } else {
          if (yesterday) {
            $('#0-2').append(" Yesterday, the station was at its most tranquil at " + clockTime(readings['yest_trough']['time']*1000) + ". The sound intensities are expected to kick up a notch though.");
          }
        }
    } else {
      if (readings['current']['value'] < readings['today_peak']['value']) {
        var louder_quieter = 'quieter';
      } else {
        var louder_quieter = 'louder';
      }
      $('#0-2').text("The sound levels are at " + readings['current']['value'] + " dB, but this is " + louder_quieter + " than today’s peak of " + readings['today_peak']['value'] + " dB. At the peak, it would’ve seemed like " + comparison(readings['today_peak']['value']) + ". Now, it’s more like " + comparison(readings['current']['value']) + ".");
    }
  }

  // Function responsible for updating the 'concourse/S train' section
  function update_s(newData){
    var readings = newData['concourse'];

    var yesterday = (readings['yest_trough']['value'] != 999) ? true : false;

    // updateChart(s_chart, readings['current']['time'], readings['current']['value']);
    var hour = new Date().toLocaleString('en-EN', {hour: '2-digit', hour12: false, timeZone: 'America/New_York'});

    if (hour < 6) {
      $('#1-1').text("It’s normally quiet here this time of the day. The Shuttle (S) train is not in service until the clock hits 6:00 am. But, during the day, the milieu is completely different.");
    } else {
      var timedif = readings['trains']['next_arrival'] - Date.now()/1000;

      if (readings['current']['value'] > 100){
        $('#1-2').text("But, right now, the musician(s) are trying to drown out the sound of the trains that arrive and leave from the two platforms that service the S train. The crowds that gather around this coveted spot to listen to the music and see the performances suggest that the musicians aren’t unwanted, even though they add to the noise levels in the subway.");
      } else {
        $('#1-2').text("The only disruption is the sound of the trains pulling in and departing. This sound alone doesn’t have as much of an adverse impact on the shopkeepers who run small booths and newsstands around here.");
      }

      if (timedif < 0) {
        $('#1-1').text("The last S train arrived " + Math.round(Math.abs(timedif)) + " seconds ago.");
      } else if (timedif < 60) {
        $('#1-1').text("The next S train is set to arrive in about " + Math.round(timedif) + " seconds.");
      } else {
        $('#1-1').text("The next S train is set to arrive in about " + Math.round(timedif/60) + " minutes.");
      }
    }

    var nowVal = readings['current']['value']

    function getThresh(val) {
      return Math.round((8/Math.pow(2, (val-90)/5))*10) / 10;
    }

    function getThreshText(thresh) {
      if (thresh == 1) {
        var threshText = 'working no more than one hour';
      } else if (thresh == 0) {
        var threshText = 'not working in this environment';
      } else {
        var threshText = 'working no more than ' + thresh + ' hours';
      }
      return threshText;
    }

    if (nowVal > 90) {
      var thresh = getThresh(nowVal);
      var threshText = getThreshText(thresh);
      $('#1-3').text("Right now, the noise level is " + nowVal + " dB. At this level, the OSHA guidelines recommend " + threshText + " without hearing protection.");
    } else if (readings['today_peak']['value'] >= 90) {
      var todayPeak = readings['today_peak']['value'];
      var thresh = getThresh(todayPeak);
      var threshText = getThreshText(thresh);
      $('#1-3').text("While the noise has reduced now, earlier today, it was at " + todayPeak + " dB. At this level, the OSHA guidelines recommend " + threshText + " without hearing protection.");
    } else if (yesterday && readings['yest_peak']['value'] > 90) {
      var yestPeak = readings['yest_peak']['value'];
      var thresh = getThresh(yestPeak);
      var threshText = getThreshText(thresh);
      $('#1-3').text("The noise levels have been manageable so far today, but yesterday, it reached " + yest_peak + " at " + clockTime(readings['yest_peak']['time']) + ". At this level, the OSHA guidelines recommend " + threshText + " without hearing protection.");
    } else {
      $('#1-3').text("The noise levels have been within the OSHA guidelines all day today. But, if they were to peak, not everyone would be able to don protective gear.");
    }
  }

  // Function responsible for updating the '1-2-3' section
  function update_red(newData) {
    var readings = newData['1-2-3'];
    // updateChart(red_chart, readings['current']['time'], readings['current']['value']);
    var louderQuieter = (readings['current']['value'] > newData['concourse']['current']['today']) ? 'louder' : 'quieter'

    var diff = Math.round(Math.abs((readings['current']['value'] - newData['concourse']['current']['value']))*10)/10;
    $('#2-1').text("Right now, the sound level is " + readings['current']['value'] + " dB. That's " + louderQuieter + " than the concourse level by " + diff + " decibels.");

    var comparison1 = comparison(readings['current']['value'])
    var comparison2 = comparison(newData['concourse']['current']['value']);
    if (comparison1 != comparison2) {
      $('#2-1').append(" Being down here is like " + comparison1 + "; just twenty feet higher, it's like " + comparison2 + ".");
    }

    var timedif = readings['trains']['next_arrival'] - Date.now()/1000;
    if (timedif < 0) {
      $('#2-2').text("The last train arrived " + Math.round(Math.abs(timedif)) + " seconds ago, which caused a momentary spike in the sound intensity.");
    } else if (timedif < 60) {
      $('#2-2').text("The next train will arrive in about " + Math.round(timedif) + " seconds, which will cause a momentary spike in the sound intensity.");
    } else {
      $('#2-2').text("The next train will arrive in about " + Math.round(timedif/60) + " minutes, which will cause a momentary spike in the sound intensity.");
    }
  }

  // Function responsible for updating the '7' section
  function update_purple(newData) {
    var readings = newData['7'];
    // updateChart(purple_chart, readings['current']['time'], readings['current']['value']);

    var yesterday = (readings['yest_trough']['value'] != 999) ? true : false;

    $('#3-1').text("The 7 train runs 60 feet below the surface, at the lowest level of Times Square station. Further away from the music and the flocks of passenger, it is almost quiet down here, with the noise levels at " + readings['current']['value'] +  " decibels.");

    if (yesterday) {
      var yestPeak = readings['yest_peak']['value'];
      $('#3-1').append("Yesterday, it got as loud as " + yestPeak + " here, but the 1-2-3 platform was at " + newData['1-2-3']['yest_peak']['value'] + " whereas the concourse was at " + newData['1-2-3']['yest_peak']['value']  + " decibels.");
    }


    var purpleDiff = Math.round((readings['current_peak']['value'] - readings['current_trough']['value'])*10)/10;
    $('#3-2').text("In a subway system with a plethora of different sources of noise, this is a cause for concern. Over the last five minutes, the sound intensity has varied by " + purpleDiff + " decibels.")

    var streetDiff = Math.round((newData['surface']['current_peak']['value'] - newData['surface']['current_trough']['value'])*10)/10;
    var concourseDiff = Math.round((newData['concourse']['current_peak']['value'] - newData['concourse']['current_trough']['value'])*10)/10;
    var redDiff = Math.round((newData['1-2-3']['current_peak']['value'] - newData['1-2-3']['current_trough']['value'])*10)/10;

    if (purpleDiff > Math.max(streetDiff, concourseDiff, redDiff)) {
      var level = '7 train';
      var max = purpleDiff;
      var min = readings['current_trough']['value'];
    } else if (streetDiff > Math.max(purpleDiff, concourseDiff, redDiff)) {
      var level = 'street';
      var max = streetDiff;
      var min = newData['surface']['current_trough']['value'];
    } else if (concourseDiff > Math.max(streetDiff, purpleDiff, redDiff)) {
      var level = 'concourse';
      var max = concourseDiff;
      var min = newData['concourse']['current_trough']['value'];
    } else {
      var level = '1-2-3 train';
      var max = redDiff;
      var min = newData['1-2-3']['current_trough']['value'];
    }

    if (level == '7 train'){
      $('#3-2').append(' That the largest variation of any of the levels right now.');
    } else {
      $('#3-2').append(' The largest variation is on the ' + level + ', where the variation over the last five minutes is ' + max + ' decibels.');
    }

    if (max > 10){
      $('#3-2').append(' That amount of variation is like going from ' + comparison(min) + ' to ' + comparison(min+max) + ' in less than five minutes.');
    }

  }

  // Given the span ID and the replacement text, swap it out (if it's different)
  function updateText(divId, replacementText) {
    id = '#' + divId;
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
