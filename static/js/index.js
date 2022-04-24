function createChirp() {
    var title = document.getElementById("title").value;
    var body = document.getElementById("body").value;

    axios({
        method: "POST",
        url: "/chirp/create",
        data: {
            title: title,
            body: body,
        },
        headers: {
            "Content-Type": "application/json",
        }
    }).then(
        (response) => {
            var data = response.data;
            if (data.redirect) {
                // redirect exists, then set the URL to the redirect
                window.location.href = data.redirect;
            }

            if (data.status == 500) {
                alert(data.error);
                window.location.href = "/";  // redirect to home page
            }
        },
    )
}

function deleteChirp(chirp_id, chirps_title) {
    var message = "Are you sure to delete the chirp " + chirps_title + " ?";
    var confirm_delete = confirm(message);

    // value of confirm() function is True if user clicks on OK
    if (confirm_delete == true) {
        // use axios to call delete, with the article id to delete
        var url = "/chirp/delete/" + chirp_id;
        axios({
            method: "POST",
            url: url,
        }).then(
            (response) => {
                var data = response.data;
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            }
        );
    }
}

function createCMT(chirp_id) {
    var body = document.getElementById("body").value;

    axios({
        method: "POST",
        url: "/comment/create/" + chirp_id,
        data: {
            body: body,
        },
        headers: {
            "Content-Type": "application/json",
        }
    }).then(
        (response) => {
            var data = response.data;
            if (data.redirect) {
                // redirect exists, then set the URL to the redirect
                window.location.href = data.redirect;
            }

            if (data.status == 500) {
                alert(data.error);
                window.location.href = "/";  // redirect to home page
            }
        },
    )
}

function deleteCMT(cmt_id) {
    var message = "Are you sure to delete the comment ?";
    var confirm_delete = confirm(message);

    // value of confirm() function is True if user clicks on OK
    if (confirm_delete == true) {
        // use axios to call delete, with the article id to delete
        var url = "/comment/delete/" + cmt_id;
        axios({
            method: "POST",
            url: url,
        }).then(
            (response) => {
                var data = response.data;
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            }
        );
    }
}