function searchUserById() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById('SearchUserInput');
    filter = input.value.toUpperCase();
    table = document.getElementById('usersTable');
    tr = table.getElementsByTagName('tr');
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      th_id = tr[i].getElementsByTagName("th")[0];
      if (th_id){
        txtValue = th_id.textContent || th_id.innerText;
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

  lg = $('#downloadsUl tr')

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < lg.length; i++) {
    tr = lg[i];
    if (tr){
      txtValue = tr.textContent || tr.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        lg[i].style.display = "";
      } else {
        lg[i].style.display = 'none';
      }
    }
  }
}

function users(){
    window.location.replace('/users');
}

function downloads(){
  window.location.replace('/downloads');
}

function logout() {
  window.location.replace('/logout')
}