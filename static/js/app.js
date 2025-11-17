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
function createTask(title, description, status = "todo") {
    return {
        id: Date.now(),  // Simples id local
        title,
        description,
        status
    };
}

saveTaskBtn.addEventListener("click", () => {
    const title = inputTitle.value.trim();
    const description = inputDesc.value.trim();

    if (!title) {
        alert("A tarefa precisa de um título!");
        return;
    }

    const newTask = createTask(title, description);
    tasks.push(newTask);

    renderTasks();
    closeModal();

    // ========== INTEGRAR COM BACKEND AQUI ==========
    // fetch('/api/tasks', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(newTask)
    // });
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

        card.innerHTML = `
            <h4>${task.title}</h4>
            <p>${task.description || ""}</p>
        `;

        enableDragEvents(card);

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
        column.style.backgroundColor = "#E2E8F0";
    });

    column.addEventListener("dragleave", () => {
        column.style.backgroundColor = "transparent";
    });

    column.addEventListener("drop", () => {
        column.style.backgroundColor = "transparent";
        if (draggedTask) {
            column.appendChild(draggedTask);

            const id = draggedTask.getAttribute("data-id");
            const task = tasks.find(t => t.id == id);

            if (task) {
                // Atualizar o status baseado na coluna onde caiu
                if (column.id === "todo-list") task.status = "todo";
                if (column.id === "doing-list") task.status = "doing";
                if (column.id === "done-list") task.status = "done";

                // ========== ATUALIZAR NO BACKEND AQUI ==========
                // fetch(`/api/tasks/${task.id}`, {
                //     method: 'PUT',
                //     headers: { 'Content-Type': 'application/json' },
                //     body: JSON.stringify(task)
                // });
            }
        }
    });
});


// ============================================================
//  CARREGAR TAREFAS DA API (FUTURO BACKEND)
// ============================================================
async function loadTasksFromAPI() {
    // Exemplo de como seria:
    // const response = await fetch('/api/tasks');
    // tasks = await response.json();
    // renderTasks();

    // Por enquanto: vazio
    renderTasks();
}

// Iniciar
loadTasksFromAPI();
