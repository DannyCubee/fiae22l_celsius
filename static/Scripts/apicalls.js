async function callapi() {
    const response = await fetch("http://0.0.0.0:8000/hello");
    const values = await response.json();
    let changeme =  document.getElementById("testing")

    changeme.textContent = values["Nachricht1"]
    console.log(values);
}