$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promotion_id").val(res.id);
        $("#promotion_name").val(res.name);
        $("#promotion_start_date").val(res.start_date);
        $("#promotion_end_date").val(res.end_date);
        $("#promotion_type").val(res.type);
        $("#promotion_value").val(res.value);
        $("#promotion_product_id").val(res.product_id);
        if (res.ongoing == true) {
            $("#promotion_ongoing").val("true");
        } else {
            $("#promotion_ongoing").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_id").val("");
        $("#promotion_name").val("");
        $("#promotion_start_date").val("");
        $("#promotion_end_date").val("");
        $("#promotion_type").val("");
        $("#promotion_value").val("");
        $("#promotion_product_id").val("");
        $("#promotion_ongoing").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a promotion
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#promotion_name").val();
        let start_date = $("#promotion_start_date").val();
        let end_date = $("#promotion_end_date").val();
        let type = $("#promotion_type").val();
        let ongoing = $("#promotion_ongoing").val() == "true";
        let product_id = parseInt($("#promotion_product_id").val());
        let value = parseFloat($("#promotion_value").val());

        let data = {
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "type": type,
            "ongoing": ongoing,
            "product_id": product_id,
            "value": value,
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a promotion
    // ****************************************

    $("#update-btn").click(function () {

        let promotion_id = $("#promotion_id").val();
        let name = $("#promotion_name").val();
        let start_date = $("#promotion_start_date").val();
        let end_date = $("#promotion_end_date").val();
        let type = $("#promotion_type").val();
        let ongoing = $("#promotion_ongoing").val() == "true";
        let product_id = parseInt($("#promotion_product_id").val());
        let value = parseFloat($("#promotion_value").val());

        let data = {
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "type": type,
            "ongoing": ongoing,
            "product_id": product_id,
            "value": value,
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/promotions/${promotion_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("promotion has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promotion_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a promotion
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#promotion_name").val();
        let product_id = parseInt($("#promotion_product_id").val());
        let start_date = $("#promotion_start_date").val();

        let queryString = ""

        if (name) {
            queryString += '&name=' + name
        }
        if (product_id) {
            queryString += '&product_id=' + product_id
        }
        if (start_date) {
            queryString += '&start_date=' + start_date
        }

        // drop first '&' 
        if (queryString.length > 0) {
            queryString = queryString.substring(1)
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Start Date</th>'
            table += '<th class="col-md-2">End Date</th>'
            table += '<th class="col-md-2">Type</th>'
            table += '<th class="col-md-2">Value</th>'
            table += '<th class="col-md-2">Ongoing</th>'
            table += '<th class="col-md-2">Product ID</th>'
            table += '</tr></thead><tbody>'
            let firstpromotion = "";
            for(let i = 0; i < res.length; i++) {
                let promotion = res[i];
                table +=  `<tr id="row_${i}"><td>${promotion.id}</td><td>${promotion.name}</td><td>${promotion.start_date}</td><td>${promotion.end_date}</td><td>${promotion.type}</td><td>${promotion.value}</td><td>${promotion.ongoing}</td><td>${promotion.product_id}</td></tr>`;
                if (i == 0) {
                    firstpromotion = promotion;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstpromotion != "") {
                update_form_data(firstpromotion)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
