$(document).ready(function() {
    $("#search-sites a").each(function(site_index, site) {
        $.getJSON(
            $(site).attr("href") + "?" + $("#searchform").serialize(),
            function(search_results) {
                $(search_results).each(function(index, element) {
                    $("#search-results dl").append(
                        "<dt><a href='" + element['url'] + "'>" + element["title"] + "</a></dt>\n" +
                            "<dd><div class='preview'>" + element["content"] + "</div></dd>"
                    );
                });
            });
    });
});
