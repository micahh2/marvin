function getUrl(subUrl) {
    return "" + subUrl;
}

$(document).ready(function() {
    $("input#query").on("keypress", function(e) {
        e = e || window.event;
        if(e.keyCode == 13) {
            console.log("Search");
            var val = $("input#query").val();
            if(val.trim() != "") {
                $("div#answer").html("<div class='loader'></div>");
                document.title = val;
                $.ajax({
                    url:"/query",
                    type:"POST",
                    data: val,
                    contentType: "application/json",
                    success: function(data) {
                        var ans = "";
                        _.each(data["json_list"], function(i) {
                            ans += "<div class='source'>";
                            ans += "<b>" + i["title"] + "</b>";
                            ans += "<div class='ans'>";
                            ans += i["result"];
                            ans += "</div></div>";
                        });
                        $("div#answer").html(ans);
                        MathJax.typeset();
                    }
                });
            }
            else {
                $("div#answer").html("");
            }
        }
    });

    $(window).on("keypress", function(e) {
        e = e || window.event;
        if(e.keyCode == 27) {
            $("input#query").val("");
        }
    });
});
