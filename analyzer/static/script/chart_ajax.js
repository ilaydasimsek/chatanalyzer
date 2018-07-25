function get_length_chart_data(){
        var length_chart_data;
        $.ajax({
            url: currentUser + username+"/length/" ,
            dataType : 'html',
            timeout : 30000,
            async: false,
            success: function(data){
                length_chart_data = data;
            },
        });

        return length_chart_data;
}
function get_time_chart_data(){
    var time_chart_data;
    $.ajax({
        url: currentUser + username+"/time/" ,
        async: false,
        dataType : 'html',
        timeout : 30000,
        success: function(data){
            time_chart_data = data
        }
    });
    return time_chart_data;
}


function hide_show_time() {
     var length = document.getElementById("length");
    var time = document.getElementById("time");
    var positivity = document.getElementById("positivity");
    if (time.style.display === "none") {
        time.style.display = "block";
        length.style.display = "none";
        positivity.style.display = "none";
    } else {
        time.style.display = "none";
    }
}
function hide_show_length() {
    var length = document.getElementById("length");
    var time = document.getElementById("time");
    var positivity = document.getElementById("positivity");
    if (length.style.display === "none") {
        length.style.display = "block";
        time.style.display = "none";
        positivity.style.display = "none";
    } else {
        length.style.display = "none";
    }

}

function hide_show_positivity() {
    var length = document.getElementById("length");
    var time = document.getElementById("time");
    var positivity = document.getElementById("positivity");
    if (positivity.style.display === "none") {
        positivity.style.display = "block";
        length.style.display = "none";
        time.style.display = "none";
    } else {
        positivity.style.display = "none";
    }
}


 function pageLoad(){
        var length = document.getElementById("length");
        var time = document.getElementById("time");
        var positivity = document.getElementById("positivity");
        positivity.style.display = "none";
        length.style.display = "none";
        time.style.display = "none";

        var length_chart_data = JSON.parse(get_length_chart_data());
        var time_chart_data = JSON.parse(get_time_chart_data());
        var ctx2 = document.getElementById("lengthChart");

        var lengthChart = new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: ["Very Short", "Short", "Medium", "Long", "Very Long"],
                datasets: [{
                    label: '# of Votes',
                    data: length_chart_data,
                    backgroundColor: [
                        'rgba(255, 210, 255, 1)',
                        'rgba(214, 151, 198, 1)',
                        'rgba(201, 92, 155, 1)',
                        'rgba(151, 32, 114, 1)',
                        'rgba(119, 25, 90, 1)',

                    ],
                    borderColor: [
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                    ],
                    borderWidth: 4
                }]
            },

        });
        var ctx1 = document.getElementById("timeChart");
        var timeChart = new Chart(ctx1, {
            type: 'pie',
            data: {
                labels: ["Very Short", "Short", "Medium", "Long", "Very Long"],
                datasets: [{
                    label: '# of Votes',
                    data: time_chart_data,
                    backgroundColor: [
                        'rgba(255, 210, 255, 1)',
                        'rgba(214, 151, 198, 1)',
                        'rgba(201, 92, 155, 1)',
                        'rgba(151, 32, 114, 1)',
                        'rgba(119, 25, 90, 1)',
                    ],
                    borderColor: [
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                        'rgba(55,17,36,1)',
                    ],
                    borderWidth: 4
                }]
            },

        });
    }

window.onload = pageLoad;
