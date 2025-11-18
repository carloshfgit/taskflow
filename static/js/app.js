// ============================================================
//  ELEMENTOS DA INTERFACE
// ============================================================
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

// Lista local de tarefas (antes da API Flask)
let tasks = [];
let draggedTask = null;


// ============================================================
//  MODAL – ABRIR E FECHAR
// ============================================================
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


// ============================================================
//  CRIAR TAREFA
// ============================================================
// 
saveTaskBtn.addEventListener("click", async () => { // Marcamos como async
    const title = inputTitle.value.trim();
    const description = inputDesc.value.trim();

    if (!title) {
        alert("A tarefa precisa de um título!");
        return;
    }

    // ========== INTEGRAR COM BACKEND AQUI ==========
    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description }) // Envia só o necessário
        });

        if (!response.ok) {
            // Se o servidor retornar um erro (400, 500)
            const errorData = await response.json();
            throw new Error(errorData.error || "Falha na requisição");
        }

        // Pega a tarefa completa (com ID e status) de volta do servidor
        const newTask = await response.json();

        // Adiciona a tarefa (vinda do backend) à lista local
        tasks.push(newTask);

        renderTasks(); // Re-renderiza a tela
        closeModal();

    } catch (error) {
        console.error("Erro ao salvar tarefa:", error);
        alert(`Não foi possível salvar a tarefa: ${error.message}`);
    }
});

// ============================================================
//  RENDERIZAR TAREFAS NAS COLUNAS
// ============================================================
function renderTasks() {
    todoList.innerHTML = "";
    doingList.innerHTML = "";
    doneList.innerHTML = "";

    tasks.forEach(task => {
        const card = document.createElement("div");
        card.classList.add("task-card");
        card.setAttribute("draggable", "true");
        card.setAttribute("data-id", task.id);

        // 1. ADICIONADO O BOTÃO DE EXCLUIR
        card.innerHTML = `
            <div class="task-header">
                <h4>${task.title}</h4>
                <button class="delete-btn" data-id="${task.id}">X</button>
            </div>
            <p>${task.description || ""}</p>
        `;

        enableDragEvents(card);
        
        // 2. ADICIONA O EVENT LISTENER PARA O BOTÃO DE EXCLUIR
        card.querySelector(".delete-btn").addEventListener("click", (e) => {
            e.stopPropagation(); // Impede o drag de começar sem querer
            const idToDelete = e.target.getAttribute("data-id");
            
            // Confirmação com o usuário
            if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
                deleteTask(idToDelete);
            }
        });


        if (task.status === "todo") todoList.appendChild(card);
        if (task.status === "doing") doingList.appendChild(card);
        if (task.status === "done") doneList.appendChild(card);
    });
}


// ============================================================
//  DRAG & DROP DOS CARDS
// ============================================================
function enableDragEvents(card) {

    // Início do arrasto
    card.addEventListener("dragstart", () => {
        draggedTask = card;
        card.style.opacity = "0.5";
    });

    // Fim do arrasto
    card.addEventListener("dragend", () => {
        draggedTask.style.opacity = "1";
        draggedTask = null;
    });
}

// Permitir soltar nas colunas
const columns = document.querySelectorAll(".task-list");

columns.forEach(column => {
    column.addEventListener("dragover", e => {
        e.preventDefault();
        // Feedback visual opcional
        // column.style.backgroundColor = "#E2E8F0"; 
    });

    // column.addEventListener("dragleave", () => {
    //     column.style.backgroundColor = "transparent";
    // });

    column.addEventListener("drop", e => {
        e.preventDefault();
        // column.style.backgroundColor = "transparent";
        
        if (draggedTask) {
            column.appendChild(draggedTask); // 1. Atualiza a UI imediatamente

            const id = draggedTask.getAttribute("data-id");
            const newStatus = column.id.replace('-list', ''); // "todo", "doing" ou "done"

            // 2. Encontra a tarefa no array local
            const task = tasks.find(t => t.id == id);
            
            if (task && task.status !== newStatus) {
                // 3. Atualiza o status no array local
                task.status = newStatus;

                // 4. ========== ATUALIZAR NO BACKEND AQUI ==========
                // Envia a mudança para a API
                fetch(`/api/tasks/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: newStatus }) // Envia só o novo status
                })
                .then(response => {
                    if (!response.ok) {
                        // Se falhar (ex: regra de negócio barrou),
                        // podemos recarregar tudo para reverter
                        console.error("Falha ao atualizar o status da tarefa.");
                        alert("Não foi possível mover a tarefa (regra de negócio?).");
                        // Recarrega do zero para garantir consistência
                        loadTasksFromAPI(); 
                    }
                    // Se der certo, não precisa fazer nada,
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

// ============================================================
//  FUNÇÃO DE EXCLUIR TAREFA (NOVA)
// ============================================================
async function deleteTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Falha ao excluir a tarefa.");
        }

        // Se a API confirmou a exclusão:
        // 1. Remove a tarefa do array local 'tasks'
        tasks = tasks.filter(task => task.id != id);
        
        // 2. Re-renderiza a UI
        renderTasks();

    } catch (error) {
        console.error("Erro ao excluir tarefa:", error);
        alert(error.message);
    }
}

// ============================================================
//  CARREGAR TAREFAS DA API 
// ============================================================
async function loadTasksFromAPI() {
    try {
        const response = await fetch('/api/tasks'); // 1. Faz a requisição GET
        
        if (!response.ok) {
            throw new Error("Não foi possível carregar as tarefas.");
        }
        
        const tasksFromServer = await response.json(); // 2. Pega o JSON
        
        tasks = tasksFromServer; // 3. Atualiza a lista local
        
        renderTasks(); // 4. Renderiza na tela
        
    } catch (error) {
        console.error("Erro ao carregar tarefas:", error);
        alert(error.message);
        tasks = []; // Garante que a lista esteja vazia se falhar
        renderTasks();
    }
}

// Iniciar
loadTasksFromAPI();