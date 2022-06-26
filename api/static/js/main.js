function searchUserById() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("SearchUserInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("UsersTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td_id = tr[i].getElementsByTagName("td")[0];
      if (td_id){
        txtValue = td_id.textContent || td_id.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}

function redirect_to_users(){
    window.location.replace("/users");
}