<script>
    function addTask() {
        let taskInput = document.getElementById("new-task");
        let taskText = taskInput.value.trim();
        if (taskText === "") return;

        let li = document.createElement("li");
        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";

        let span = document.createElement("span");
        span.textContent = taskText;

        li.appendChild(checkbox);
        li.appendChild(span);
        document.getElementById("todo-list").appendChild(li);

        taskInput.value = "";
    }
</script>
