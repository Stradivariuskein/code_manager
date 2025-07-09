

async function getAllProjects() {
    const apiUrl = '/api/projects/';  // Cambia la URL si es necesario
    

    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const projects = await response.json();
        console.log('Projects:', projects);
        return projects;
    } catch (error) {
        console.error('Error fetching projects:', error);
    }
}

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

async function postRequest(url, method = null) {
    const msjElement = document.getElementById('msj');
    if (method == null) {
        method = "POST"
    }
    try {
        const response = await fetch(url, {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Si estás usando CSRF tokens en tu aplicación Django
            },
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Unknown error occurred');
        }

        msjElement.textContent = result.message || 'Success!';
    } catch (error) {
        console.error('Error:', error);
        msjElement.textContent = `Error: ${error.message}`;
    }
    renderProjects() // reload table
}

async function renderProjects() {
    const projects = await getAllProjects();
    console.log(projects)
    const tbody = document.getElementById('projects-table-body');
    tbody.innerHTML = '';  // Clear existing content

    projects.forEach(project => {
        const tr = document.createElement('tr');

        const containerIdTd = document.createElement('td');
        containerIdTd.setAttribute("data-label", "Docker ID")
        containerIdTd.textContent = project.container.dockerId.slice(-10);
        console.log(project.container.dockerId)
        tr.appendChild(containerIdTd);

        const nameTd = document.createElement('td');
        nameTd.setAttribute("data-label", "Name")
        nameTd.textContent = project.name;
        tr.appendChild(nameTd);

        const imageIdTd = document.createElement('td');
        imageIdTd.setAttribute("data-label", "Image ID")
        imageIdTd.textContent = project.container.imageId.slice(-10);
        tr.appendChild(imageIdTd);

        const ipTd = document.createElement('td');
        ipTd.setAttribute("data-label", "IP")
        const link_code = document.createElement('a');
        link_code.textContent = project.container.ip;
        link_code.setAttribute("target","_blank");
        link_code.setAttribute("href",`/Connect/${project.container.ip}/`)
        ipTd.appendChild(link_code);
        tr.appendChild(ipTd);

        const portsTd = document.createElement('td');
        portsTd.setAttribute("data-label", "Ports")
        portsTd.textContent = project.container.ports;
        tr.appendChild(portsTd);

        const statusTd = document.createElement('td');
        statusTd.setAttribute("data-label", "Status")
        statusTd.textContent = project.container.status;
        tr.appendChild(statusTd);

        const actionsTd = document.createElement('td');
        actionsTd.setAttribute("data-label", "Actions");

        // Crear el botón de los tres puntos
        const dropdownButton = document.createElement('button');
        dropdownButton.textContent = '⋮'; // Tres puntos verticales
        dropdownButton.className = 'dropdown-button';
        dropdownButton.onclick = function() {
            dropdownContent.classList.toggle('show');
        };

        // Crear el contenedor para los botones dentro del dropdown
        const dropdownContent = document.createElement('div');
        dropdownContent.className = 'dropdown-content';

        // Botón de Play
        const playButton = document.createElement('button');
        playButton.textContent = 'Play';
        playButton.onclick = function() {
            postRequest(`/api/project/${project.container.dockerId}/start/`);
        };
        dropdownContent.appendChild(playButton);

        // Botón de Stop
        const stopButton = document.createElement('button');
        stopButton.textContent = 'Stop';
        stopButton.onclick = function() {
            postRequest(`/api/project/${project.container.dockerId}/stop/`);
        };
        dropdownContent.appendChild(stopButton);

        // Botón de Restart
        const restartButton = document.createElement('button');
        restartButton.textContent = 'Restart';
        restartButton.onclick = function() {
            postRequest(`/api/project/${project.container.dockerId}/restart/`);
        };
        dropdownContent.appendChild(restartButton);

        // Botón de Delete
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function() {
            postRequest(`/api/project/${project.container.dockerId}/delete/`, method="DELETE");
        };
        dropdownContent.appendChild(deleteButton);

        // Añadir el botón de los tres puntos y el contenido del dropdown al <td>
        actionsTd.appendChild(dropdownButton);
        actionsTd.appendChild(dropdownContent);

        // Añadir <td> a la fila
        tr.appendChild(actionsTd);
        tbody.appendChild(tr);

        // const actionsTd = document.createElement('td');
        // actionsTd.setAttribute("data-label", "Actions")
        // const playButton = document.createElement('button');
        // playButton.textContent = 'Play';
        // playButton.onclick = function() {
        //     postRequest(`/api/project/${project.container.dockerId}/start/`);
        // };
        // actionsTd.appendChild(playButton);
        // const stopButton = document.createElement('button');
        // stopButton.textContent = 'Stop';
        // stopButton.onclick = function() {
        //     postRequest(`/api/project/${project.container.dockerId}/stop/`);
        // }
        // actionsTd.appendChild(stopButton);
        // const restartButton = document.createElement('button');
        // restartButton.textContent = 'Restart';
        // restartButton.onclick = function() {
        //     postRequest(`/api/project/${project.container.dockerId}/restart/`);
        // }
        // actionsTd.appendChild(restartButton);
        // const deleteButton = document.createElement('button');
        // deleteButton.textContent = 'Delete';
        // deleteButton.onclick = function() {
        //     postRequest(`/api/project/${project.container.dockerId}/delete/`, method="DELETE");
        // }
        // actionsTd.appendChild(deleteButton);
        // tr.appendChild(actionsTd);

        // tbody.appendChild(tr);
    });
}


