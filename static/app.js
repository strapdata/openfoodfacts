$(function(){

    function autocomplete(req, res) {
        return $.ajax({
            type: "POST",
            url: "/api/autocomplete_agg",
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            data: JSON.stringify({
                q: req.term
            }),
            success: function(data) { console.log(data); res(data) }
        });
    }

    function search(term, callback) {
        return $.ajax({
            type: "POST",
            url: "/api/search",
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            data: JSON.stringify({
                q: term
            }),
            success: function(data) { console.log(data); callback(data) }
        });
    }

    function render(results) {

        var hits = results.hits.hits;

        var html = '';
        for(var i = 0; i < hits.length; i++) {
            var product = hits[i]._source;

            html +=
                '<tr>' +
                    '<td><a href="/api/product?code=' + product.code + '">' + product.code + '</a></td>' +
                    '<td><a href="' + product.url + '">' + product.product_name + '</a></td>' +
                    '<td>' + product.brands + '</td>' +
                    '<td><img src="' + product.image_url + '" alt="' + product.image_url + '" width="75" height="75"></img></td>' +
                '</tr>';
        }

        $('#search-results tr').not(':first').remove();
        $('#search-results tr').first().after(html);
    }

    $('#search-input').autocomplete({
        source: autocomplete,
        minLength: 2
    });

    $('#search-input').keyup(function(e) {
        if(e.which === 13) {
            $('#search-input').autocomplete('close');
            search($("#search-input").val(), render);
            return false
        }
    })
});
