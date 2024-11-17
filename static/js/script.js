let menuIcon = document.querySelector('#menu-icon');
        let navbar = document.querySelector('.navbar');
        let navbarLinks = document.querySelectorAll('.navbar a');
        let logoutBtn = document.getElementById('logout'); 
        let addBtn = document.getElementById('add');  


        menuIcon.onclick = () => {
            menuIcon.classList.toggle('fa-times');
            navbar.classList.toggle('active');
        };

        function adjustNavbarStyles() {
            if (window.innerWidth <= 445) {
                navbarLinks.forEach(link => {
                
                    link.classList.remove('w3-button', 'w3-red', 'w3-right', 'w3-margin-top', 'w3-margin-bottom', 'w3-white', 'w3-margin-right');
                });
            
                logoutBtn.classList.remove('w3-red');
                addBtn.classList.remove('w3-white'); 
            } else {
                
                logoutBtn.classList.add('w3-red');
                logoutBtn.classList.remove('w3-white');  

                addBtn.classList.add('w3-white'); 

                
                navbarLinks.forEach(link => {
                    link.classList.add('w3-button', 'w3-right', 'w3-margin-top', 'w3-margin-bottom', 'w3-margin-right');
                });
            }
        }


        window.addEventListener('load', adjustNavbarStyles);
        window.addEventListener('resize', adjustNavbarStyles);

        function updateCount(field, counterId, maxLength) {
        const currentLength = field.value.length;
        document.getElementById(counterId).textContent = `${currentLength}/${maxLength}`;
        }

    
        console.log(document.getElementById('flag').value);
        document.getElementById('image').src = default_img_src;
        defaultMsgIfTableEmpty();

        function openCustomAlert(idno) {
        document.getElementById('deleteIdNo').value = idno;
        document.getElementById('customAlert').style.display = 'flex'; 
        }

        function closeAlert() {
        document.getElementById('customAlert').style.display = 'none';
        }

        function readURI(input) {
            if(input.files && input.files[0]){
                reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('image').src = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);
            }
        }
        function view_record(image, idno, lastname, firstname, course, level) {
            document.getElementById('image').src = image;
            document.getElementById('idno').value = idno;
            document.getElementById('idno').readOnly = true;
            document.getElementById('lastname').value = lastname;
            document.getElementById('firstname').value = firstname;
            document.getElementById('course').value = course;
            document.getElementById('level').value = level;
            document.getElementById('flag').value = 1;
            console.log(document.getElementById('flag').value);
        }
        function cancel_record() {
            document.getElementById('image').src = default_img_src;
            document.getElementById('idno').value = '';
            document.getElementById('idno').readOnly = false;
            document.getElementById('lastname').value = '';
            document.getElementById('firstname').value = '';
            document.getElementById('course').value = '';
            document.getElementById('level').value = '';
            document.getElementById('flag').value = 0;
            console.log(document.getElementById('flag').value);
        }

        function viewrecordstudents(image, idno, lastname, firstname, course, level) {
            document.getElementById('image-view').src = image;
            document.getElementById('idno-view').value = idno;
            document.getElementById('lastname-view').value = lastname;
            document.getElementById('firstname-view').value = firstname;
            document.getElementById('course-view').value = course;
            document.getElementById('level-view').value = level;
            
            document.getElementById('viewModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('viewModal').style.display = 'none';
        }


        
        window.addEventListener('DOMContentLoaded', (event) => {
            const flashMessages = document.querySelectorAll('.flash-message');
            
            flashMessages.forEach((flashMessage) => {
                setTimeout(() => {
                    flashMessage.classList.add('fade-out');
                }, 2500);

                flashMessage.addEventListener('animationend', () => {
                    flashMessage.remove();
                });
            });
        });

        function substringer(str, phrase) {
            const index = str.indexOf(phrase);
            str = (index !== -1) ? str.slice(index) : ''; 
            return str;
        }

        function defaultMsgIfTableEmpty() {
            if (document.querySelectorAll('#table tbody #tr2').length == 0) {
                console.log('table is empty');
                document.getElementById('empty_table_msg').style = 'display: block;';
            } else {
                console.log('table is not empty!!');
            }
        }

    function checkIfFieldsExists() {
    const idno = document.getElementById('idno').value.trim();
    const lastname = document.getElementById('lastname').value.trim();
    const firstname = document.getElementById('firstname').value.trim();
    const course = document.getElementById('course').value.trim();
    const level = document.getElementById('level').value.trim();
    const img = substringer(document.getElementById('image').src, "/static/img/");
    
    if (!idno || !lastname || !firstname || !course || !level) {
        alert("Please fill in all fields.");
        return false;
    }

    if (img == default_img_src) {
        alert("Please insert an image.");
        return false;
    }

    console.log(img);
    console.log(default_img_src);
    return true;
}

function openAddStudentModal() {
    document.getElementById('addStudentModal').style.display = 'flex';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('addStudentModal')) {
        document.getElementById('addStudentModal').style.display = 'none';
    }
}

document.getElementById('close-login-btn').addEventListener('click', function() {
    document.getElementById('addStudentModal').style.display = 'none';
});