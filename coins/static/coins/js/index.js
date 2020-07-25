document.addEventListener('DOMContentLoaded', () =>{

  document.querySelector('#load-more-btn').onclick = function () {
    const request = new XMLHttpRequest();
    request.open('POST', 'load_coins');

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


    }

    const data = new FormData();
    data.append('csrfmiddlewaretoken', window.CSRF_TOKEN);
    data.append('page', this.dataset.page);
    request.send(data);
  }

});
