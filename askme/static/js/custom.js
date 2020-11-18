let vote = (oid, value, flag) => {
    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:8000/vote/',
        data: {
            event: value,
            object: oid,
            flag: flag,
        },
    }).done((response) => {
        if (flag === 0) {
            rating_id = 'rating_question_' + oid;
            like_button_name = '#like_question_' + oid;
            dislike_button_name = '#dislike_question_' + oid;
        }
        else {
            rating_id = 'rating_answer_' + oid;
            like_button_name = '#like_answer_' + oid;
            dislike_button_name = '#dislike_answer_' + oid;
        }
        let element = document.getElementById(rating_id);
        element.textContent = `${response.rating}`;
        if (value === 1) {
            $(like_button_name).attr("disabled", true);
            $(dislike_button_name).attr("disabled", false);
        }
        else {
            $(dislike_button_name).attr("disabled", true);
            $(like_button_name).attr("disabled", false);
        }
    });
};