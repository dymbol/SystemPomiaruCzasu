
    //function shows clock
    function startTime() {
        var today = new Date();
        var h = today.getHours();
        var m = today.getMinutes();
        var s = today.getSeconds();
        var ms = today.getMilliseconds();
        m = checkTime(m);
        s = checkTime(s);
        document.getElementById('time_clock').innerHTML =
        h + ":" + m + ":" + s+ ":" + ms;
        var t = setTimeout(startTime, 500);
    }
    function checkTime(i) {
        if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
        return i;
    }
    startTime();




    // TIME MEASURMENT START //
    var StartTime;
    var EndTime;
    var TimeDiff;
    var StartLock = false;
    var StopLock = false;
    var MeasureMade = false;
    var fee = 0;
    var taryfa = 0;

   function start_measure()
   {
        if( StartLock == false )
        {
            StartLock = true;
            StartTime = new Date();
            //console.log(StartTime);

            $("#btn_start").attr("disabled", true);
            $("#stoper_info").text("Pomiar w toku");
        } else {console.log("Can't start")}
   };

   function stop_measure()
   {
        if(MeasureMade == false && StartLock == true) {
            EndTime = new Date();
            //console.log(EndTime);
            TimeDiff = EndTime - StartTime;
            MeasureMade = true;
            //console.log(TimeDiff);
            $('#result').text(TimeDiff);
            $("#btn_stop").attr("disabled", true);
            $("#stoper_info").text("Pomiar wykonany");
        } else {console.log("Measure already done!")}


   };

   function clear_measure()
   {
    StartLock = false;
    StartLock = false;
    StopLock = false;
    MeasureMade = false;

    taryfa = 0;
    $('#taryfa').text("Nie");

    fee = 0;
    $('#kara').text(fee);

    $('#result').text("-");
    $("#btn_start").attr("disabled", false);
    $("#btn_stop").attr("disabled", false);
    $("#stoper_info").text("Gotowy do pomiaru");
    $('#send_result_info').html("")
   }


    function add_fee()
    {
        fee = fee + 5
        $('#kara').text(fee);
    }

    function add_taryfa()
    {
        taryfa = 1
        $('#taryfa').text("Tak");
    }

    function send_result(team_id, track_id, loop)
    {
        $.get( "/save_result/"+team_id+"/"+track_id+"/"+loop+"/"+TimeDiff+"/"+fee+"/"+taryfa, function( data ) {
            $( "#send_result_info" ).text( data["status"] );

            jQuery.each(data["msg"], function() {
             //console.log(this);
             $('#send_result_info').append(
                    '<div class=\"alert alert-danger\" role=\"alert\">'+this+'</div>'
                )
            });

            if (data["status"] == "ok") {
                alert( "Wynik został zapisany" );
            }else{
                alert( "Błąd zapisu wyniku" );
            }
        });
    }
