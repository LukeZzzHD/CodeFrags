Prism.plugins.NormalizeWhitespace.setDefaults({
	'remove-trailing': true,
	'remove-indent': true,
	'left-trim': true,
	'right-trim': true,
});


function deleteComment(id) {
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = () => {if(xhr.readyState == 4)$("#comments").load(document.URL + ' #comments');};
	xhr.open('GET', '/post/comment/' + id + '/delete', false);
	xhr.send();
	if (xhr.status == 200) {
		flashMessage('The comment has been deleted successfully!', 'success');
	} else {
		flashMessage('The comment couldn\'t be deleted!', 'danger');
	}
}

function deletePost(id) {
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = () => {if(xhr.readyState == 4)$("#comments").load(document.URL + ' #comments');};
	xhr.open('GET', '/post/' + id + '/delete', false);
	xhr.send();
	flashMessage('The post has been deleted successfully!', 'success');
}

function flashMessage (msg, type) {
	document.getElementsByClassName('col-12')[0].innerHTML += `
			<div class="flash-message card alert alert-${type}">
                ${msg}
				<span onclick="$(this).parent().remove()" class="remove-icon ml-auto">✕</span>
            </div>
	`;
}

function likeorunlikePost (id, action) {
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = () => {if(xhr.readyState == 4)$("#postLike").load(document.URL + ' #postLike');};
	xhr.open('GET', '/post/' + id + '/' + action, false);
	xhr.send();
	flashMessage('The post has been ' + action + 'd!', 'success');
}

function likeorunlikeComment (id) {}
