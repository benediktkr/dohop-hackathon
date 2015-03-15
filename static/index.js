$(document).ready(function() {
    $("#myform").submit(function(e) {
        e.preventDefault();
        $("#spinner").show();

        var data = $("#myform").serialize();

        $.post('/fares.json', data, function(data) {
            $("#spinner").hide();
            console.log(data);
            if (data.my_price) {
                $("#myday").show()
                $("#result_price").html(data.my_price);
                if (data.my_price <= data.average) {
                    $("#result_text").html("Good day to travel");
                } else {
                    $("#result_text").html("Not-so-good day to travel");
                }            
            }

            
            if (data.cheapest_date) {
                $("#cheap").show();
                $("#result_cheap").html(data.cheapest_date);
                $("#cheap_price").html(data.cheapest_price);
                
            }
            if (data.expensive_date) {
                $("#exp").show();
                $("#result_exp").html(data.expensive_date);
                $("#exp_price").html(data.expensive_price);
            }
            $("#result").show();
        }, "json");
    });
});
