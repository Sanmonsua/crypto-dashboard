document.addEventListener('DOMContentLoaded', () =>{
  document.querySelector('#search-coins-field').onkeyup = ()=>{
    value = document.querySelector('#search-coins-field').value;
    document.querySelector('#search-content-holder').setAttribute('hidden', true);
    document.querySelector('#search-content').innerHTML = value;
    search(value);
    if (value.length > 0){
      document.querySelector('#search-content-holder').removeAttribute('hidden');
    }
  }

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
      console.log(data.coins_html);
      document.querySelector('#coins-list').innerHTML += data.coins_html;
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

function search(value){
  const request = new XMLHttpRequest();
  request.open('POST', 'search');

  request.onload = () =>{
    const data = JSON.parse(request.responseText);

    if (!data.has_another){
      document.querySelector('#load-more-btn').setAttribute('hidden', 'true');
    } else{
      document.querySelector('#load-more-btn').removeAttribute('hidden');
    }
    console.log(data.coins_html);
    document.querySelector('#coins-list').innerHTML = data.coins_html;
  }
  const data = new FormData()
  data.append('csrfmiddlewaretoken', window.CSRF_TOKEN);
  data.append('search', value)
  request.send(data);
}
