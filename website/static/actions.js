function likePost (post_id) {
  let request = new XMLHttpRequest();
  request.open('GET', `/post/${post_id}/like`, true);
  request.send();
}

function unlikePost (post_id) {
  let request = new XMLHttpRequest();
  request.open('GET', `/post/${post_id}/unlike`, true);
  request.send();
}

function likeComment (comment_id) {
  let request = new XMLHttpRequest();
  request.open('GET', `/post/comment/${comment_id}/like`, true);
  request.send();
}

function unlikeComment (comment_id) {
  let request = new XMLHttpRequest();
  request.open('GET', `/post/comment/${comment_id}/unlike`, true);
  request.send();
}

function deletePost(post_id) {
  let request = new XMLHttpRequest();
  request.open('GET', `/post/${post_id}/delete`, true);
  request.send();
}

function deleteComment(comment_id) {
  let request = new XMLHttpRequest();
  request.open('GET', `/post/${comment_id}/delete`, true);
  request.send();
}
