document.addEventListener('DOMContentLoaded', () =>{

  document.querySelector('#load-more-btn').onclick = function () {
    const request = new XMLHttpRequest();
    request.open('POST', 'load_coins');

    const x = pageXOffset;
    const y = pageYOffset;

    const page = this.dataset.page;

    request.onload = () =>{
      console.log(page);
      const data = JSON.parse(request.responseText);

      if (data.has_another){
        this.setAttribute('data-page', parseInt(page)+1);
      } else{
        this.setAttribute('hidden', 'true');
      }

      document.querySelector('#coins-table').innerHTML += data.coins_html;
      scrollTo(x, y);

    }

    const data = new FormData();
    data.append('csrfmiddlewaretoken', window.CSRF_TOKEN);
    data.append('page', this.dataset.page);
    request.send(data);
  }

  document.querySelectorAll('.field').forEach( f =>{
    f.onclick = function(){
      redirectPost('', {'field':f.dataset.field, 'csrfmiddlewaretoken':window.CSRF_TOKEN});
    }
  })

});

function redirectPost(url, data) {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = url;
    console.log(data['field'])
    for (var name in data) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = data[name];
        form.appendChild(input);
    }
    form.submit();
    console.log('submited');
}
