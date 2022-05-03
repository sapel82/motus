$(document).ready(function () {

    // Set ressource for profile to active/inactive
    $(".moodfactor-container").each(function(i) {

        var ressource_id = $(this).attr('id');
        var id = ressource_id.substr(10);

        $(document).on("click tap", `#${ressource_id}`, function()
        {
            // Shake effect
            $(`#${ressource_id}`).addClass('shake').on("animationend", function(e) {
                $(this).removeClass('shake').off("animationend");
              });

            $.ajax({
                url: `/app/set/ressource/${id}`,
                success: function (result)
                {
                    if (result == "false") {
                        $(`#ressource_img_${id}`).fadeTo(1, 0.3);
                        $(`#${ressource_id}`).attr("data-active", "false");
                    }
                    else {
                        $(`#ressource_img_${id}`).fadeTo(1, 1);
                        $(`#${ressource_id}`).attr("data-active", "true");
                    }
                }
            })
        })
    })


    // // Check if enough mood factors are selected
    // $(document).on("click tap touchstart", "#submitRessources", function()
    // {
    //     ressourcesSelected = $(".moodfactor-container[data-active='true']").length;
    //     if (ressourcesSelected >= 5) {
    //         $("#submitRessources").submit(function(){
    //             return true;
    //         })
    //     }
    //     else {
    //         alert("Es wurde nicht genügend Ressourcen ausgewählt");
    //         $("#submitRessources").submit(function(){
    //             return false;
    //         })
    //     }
    // })

});

// Shows the EULA modal window
function showEULA() {
    var eulaModal = new bootstrap.Modal(document.getElementById('eulaModal'));
    eulaModal.show(self);
}

// Shows the Use of data modal window
function showUseOfData() {
    var useOfDataModal = new bootstrap.Modal(document.getElementById('useOfDataModal'));
    useOfDataModal.show(self);
}

function countMoodFactors() {
    moodFactorsSelected = $(".moodfactor-container[data-active='true']").length;
    if (moodFactorsSelected >= 5) {
        return true
    }
    else {
        $("#notEnoughMoodFactorsModal").modal("show");
        return false;
    }
}





