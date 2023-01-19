function searchUserById() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById('SearchUserInput');
    filter = input.value.toUpperCase();
    table = document.getElementById('UsersTable');
    tr = table.getElementsByTagName('tr');
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td_id = tr[i].getElementsByTagName("td")[0];
      if (td_id){
        txtValue = td_id.textContent || td_id.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = 'none';
        }
      }
    }
}

function searchDownloadByUserId() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById('SearchDownloadInput');
  filter = input.value.toUpperCase();

  lg = $('#downloadsUl li')

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < lg.length; i++) {
    li = lg[i];
    if (li){
      txtValue = li.textContent || li.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        lg[i].style.display = "";
      } else {
        lg[i].style.display = 'none';
      }
    }
  }
}

function redirect_to_users(){
    window.location.replace('/users');
}

function redirect_to_downloads(){
  window.location.replace('/downloads');
}