// Crear el formulario
function createForm(event) {
    event.stopPropagation(); 
    const createBtn = document.getElementById('createBtn');
    createBtn.disabled = true;

    const card = document.createElement('div');
    card.classList.add('card');

    const form = document.createElement('form');
    form.innerHTML = `
        <div class="input-field">
            <label>Proyect name</label>
            <input type="text" name="name" placeholder="Nombre del proyecto">
        </div>
        <div class="input-field">
            <label>Password</label>
            <input type="password" name="password" placeholder="Contraseña">
        </div>
        <div class="input-field">
            <label>Enable https</label>
            <input type="checkbox" name="enable_https">
        </div>
        <div class="input-field">
            <label>Port</label>
            <input type="number" name="port" placeholder="Port: 8000">
        </div>
        <button id="submit_btn" type="submit" class="btn solid">Enviar</button>
    `;

    

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); 
        const submitButton = document.getElementById('submit_btn');
        submitButton.disabled = true;
        const apiUrl = '/api/create_project/';
        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            if (key === 'enable_https') {
                data[key] = form.elements[key].checked;
            } else if (key === 'port') {
                data[key] = parseInt(value, 10);
            } else {
                data[key] = value;
            }
        });

        // Asegúrate de que el campo enable_https esté presente en los datos
        if (!data.hasOwnProperty('enable_https')) {
            data['enable_https'] = false;
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                document.getElementById("msj").innerHTML = errorData.error || "Unknown error occurred";
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log(result);

                document.getElementById("msj").innerHTML = 'Project created successfully!'
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to create project');
        } finally {
            submitButton.disabled = false; // Habilitar el botón de envío nuevamente
            // Eliminar la tarjeta del DOM
            card.remove();
            const createBtn = document.getElementById('createBtn');
            createBtn.disabled = false;
        }
    });

    form.className = "sign-in-form";
    card.appendChild(form);
    document.body.appendChild(card);

    document.addEventListener('click', handleClickOutsideCard);
}


function handleClickOutsideCard(event) {
    const card = document.querySelector('.card');
    const createBtn = document.getElementById('createBtn');

    if (card && !card.contains(event.target)) {
        // Eliminar la tarjeta del DOM
        card.remove();
        // Habilitar el botón de crear proyecto
        createBtn.disabled = false;
        // Remover el evento de clic del documento
        document.removeEventListener('click', handleClickOutsideCard);
    }
}


window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
        const dropdowns = document.querySelectorAll('.dropdown-content');
        dropdowns.forEach(dropdown => {
            if (dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        });
    }
};



document.addEventListener('DOMContentLoaded', renderProjects);