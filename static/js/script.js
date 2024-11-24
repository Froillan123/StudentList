function checkIfFieldsExists(event) {
    event.preventDefault(); // Prevent form from submitting before validation

    const idno = document.getElementById('idno').value.trim();
    const lastname = document.getElementById('lastname').value.trim();
    const firstname = document.getElementById('firstname').value.trim();
    const course = document.getElementById('course').value.trim();
    const level = document.getElementById('level').value.trim();
    const image_data = document.getElementById('image_data').value.trim();
    const flag = document.getElementById('flag').value.trim();

    if (!idno || !lastname || !firstname || !course || !level) {
        alert("Please fill in all fields.");
        return false;
    }

    if (flag === '0') {
        fetch(`/check_student_exists?idno=${idno}`)
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert(`Student with ID No. ${idno} already exists.`);
                    document.getElementById('idno').value = ''; 
                    return false;  
                } else {
                    submitFormWithSnapshot();
                }
            })
            .catch(error => {
                alert("Error checking student existence. Please try again.");
                return false;  
            });
    } else {
        submitFormWithSnapshot();
    }
}

function submitFormWithSnapshot() {
    Webcam.snap(function(data_uri) {
        fetch(data_uri)
            .then(res => res.blob())
            .then(blob => {
                const file = new File([blob], "webcam.jpg", { type: "image/png" });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                document.getElementById('image_data').files = dataTransfer.files;
                document.getElementById('reg').submit();
            });
    });
}

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
        if (window.innerWidth <= 487) {
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



    function openCustomAlert(idno) {
    document.getElementById('deleteIdNo').value = idno;
    document.getElementById('customAlert').style.display = 'flex'; 
    }

    function closeAlert() {
    document.getElementById('customAlert').style.display = 'none';
    }

    function viewrecordstudents(image, idno, lastname, firstname, course, level) {
        document.getElementById('image-view').src = image; 
        document.getElementById('idno-view').value = idno; 
        document.getElementById('lastname-view').value = lastname; 
        document.getElementById('firstname-view').value = firstname; 
        document.getElementById('course-view').value = course; 
        document.getElementById('level-view').value = level; 
        document.getElementById('viewModal').style.display = 'flex';
        document.getElementById('image-view').style.display = 'block';
        document.getElementById('image-view').style.margin = 'auto'
    }


        function editRecord() {
            const idno = document.getElementById('idno-view') ? document.getElementById('idno-view').value : '';
            const lastname = document.getElementById('lastname-view') ? document.getElementById('lastname-view').value : '';
            const firstname = document.getElementById('firstname-view') ? document.getElementById('firstname-view').value : '';
            const course = document.getElementById('course-view') ? document.getElementById('course-view').value : '';
            const level = document.getElementById('level-view') ? document.getElementById('level-view').value : '';

            document.getElementById('image-view').style.display = 'none'; 
            document.getElementById('my_camera').style.display = 'block';  
            document.getElementById('idno').value = idno;
            document.getElementById('lastname').value = lastname;
            document.getElementById('firstname').value = firstname;
            document.getElementById('course').value = course;
            document.getElementById('level').value = level;

            document.getElementById('flag').value = '1'; 
            document.getElementById('reg').action = "/register"; 
            document.getElementById('viewModal').style.display = 'none';
            document.getElementById('addStudentModal').style.display = 'flex';

            const idnoField = document.getElementById('idno');
            idnoField.readOnly = true; 
            console.log(idnoField);  

            updateCount(document.getElementById('idno'), 'idno-count', 10);
            updateCount(document.getElementById('lastname'), 'lastname-count', 50);
            updateCount(document.getElementById('firstname'), 'firstname-count', 50);
            updateCount(document.getElementById('course'), 'course-count', 15);
            updateCount(document.getElementById('level'), 'level-count', 5);
        }

        function cancel_edit() {
            document.getElementById('idno').readOnly = false; 
            document.getElementById('idno').value = '';
            document.getElementById('lastname').value = '';
            document.getElementById('firstname').value = '';
            document.getElementById('course').value = '';
            document.getElementById('level').value = '';
            document.getElementById('flag').value = '0'; 
            const imageView = document.getElementById('image-view');
            if (document.getElementById('image-view').style.display === 'none') {
                imageView.src = '';  
                imageView.style.display = 'none';  
            }
            document.getElementById('addStudentModal').style.display = 'none';
            document.getElementById('idno-count').textContent = '0/10';
            document.getElementById('lastname-count').textContent = '0/50';
            document.getElementById('firstname-count').textContent = '0/50';
            document.getElementById('course-count').textContent = '0/15';
            document.getElementById('level-count').textContent = '0/5';
        }

    function closeModal() {
        document.getElementById('idno').readOnly = false; 
        document.getElementById('idno').value = '';
        document.getElementById('lastname').value = '';
        document.getElementById('firstname').value = '';
        document.getElementById('course').value = '';
        document.getElementById('level').value = '';
        document.getElementById('flag').value = '0'; 
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


    function openAddStudentModal() {
    document.getElementById('addStudentModal').style.display = 'flex';
    }

    window.onclick = function(event) {
    if (event.target == document.getElementById('addStudentModal')) {
        document.getElementById('addStudentModal').style.display = 'none';
    }
    }


    document.addEventListener('click', function(event) {
        const addStudentModal = document.getElementById('addStudentModal');
        const addStudentContent = document.querySelector('#addStudentModal .custom-modal-content');

        const viewModal = document.getElementById('viewModal');
        const viewContent = document.querySelector('#viewModal .view-modal-content');

        const customAlert = document.getElementById('customAlert');
        const alertContent = document.querySelector('#customAlert .alert-content');
        if (addStudentModal.style.display === 'flex' && !addStudentContent.contains(event.target)) {
            event.stopPropagation(); 
        }
        if (viewModal.style.display === 'flex' && !viewContent.contains(event.target)) {
            event.stopPropagation(); 
        }
        if (customAlert.style.display === 'flex' && !alertContent.contains(event.target)) {
            event.stopPropagation(); 
        }
    });

