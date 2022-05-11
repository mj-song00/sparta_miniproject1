function save_blog() {
    const url = $('#basic_url').val(); //블로그 url
    const summary = $('#basic_summary').val(); // 블로그 요약내용
    const today = new Date().toISOString();  // 작성 날짜
    $.ajax({
        type: "POST",
        url: "/blogg/saveBlog",
        data: {url_give: url, summary_give: summary, date_give: today},
        success: function (response) { //{'msg': '저장 완료 !!'}
            console.log(response)
        }
    });
}

function del_blog(a) {
    const id = a; // 삭제할 블로그 id값
    $.ajax({
        type: "POST",
        url: "/delBlog",
        data: {id_give: id},
        success: function (response) { //{'msg' : '삭제되었습니다!'}
            alert(response['msg'])
            window.location.reload();
        }
    });
}

function save_comment(a) {
    const comment = $('#comment1').val(); //댓글 내용
    const today = new Date().toISOString(); // 댓글 작성 날짜
    const id = a; // 블로그 id값
    $.ajax({
        type: "POST",
        url: "/savecomment",
        data: {comment_give: comment, date_give: today, id_give: id},
        success: function (response) { // {'msg': '댓글 달기 성공 !!'}
            alert(response['msg'])
            window.location.reload();
        }
    });
}

function chg_comment(a) {
    const id = a; // 블로그 id값
    const comment = $('#comment1').val(); //댓글 내용
    const today = new Date().toISOString(); // 댓글 작성 날짜
    $.ajax({
        type: "POST",
        url: "/chgcomment",
        data: {comment_give: comment, date_give: today, id_give: id},
        success: function (response) { // {'msg': '댓글 달기 성공 !!'}
            alert(response['msg'])
            window.location.reload();
        }
    });
}

function del_comment(a) {
    const listNum = a; // 댓글 번호
    const id = '6279f4887fb619a25b54f923' // 블로그 id값
    $.ajax({
        type: "POST",
        url: "/delcomment",
        data: {listNum_give: listNum, '_id_give': id},
        success: function (response) {  //{'msg' : '삭제되었습니다!'}
            alert(response['msg'])
            window.location.reload();
        }
    });
}
