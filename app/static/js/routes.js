

function moveTo(id){
  listItems = document.getElementsByTagName('li')
  for (let item of listItems) {
    item.classList.remove('active')
  }
  liSelected = document.getElementById(id)
  liSelected.className = "active"
}


