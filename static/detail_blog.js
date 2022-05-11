function save_blog() {
    const url = $('#basic_url').val();
    const summary = $('#basic_summary').val();
    const today = new Date().toISOString();
    $.ajax({
        type: "POST",
        url: "/blogg/saveBlog",
        data: {url_give: url, summary_give: summary, date_give: today},
        success: function (response) {
            console.log(response)
        }
    });
}

function chg_blog(a) {
    const id = a;
    const url = $('#basic_url').val();
    const summary = $('#basic_summary').val();
    const today = new Date().toISOString();
    $.ajax({
        type: "POST",
        url: "/chgBlog",
        data: {url_give: url, summary_give: summary, date_give: today , id_give: id},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });
}

function save_comment(a) {
    const comment = $('#comment1').val();
    const today = new Date().toISOString();
    $.ajax({
        type: "POST",
        url: "/savecomment",
        data: {comment_give: comment, date_give: today , id_give: a},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });
}
function chg_comment(a) {
    const comment = $('#comment1').val();
    const today = new Date().toISOString();
    $.ajax({
        type: "POST",
        url: "/chgcomment",
        data: {comment_give: comment, date_give: today , id_give: a},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });
}
function del_comment(a) {
    const listNum = a;
    const _id = '6279f4887fb619a25b54f923'
    $.ajax({
        type: "POST",
        url: "/delcomment",
        data: { listNum_give: listNum, '_id_give':_id},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });
}
