document.getElementById('solve').addEventListener('click', function() {
    const data = new FormData();
    data.append('plane', document.getElementById('plane').value);
    data.append('line_x', document.getElementById('line_x').value);
    data.append('line_y', document.getElementById('line_y').value);
    data.append('line_z', document.getElementById('line_z').value);
    axios.post('/solve', data).then(res => {
        if (res.data.error) {
            document.getElementById('steps').innerText = res.data.error;
            document.getElementById('plot').src = '';
        } else {
            document.getElementById('steps').innerHTML = res.data.steps.join('<br>');
            document.getElementById('plot').src = 'data:image/png;base64,' + res.data.image;
        }
    });
});

function insert(id, text) {
    const el = document.getElementById(id);
    el.value += text;
    el.focus();
}
