// --- CONFIGURAÇÃO DO WEBSOCKET ---
const socket = io(); // Conecta automaticamente ao servidor atual

socket.on('connect', () => {
    console.log(">> Conectado ao servidor WebSocket!");
});

// Ouve o evento 'update_board' que criamos no Python
socket.on('update_board', (data) => {
    console.log(">> Atualização recebida:", data);
    
    // Simplesmente recarregamos a lista da API para garantir que tudo esteja sincronizado
    loadTasksFromAPI(); 
});

//elementos da interface
const btnStart = document.getElementById("btn-start");
const modal = document.getElementById("task-modal");
const closeModalBtn = document.getElementById("close-modal-btn");
const saveTaskBtn = document.getElementById("save-task-btn");

const inputTitle = document.getElementById("task-title");
const inputDesc = document.getElementById("task-desc");

const todoList = document.getElementById("todo-list");
const doingList = document.getElementById("doing-list");
const doneList = document.getElementById("done-list");

const addButtons = document.querySelectorAll(".add-task-btn");


//lista local de tarefas (antes da API Flask)
let tasks = [];
let draggedTask = null;


//modal (janela) abrir e fechar
function openModal() {
    if (!modal.classList.contains("hidden")) return;
    modal.classList.remove("hidden");
}

function closeModal() {
    console.log("Fechando modal...");
    modal.classList.add("hidden");
    inputTitle.value = "";
    inputDesc.value = "";
}

btnStart.addEventListener("click", openModal);
closeModalBtn.addEventListener("click", closeModal);

addButtons.forEach(btn => {
    btn.addEventListener("click", openModal);
});


//criar tarefa
saveTaskBtn.addEventListener("click", async () => { //marcamos como async
    const title = inputTitle.value.trim();
    const description = inputDesc.value.trim();

    if (!title) {
        alert("A tarefa precisa de um título!");
        return;
    }

    //integracao com backend
    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description }) // Envia só o necessário
        });

        if (!response.ok) {
            //se o servidor retornar um erro (400, 500)
            const errorData = await response.json();
            throw new Error(errorData.error || "Falha na requisição");
        }

        //pega a tarefa completa (com ID e status) de volta do servidor
        const newTask = await response.json();

        //adiciona a tarefa (vinda do backend) à lista local
        tasks.push(newTask);

        renderTasks(); //renderiza a tela
        closeModal();

    } catch (error) {
        console.error("Erro ao salvar tarefa:", error);
        alert(`Não foi possível salvar a tarefa: ${error.message}`);
    }
});

//renderizar tarefas nas colunas
function renderTasks() {
    todoList.innerHTML = "";
    doingList.innerHTML = "";
    doneList.innerHTML = "";

    tasks.forEach(task => {
        const card = document.createElement("div");
        card.classList.add("task-card");
        card.setAttribute("draggable", "true");
        card.setAttribute("data-id", task.id);

        //botao de excluir
        card.innerHTML = `
            <div class="task-header">
                <h4>${task.title}</h4>
                <button class="delete-btn" data-id="${task.id}">X</button>
            </div>
            <p>${task.description || ""}</p>
        `;

        enableDragEvents(card);

        card.querySelector(".delete-btn").addEventListener("click", (e) => {
            e.stopPropagation(); // Impede o drag de começar sem querer
            const idToDelete = e.target.getAttribute("data-id");
            
            //confirmação com o usuário
            if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
                deleteTask(idToDelete);
            }
        });


        if (task.status === "todo") todoList.appendChild(card);
        if (task.status === "doing") doingList.appendChild(card);
        if (task.status === "done") doneList.appendChild(card);
    });
}


//drag and drop dos cards
function enableDragEvents(card) {

    //início do arrasto
    card.addEventListener("dragstart", () => {
        draggedTask = card;
        card.style.opacity = "0.5";
    });

    //fim do arrasto
    card.addEventListener("dragend", () => {
        draggedTask.style.opacity = "1";
        draggedTask = null;
    });
}

//permitir soltar nas colunas
const columns = document.querySelectorAll(".task-list");

columns.forEach(column => {
    column.addEventListener("dragover", e => {
        e.preventDefault(); 
    });

    column.addEventListener("drop", e => {
        e.preventDefault();
        
        if (draggedTask) {
            column.appendChild(draggedTask); //atualiza a UI imediatamente

            const id = draggedTask.getAttribute("data-id");
            const newStatus = column.id.replace('-list', ''); // "todo", "doing" ou "done"

            //encontra a tarefa no array local
            const task = tasks.find(t => t.id == id);
            
            if (task && task.status !== newStatus) {
                //atualiza o status no array local
                task.status = newStatus;

                //integracao com backend
                fetch(`/api/tasks/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: newStatus })
                })
                .then(response => {
                    if (!response.ok) {
                        //se falhar (ex: regra de negócio barrou),
                        //podemos recarregar tudo para reverter
                        console.error("Falha ao atualizar o status da tarefa.");
                        alert("Não foi possível mover a tarefa (regra de negócio?).");
                        //recarrega do zero para garantir consistência
                        loadTasksFromAPI(); 
                    }
                    // se der certo, não precisa fazer nada,
                    // pois a UI e o array local já foram atualizados.
                })
                .catch(error => {
                    console.error("Erro de rede:", error);
                    loadTasksFromAPI(); // Reverte em caso de erro
                });
            }
        }
    });
});

//excluir tarefa
async function deleteTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Falha ao excluir a tarefa.");
        }

        //se a API confirmar a exclusão:
        //remove a tarefa do array local 'tasks'
        tasks = tasks.filter(task => task.id != id);
        
        //renderiza a UI
        renderTasks();

    } catch (error) {
        console.error("Erro ao excluir tarefa:", error);
        alert(error.message);
    }
}

//carregar tarefas da API
async function loadTasksFromAPI() {
    try {
        const response = await fetch('/api/tasks'); //faz a requisição GET
        
        if (!response.ok) {
            throw new Error("Não foi possível carregar as tarefas.");
        }
        
        const tasksFromServer = await response.json(); //pega o JSON
        
        tasks = tasksFromServer; //atualiza a lista local
        
        renderTasks(); //renderiza na tela
        
    } catch (error) {
        console.error("Erro ao carregar tarefas:", error);
        alert(error.message);
        tasks = []; //garante que a lista esteja vazia se falhar
        renderTasks();
    }
}

//iniciar
loadTasksFromAPI();