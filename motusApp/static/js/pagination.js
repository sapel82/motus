$(document).ready(function () {
    window.news_index = '';

    var page = 1;
    var block_request = false;
    var end_pagination = false;

    $(window).scroll(function () {
        var margin = $(document).height() - $(window).height() - 50;

        if ($(window).scrollTop() > margin && end_pagination === false && block_request === false) {
            block_request = true;
            page += 1;

            $.ajax({
                type: 'GET',
                url: window.news_index,
                data: {
                    "page": page
                },
                success: function (data) {
                    if (data.end_pagination === true) {
                        end_pagination = true;
                    } else {
                        block_request = false;
                    }
                    $('.records-list').append(data.content);
                }
            })
        }
    });
})