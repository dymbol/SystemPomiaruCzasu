
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
            $("#btn_start").attr("disabled", true);
            SendAlert("warning", "Pomiar w toku" );
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
            $('#result').text(MsToHuman(TimeDiff));
            $("#btn_stop").attr("disabled", true);
            SendAlert("success", "Pomiar wykonany" );


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
    SendAlert("info", "Gotowy do pomiaru" );
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
        $.get( "/save_result/"+team_id+"/"+track_id+"/"+TimeDiff+"/"+fee+"/"+taryfa, function( data ) {
            $( "#send_result_info" ).html( '<span class="badge badge-info">'+data["status"]+'</span>' );

            jQuery.each(data["msg"], function() {
            SendAlert("danger",  this);
            });

            if (data["status"] == 'ok') {
                alert( "Wynik został zapisany" );
            }else{
                alert( "Błąd zapisu wyniku" );
            }
        });
    }


    function SendAlert(level, msg) {
         $("#alerts").empty();
             $('#alerts').append(
                        '<div class=\"alert alert-'+level+'\" role=\"alert\"><h3>'+msg+'</h3></div>'
                    )
    }

    function MsToHuman(timeinms) {
        min = Math.floor((timeinms/1000/60) << 0),
        sec = Math.floor((timeinms/1000) % 60);
        ms = timeinms - (min*1000*60) - (sec*1000)
        return min+":"+sec+":"+ms
    }
