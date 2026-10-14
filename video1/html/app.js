let gen = document.getElementById("gen")
let a  = 0
for(let i = 0; i < 28; i++) {
  let row = document.createElement("div")
  row.id = `col-${i}`
  row.className += "row"
  for(let j = 0; j < 28; j++) {
    let el = document.createElement("div")
    el.id = `${a}`
    a++
    el.classList += "element"
    row.appendChild(el)
  }
  gen.appendChild(row)
}
const boxes = document.querySelectorAll(".element")
let mnist_v = []
let clearMnistV = () => {
  for(let i = 0; i < 28*28; i++) {
    mnist_v[i] = 0
  }
}
let clearCharts = () => {
  document.querySelectorAll(".r_table_chart").forEach(element => {
    element.style.width = "0px"
    element.style.background = "white"
  });
}
clearMnistV()
boxes.forEach(box => {
  box.addEventListener("mousemove", (e) => {
    if(e.buttons === 1) {
      box.style.background = 'black'
      mnist_v[box.id] = 255
    }
  })
  box.addEventListener("mouseleave", (e) => {
    if(e.buttons === 1) box.style.background = 'red'
  })
});
let clearElements = () => {
  clearMnistV()
  boxes.forEach(element => {
    element.style.background = "white"
    document.getElementById("model_image").value = ""
    document.getElementById("model_label").value = ""
  });
  clearCharts()
}
let display = () => {
  mnist_v.forEach(element => {
    console.log(element)
  });
  document.getElementById("display").textContent = mnist_v
}
let prepare = () => {
  document.getElementById("model_image").value = JSON.stringify(mnist_v)
  return true
}
let addToLibrary = () => {
  const sent_data = {
    model_label: document.getElementById("model_label").value,
    model_image: mnist_v
  };

  fetch("/saveNODE", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(sent_data)
  })
  .then(res => res.text())
  .then(data => {
    if(data) {
      document.getElementById("saveData_status").background = "green"
    }
    else {
      document.getElementById("saveData_status").background = "red"
    }
  })
  
}
function sendData() {
  clearCharts()
  const sent_data = {
    model_label: document.getElementById("model_label").value,
    model_image: mnist_v
  };

  fetch("/api", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(sent_data)
  })
  .then(res => res.text())
  .then(data => {
    const data_json = JSON.parse(data)
    console.log(JSON.stringify(data_json))
    document.getElementById("data_json").textContent = data_json
    const prediction = data_json["prediction"]
    document.getElementById("r_prediction").textContent = `Prediction: ${prediction}`
    const accuracy = data_json["accuracy"]
    document.getElementById("r_accuracy").textContent = `Accuracy: ${accuracy}`
    for(let i = 0; i < 10; i++) {
      let probability = data_json["probabilities"][i]
      console.log(probability)
      let chart = document.getElementById(`r_table_chart_${i+1}`)
      chart.style.width = `${probability*100}%`
      if(i == prediction) {
        if(accuracy == 1) {
          chart.style.backgroundColor = `green`
        }
        else {
          chart.style.backgroundColor = `red`
        }
      }
    }
  });
}
// let exportos = () => {
//   fetch("/run-python")
//     .then(res => res.text())
//     .then(data => console.log(data));
// }