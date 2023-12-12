async function callapi() {
    const response = await fetch("http://0.0.0.0:8000/hello");
    const values = await response.json();
    let changeme =  document.getElementById("testing")

    changeme.textContent = values["Nachricht1"]
    console.log(values);
}

async function getlastread(){
    const response = await fetch("http://localhost:8000/api/v1/last-reading");
    const value = await response.json();
    let changeme = document.getElementById("livetemp")
    changeme.textContent = value["temp_c"];
}


async function getClientStatus(){
    const response = await fetch("http://192.168.2.56")
    console.log(response)
}

