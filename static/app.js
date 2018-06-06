$(function () {
    var router = Sammy(function () {

        this.get('#/', function () {
            console.log("route main")
            $('#search-input').val("");
            doSearch();
        });

        this.get('#/search/q=(.*)', function () {
            console.log("route search", this.params['splat'])
            var q = this.params['splat'][0];
            $('#search-input').val(q);
            doSearch();
        });

    });

    var currentResults = undefined;

    function autocompleteAPI(req, res) {
        return $.ajax({
            type: "POST",
            url: "/api/autocomplete_agg",
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            data: JSON.stringify({
                q: req.term
            }),
            success: function (data) {
                console.log(data);
                res(data)
            }
        });
    }

    function searchAPI(term, callback) {
        return $.ajax({
            type: "POST",
            url: "/api/search",
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            data: JSON.stringify({
                q: term
            }),
            success: function (data) {
                console.log(data);
                callback(data)
            }
        });
    }

    function listColumn(listVal) {
        if (!Array.isArray(listVal)) {
            return listVal || ""
        }

        return "<ul class='pl-0' style='list-style-type: none;'><li>" + listVal.join("</li><li>") + "</li></ul>"
    }

    function nutriscoreImageUrl(grade) {
        return "https://static.openfoodfacts.org/images/misc/nutriscore-" + grade + ".svg"
    }


    function render(results) {

        var hits = results.hits.hits;

        var html = '';
        for (var i = 0; i < hits.length; i++) {
            var product = hits[i]._source;

            html += '<tr data-toogle="popover" data-title="' + product.product_name + '" data-product-idx="' + i + '" >';
            html += '<td><a href="/api/product?code=' + product.code + '">' + product.code + '</a></td>'
            html += '<td>' + product.product_name + '</td>'
            html += '<td>' + listColumn(product.brands) + '</td>'
            html += '<td>' + listColumn(product.quantity) + '</td>'
            html += '<td>' + (product.fat_100g || "") + '</td>'
            html += '<td>' + (product.salt_100g || "") + '</td>'
            html += '<td>' + (product.sugars_100g || "") + '</td>'
            html += '<td>' + (product.proteins_100g || "") + '</td>'

            html += "<td>";
            var grade = product.nutrition_grade_fr || product.nutrition_grade_uk;
            if (grade) {
                html += '<img width="150" src="' + nutriscoreImageUrl(grade) + '"></img>'
            }
            html += "</td>";
            html += '</tr>';
        }

        $('#search-results tbody tr').remove();
        $('#search-results tbody').append(html);
        $('#search-results tbody tr[data-toogle="popover"]').popover({
            html: true,
            trigger: 'hover',
            content: function () {
                var idx = parseInt($(this).attr('data-product-idx'));
                var product = currentResults ? currentResults.hits.hits[idx]._source : {};
                var content = "";

                function addImageIfExists(image_url) {
                    if (image_url) {
                        content += '<img src="' + image_url + '" />';
                    }
                }

                addImageIfExists(product.image_small_url);
                addImageIfExists(product.image_ingredients_small_url);
                addImageIfExists(product.image_nutrition_small_url);

                if (product.categories_fr) {
                    content += "<div><b>Catégories :</b>";
                    content += listColumn(product.categories_fr);
                    content += "</div>";
                }
                return content;
            },
            placement: "auto"
        });
    }

    function doSearch() {
        var q = $("#search-input").val()
        $('#search-input').autocomplete('close');
        searchAPI(q, function (results) {
            currentResults = results;
            render(results)
        });
    }

    function closeAllPopover() {
        $("[data-toogle='popover']").popover('hide');
    }


    $('#search-input').autocomplete({
        source: autocompleteAPI,
        minLength: 2
    });

    $('#search-input').keyup(function (e) {
        if (e.which === 13) {
            var q = $("#search-input").val();
            closeAllPopover();
            router.setLocation("#/search/q=" + q);
            return false
        }
    });

    $(document).on('click', closeAllPopover);

    router.run("#/");
});
