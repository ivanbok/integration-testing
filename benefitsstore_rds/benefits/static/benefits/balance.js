window.onload = getBalance

function getBalance(){
    fetch('/availablebalance')
    .then(response => {
        console.log(response)
    })
}
