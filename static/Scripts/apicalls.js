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
    let marqueetext = `Last reading from ${value["client"]}, ${value["temp_c"]}°C/${value["temp_f"]}°F`
    changeme.textContent = marqueetext;
}


async function getClientStatus(){


    const rpi1_statustext = document.getElementById("client1_status")

    rpi1_statustext.style.color = "gray"
    rpi1_statustext.textContent = "loading..."


    const response = await fetch("http://0.0.0.0:8000/get-uptime")
    const value = await response.json()

    console.log(value)

    if (value === true){
        rpi1_statustext.textContent = "ONLINE";
        rpi1_statustext.style.color = "green";
    } else {
        rpi1_statustext.textContent = "OFFLINE";
        rpi1_statustext.style.color = "red";
    }

}

