document.addEventListener("DOMContentLoaded", () => {
    map = document.getElementsByClassName("map-container")[0]
    error_message = document.getElementsByClassName("error-message")[0]
    submit_button = document.getElementsByClassName("submit")[0]

    document.getElementById("form").addEventListener("submit", (e) => {
        error_message.innerHTML = ""
        submit_button.classList.add("loading")

        e.preventDefault();

        var formData = new FormData(document.getElementById("form"));
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                json_response = JSON.parse(xhr.responseText);

                if (json_response["status"] == "200") {
                    map.setAttribute("srcdoc", json_response["content"])
                    map.classList.add("generated")

                    map.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
                }
                else {
                    error_message.innerHTML = json_response["content"]
                }
                
                setTimeout(() => {
                    submit_button.classList.remove("loading")
                }, 800)
            }
        }

        xhr.open("POST", "/map", true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

        xhr.send("artist=" + formData.get("artist").replace(/%20/g, '+'))
    })
})