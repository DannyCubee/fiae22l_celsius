const test_host = "0.0.0.0:8000"
const live_host = "172.20.174.121:8000"

async function callapi() {
    const response = await fetch(`/hello`);
    console.log(live_host);
    const values = await response.json();
    let changeme =  document.getElementById("testing")

    changeme.textContent = values["Nachricht1"]
    console.log(values);
}

async function getlastread(){
    const response = await fetch("/api/v1/last-reading");
    const value = await response.json();
    let changeme = document.getElementById("livetemp")
    let marqueetext = `Last reading from ${value["client"]}, ${value["temp_c"]}°C/${value["temp_f"]}°F`
    changeme.textContent = marqueetext;
}


async function getClientStatus(){
    const rpi1_statustext = document.getElementById("client1_status")
    const rpi2_statustext = document.getElementById("client2_status")

    rpi1_statustext.style.color = "gray"
    rpi1_statustext.textContent = "loading..."
    rpi2_statustext.style.color = "gray"
    rpi2_statustext.textContent = "loading..."


    const response1 = await fetch("/get-uptime-rp1")
    const value = await response1.json()

    console.log(value)

    if (value === true){
        rpi1_statustext.textContent = "ONLINE";
        rpi1_statustext.style.color = "green";
    } else {
        rpi1_statustext.textContent = "OFFLINE";
        rpi1_statustext.style.color = "red";
    }


    const response2 = await fetch("/get-uptime-rp2")
    const value2 = await response2.json()

    console.log(value2)


    if (value2 === true){
        rpi2_statustext.textContent = "ONLINE";
        rpi2_statustext.style.color = "green";
    } else {
        rpi2_statustext.textContent = "OFFLINE";
        rpi2_statustext.style.color = "red";
    }

}

async function getValues(){
    const response = await fetch("/api/v1/all-temperatures");
    const value = await response.json();

    value.forEach(obj => {console.log(obj["temp_c"])})
}
